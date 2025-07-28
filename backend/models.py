from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import uuid4

from backend.database.repos import users_repo, worlds_repo, campaigns_repo, members_repo, context_repo, blueprints_repo, objects_repo, objectives_repo, eras_repo, chapters_repo, encounters_repo, actions_repo, minigames_repo


# === Base ===
class BaseDocument(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


# === Users & Core Entities ===
class User(BaseDocument):
    username: str
    email: EmailStr
    password_hash: str

class WorldSetting(BaseModel):
    is_public: bool

class World(BaseDocument):
    name: str
    description: Optional[str]
    creator_id: str
    context_ids: List[str] = Field(default_factory=list)
    settings: WorldSetting

    def get_creator(self) -> 'User': 
        creator = users_repo.get(self.creator_id)
        if creator:
            return creator
        else:
            raise ValueError("Creator not found")

    def get_context(self) -> List['Context']:
        results = []
        for cid in self.context_ids:
            context = context_repo.get(cid)
            if context:
                results.append(context)
        return results


class Campaign(BaseDocument):
    name: str
    description: Optional[str]
    creator_id: str
    world_id: Optional[str] = None
    context_ids: List[str] = Field(default_factory=list)
    settings: WorldSetting
    member_ids: List[str] = Field(default_factory=list)
    era_ids: List[str] = Field(default_factory=list)

    def get_creator(self) -> 'User':
        creator = users_repo.get(self.creator_id)
        if creator:
            return creator
        else:
            raise ValueError("Creator not found")

    def get_world(self) -> Optional['World']:
        return worlds_repo.get(self.world_id) if self.world_id else None

    def get_context(self) -> List['Context']:
        results = []
        for cid in self.context_ids:
            context = context_repo.get(cid)
            if context:
                results.append(context)
        return results

    def get_members(self) -> List['Member']:
        results = []
        for mid in self.member_ids:
            member = members_repo.get(mid)
            if member:
                results.append(member)
        return results

    def get_eras(self) -> List['Era']:
        results = []
        for eid in self.era_ids:
            era = eras_repo.get(eid)
            if era:
                results.append(era)
        return results


# === Game Structure ===
class Member(BaseDocument):
    user_id: Optional[str]
    campaign_id: str
    role: str  # "player", "dm", "spectator"
    status: str = "active"
    sleeve_id: Optional[str] = None  # links to a GameObject like a character

    def get_user(self) -> Optional['User']:
        return users_repo.get(self.user_id) if self.user_id else None

    def get_campaign(self) -> 'Campaign':
        campaign = campaigns_repo.get(self.campaign_id)
        if campaign:
            return campaign
        else:
            raise ValueError("Campaign not found")

    def get_sleeve(self) -> Optional['Object']:
        return objects_repo.get(self.sleeve_id) if self.sleeve_id else None

class Context(BaseDocument):
    name: str
    type: str
    data: Dict[str, Any] = Field(default_factory=dict)

# === Blueprint System ===
class CustomField(BaseModel):
    name: str
    type: str  # "int", "str", "dropdown", "bool", "blueprint"
    value: str
    options: Optional[List[str]] = None
    linked_behavior: Optional[str] = None

    def get(self) -> Any:
        if self.type == "blueprint":
            return blueprints_repo.get(self.value)
        elif self.type == "dropdown" and self.options:
            index = int(self.value)
            return self.options[index] if 0 <= index < len(self.options) else None
        else:
            return self.value

class Blueprint(BaseDocument):
    name: str
    description: Optional[str]
    creator_id: str
    is_public: bool = False
    is_developer: bool = False
    fields: List[CustomField] # fields with default values

    def get_creator(self) -> 'User':
        creator = users_repo.get(self.creator_id)
        if creator:
            return creator
        else:
            raise ValueError("Creator not found")

class Object(BaseDocument):
    name: str
    description: Optional[str]
    creator_id: str
    blueprint_id: str
    fields: List[CustomField] # fields with instance values

    def get_creator(self) -> 'User':
        creator = users_repo.get(self.creator_id)
        if creator:
            return creator
        else:
            raise ValueError("Creator not found")

    def get_blueprint(self) -> 'Blueprint':
        blueprint = blueprints_repo.get(self.blueprint_id)
        if blueprint:
            return blueprint
        else:
            raise ValueError("Blueprint not found")

# === Narrative System ===
class Objective(BaseDocument):
    name: str
    task: str
    progress: int
    children_ids: List[str] = Field(default_factory=list)
    parent_id: Optional[str] = None

    def get_children(self) -> List['Objective']:
        result = []
        for child_id in self.children_ids:
            child = objectives_repo.get(child_id)
            if child:
                result.append(child)
        return result
    
    def get_parent(self) -> Optional['Objective']:
        if self.parent_id:
            return objectives_repo.get(self.parent_id)

class Era(BaseDocument):
    campaign_id: str
    name: str
    description: Optional[str]
    objective_id: str
    chapter_ids: List[str] = Field(default_factory=list)
    
    def get_campaign(self) -> 'Campaign':
        campaign = campaigns_repo.get(self.campaign_id)
        if campaign:
            return campaign
        else:
            raise ValueError("Campaign not found")

    def get_objective(self) -> 'Objective':
        objective = objectives_repo.get(self.objective_id)
        if objective:
            return objective
        else:
            raise ValueError("Objective not found")

    def get_chapters(self) -> List['Chapter']:
        result = []
        for chapter_id in self.chapter_ids:
            chapter = chapters_repo.get(chapter_id)
            if chapter:
                result.append(chapter)
        return result

    def get_encounters(self) -> List['Encounter']:
        result = []
        chapters = self.get_chapters()
        for chapter in chapters:
            encounters = chapter.get_encounters()
            result.extend(encounters)
        return result
    
    def get_actions(self) -> List['Action']:
        result = []
        encounters = self.get_encounters()
        for encounter in encounters:
            actions = encounter.get_actions()
            result.extend(actions)
        return result
    
    def get_recent_chapters(self, limit: int = 2) -> List['Chapter']:
        result = []
        for chapter_id in self.chapter_ids[-limit:]:
            chapter = chapters_repo.get(chapter_id)
            if chapter:
                result.append(chapter)
        return result

class Chapter(BaseDocument):
    era_id: str
    name: str
    description: Optional[str]
    objective_id: str
    encounter_ids: List[str] = Field(default_factory=list)
    
    def get_era(self) -> 'Era':
        era = eras_repo.get(self.era_id)
        if era:
            return era
        else:
            raise ValueError("Era not found")

    def get_objective(self) -> 'Objective':
        objective = objectives_repo.get(self.objective_id)
        if objective:
            return objective
        else:
            raise ValueError("Objective not found")

    def get_encounters(self) -> List['Encounter']:
        result = []
        for encounter_id in self.encounter_ids:
            encounter = encounters_repo.get(encounter_id)
            if encounter:
                result.append(encounter)
        return result
    
    def get_actions(self) -> List['Action']:
        result = []
        encounters = self.get_encounters()
        for encounter in encounters:
            actions = encounter.get_actions()
            result.extend(actions)
        return result

    def get_recent_encounters(self, limit: int = 2) -> List['Encounter']:
        result = []
        for encounter_id in self.encounter_ids[-limit:]:
            encounter = encounters_repo.get(encounter_id)
            if encounter:
                result.append(encounter)
        return result


class Encounter(BaseDocument):
    chapter_id: str
    name: str
    description: Optional[str]
    action_ids: List[str] = Field(default_factory=list)
    
    def get_chapter(self) -> 'Chapter':
        chapter = chapters_repo.get(self.chapter_id)
        if chapter:
            return chapter
        else:
            raise ValueError("Chapter not found")

    def get_actions(self) -> List['Action']:
        result = []
        for action_id in self.action_ids:
            action = actions_repo.get(action_id)
            if action:
                result.append(action)
        return result

# === Gameplay & Events ===

class Action(BaseDocument):
    encounter_id: str
    owner_member_id: str
    character_object_id: Optional[str]
    content: str
    type: str
    dm_response: Optional[str]
    minigame_id: Optional[str]

    def get_encounter(self) -> 'Encounter':
        encounter = encounters_repo.get(self.encounter_id)
        if encounter:
            return encounter
        else:
            raise ValueError("Encounter not found")

    def get_owner(self) -> 'Member':
        owner = members_repo.get(self.owner_member_id)
        if owner:
            return owner
        else:
            raise ValueError("Owner not found")
        
    def get_minigame(self) -> Optional['MinigameResult']:
        return minigames_repo.get(self.minigame_id) if self.minigame_id else None

    def get_character(self) -> Optional['Object']:
        return objects_repo.get(self.character_object_id) if self.character_object_id else None


class MinigameResult(BaseDocument):
    action_id: str
    type: str
    result: str
    details: Dict[str, Any] = Field(default_factory=dict)
    completed_at: datetime = Field(default_factory=datetime.utcnow)

    def get_action(self) -> 'Action':
        action = actions_repo.get(self.action_id)
        if action:
            return action
        else:
            raise ValueError("Action not found")