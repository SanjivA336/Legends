from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from uuid import uuid4

# === Base ===
class BaseDocument(BaseModel):
    id: str = "new"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
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
    blueprint_ids: List[str] = Field(default_factory=list)
    object_ids: List[str] = Field(default_factory=list)
    settings: WorldSetting

    def get_creator(self) -> 'User': 
        from backend.database.repos import users_repo
        
        creator = users_repo.get(self.creator_id)
        if creator:
            return creator
        else:
            raise ValueError("Creator not found")

    def get_context(self) -> List['Context']:
        from backend.database.repos import context_repo
        
        results = []
        for cid in self.context_ids:
            context = context_repo.get(cid)
            if context:
                results.append(context)
        return results
    
    def get_blueprints(self) -> List['Blueprint']:
        from backend.database.repos import blueprints_repo
        
        results = []
        for bid in self.blueprint_ids:
            blueprint = blueprints_repo.get(bid)
            if blueprint:
                results.append(blueprint)
        return results
    
    def get_objects(self) -> List['Object']:
        from backend.database.repos import objects_repo
        
        results = []
        for oid in self.object_ids:
            obj = objects_repo.get(oid)
            if obj:
                results.append(obj)
        return results


class Campaign(BaseDocument):
    name: str
    description: Optional[str]
    creator_id: str
    world_id: Optional[str] = None
    context_ids: List[str] = Field(default_factory=list)
    blueprint_ids: List[str] = Field(default_factory=list)
    object_ids: List[str] = Field(default_factory=list)
    settings: WorldSetting
    member_ids: List[str] = Field(default_factory=list)
    era_ids: List[str] = Field(default_factory=list)

    def get_creator(self) -> 'User':
        from backend.database.repos import users_repo
        
        creator = users_repo.get(self.creator_id)
        if creator:
            return creator
        else:
            raise ValueError("Creator not found")

    def get_world(self) -> Optional['World']:
        from backend.database.repos import worlds_repo
        
        return worlds_repo.get(self.world_id) if self.world_id else None

    def get_context(self) -> List['Context']:
        from backend.database.repos import context_repo
        
        results = []
        for cid in self.context_ids:
            context = context_repo.get(cid)
            if context:
                results.append(context)
        return results
    
    def get_blueprints(self) -> List['Blueprint']:
        from backend.database.repos import blueprints_repo
        
        results = []
        for bid in self.blueprint_ids:
            blueprint = blueprints_repo.get(bid)
            if blueprint:
                results.append(blueprint)
        return results
    
    def get_objects(self) -> List['Object']:
        from backend.database.repos import objects_repo
        
        results = []
        for oid in self.object_ids:
            obj = objects_repo.get(oid)
            if obj:
                results.append(obj)
        return results

    def get_members(self) -> List['Member']:
        from backend.database.repos import members_repo
        
        results = []
        for mid in self.member_ids:
            member = members_repo.get(mid)
            if member:
                results.append(member)
        return results

    def get_eras(self) -> List['Era']:
        from backend.database.repos import eras_repo
        
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
        from backend.database.repos import users_repo
        
        return users_repo.get(self.user_id) if self.user_id else None

    def get_campaign(self) -> 'Campaign':
        from backend.database.repos import campaigns_repo
        
        campaign = campaigns_repo.get(self.campaign_id)
        if campaign:
            return campaign
        else:
            raise ValueError("Campaign not found")

    def get_sleeve(self) -> Optional['Object']:
        from backend.database.repos import objects_repo
        
        return objects_repo.get(self.sleeve_id) if self.sleeve_id else None

class Context(BaseDocument):
    name: str
    content: str

# === Blueprint System ===
class CustomField(BaseModel):
    name: str
    type: str  # "int", "str", "dropdown", "bool", "blueprint"
    value: str
    options: Optional[List[str]] = None
    linked_behavior: Optional[str] = None

    def get(self) -> Any:
        if self.type == "blueprint":
            from backend.database.repos import blueprints_repo
            
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
        from backend.database.repos import users_repo
        
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
        from backend.database.repos import users_repo
        
        creator = users_repo.get(self.creator_id)
        if creator:
            return creator
        else:
            raise ValueError("Creator not found")

    def get_blueprint(self) -> 'Blueprint':
        from backend.database.repos import blueprints_repo
        
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
        from backend.database.repos import objectives_repo
        
        result = []
        for child_id in self.children_ids:
            child = objectives_repo.get(child_id)
            if child:
                result.append(child)
        return result
    
    def get_parent(self) -> Optional['Objective']:
        from backend.database.repos import objectives_repo
        
        if self.parent_id:
            return objectives_repo.get(self.parent_id)

class Era(BaseDocument):
    campaign_id: str
    name: str
    description: Optional[str]
    objective_id: str
    chapter_ids: List[str] = Field(default_factory=list)
    
    def get_campaign(self) -> 'Campaign':
        from backend.database.repos import campaigns_repo
        
        campaign = campaigns_repo.get(self.campaign_id)
        if campaign:
            return campaign
        else:
            raise ValueError("Campaign not found")

    def get_objective(self) -> 'Objective':
        from backend.database.repos import objectives_repo
        
        objective = objectives_repo.get(self.objective_id)
        if objective:
            return objective
        else:
            raise ValueError("Objective not found")

    def get_chapters(self) -> List['Chapter']:
        result = []
        for chapter_id in self.chapter_ids:
            from backend.database.repos import chapters_repo
            
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
        from backend.database.repos import chapters_repo
        
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
        from backend.database.repos import eras_repo
        
        era = eras_repo.get(self.era_id)
        if era:
            return era
        else:
            raise ValueError("Era not found")

    def get_objective(self) -> 'Objective':
        from backend.database.repos import objectives_repo
        
        objective = objectives_repo.get(self.objective_id)
        if objective:
            return objective
        else:
            raise ValueError("Objective not found")

    def get_encounters(self) -> List['Encounter']:
        result = []
        for encounter_id in self.encounter_ids:
            from backend.database.repos import encounters_repo
            
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
        from backend.database.repos import encounters_repo
        
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
        from backend.database.repos import chapters_repo
        
        chapter = chapters_repo.get(self.chapter_id)
        if chapter:
            return chapter
        else:
            raise ValueError("Chapter not found")

    def get_actions(self) -> List['Action']:
        from backend.database.repos import actions_repo
        
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
        from backend.database.repos import encounters_repo
        
        encounter = encounters_repo.get(self.encounter_id)
        if encounter:
            return encounter
        else:
            raise ValueError("Encounter not found")

    def get_owner(self) -> 'Member':
        from backend.database.repos import members_repo
        
        owner = members_repo.get(self.owner_member_id)
        if owner:
            return owner
        else:
            raise ValueError("Owner not found")
        
    def get_minigame(self) -> Optional['MinigameResult']:
        from backend.database.repos import minigames_repo
        
        return minigames_repo.get(self.minigame_id) if self.minigame_id else None

    def get_character(self) -> Optional['Object']:
        from backend.database.repos import objects_repo
        
        return objects_repo.get(self.character_object_id) if self.character_object_id else None


class MinigameResult(BaseDocument):
    action_id: str
    type: str
    result: str
    details: Dict[str, Any] = Field(default_factory=dict)
    completed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def get_action(self) -> 'Action':
        from backend.database.repos import actions_repo
        
        action = actions_repo.get(self.action_id)
        if action:
            return action
        else:
            raise ValueError("Action not found")