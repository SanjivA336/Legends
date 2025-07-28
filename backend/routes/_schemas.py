from datetime import datetime, timezone
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from backend.models import *

# Payload: Client (frontend) to Server (backend)
# Response: Server (backend) to Client (frontend)

# === Users & Core Entities ===
class UserSchema(BaseDocument):
    username: str
    email: EmailStr
    password_current: Optional[str]
    password_new: Optional[str]

    def to_model(self):
        return User(
            username=self.username,
            email=self.email,
            password_hash="N/A"
        )
        
    @staticmethod
    def from_model(model: User):
        schema = UserSchema(
            username=model.username,
            email=model.email,
            password_current=None,
            password_new=None
        )
        schema.id = model.id
        return schema

class WorldSchema(BaseDocument):
    name: str
    description: Optional[str]
    creator: 'UserSchema'
    contexts: List['ContextSchema']
    settings: WorldSetting
    
    def to_model(self):
        return World(
            name=self.name,
            description=self.description or "",
            creator_id=self.creator.id,
            context_ids=[context.id for context in self.contexts],
            settings=self.settings
        )
        
    @staticmethod
    def from_model(model: World):
        creator = model.get_creator()
        contexts = model.get_context()
        settings = model.settings
        
        schema = WorldSchema(
            name=model.name,
            description=model.description or "",
            creator=UserSchema.from_model(creator),
            contexts=[ContextSchema.from_model(context) for context in contexts],
            settings=settings
        )
        schema.id = model.id
        return schema

class CampaignSchema(BaseDocument):
    name: str
    description: Optional[str]
    creator: 'UserSchema'
    world: Optional['WorldSchema'] = None
    contexts: List['ContextSchema'] = Field(default_factory=list)
    settings: WorldSetting
    members: List['MemberSchema'] = Field(default_factory=list)
    eras: List['EraSchema'] = Field(default_factory=list)

    def to_model(self):
        return Campaign(
            name=self.name,
            description=self.description or "",
            creator_id=self.creator.id,
            world_id=self.world.id if self.world else None,
            context_ids=[context.id for context in self.contexts],
            settings=self.settings,
            member_ids=[member.id for member in self.members],
            era_ids=[era.id for era in self.eras]
        )
        
    @staticmethod
    def from_model(model: Campaign):
        creator = model.get_creator()
        world = model.get_world()
        contexts = model.get_context()
        settings = model.settings
        members = model.get_members()
        eras = model.get_eras()

        schema = CampaignSchema(
            name=model.name,
            description=model.description or "",
            creator=UserSchema.from_model(creator),
            world=WorldSchema.from_model(world) if world else None,
            contexts=[ContextSchema.from_model(context) for context in contexts],
            settings=settings,
            members=[MemberSchema.from_model(member) for member in members],
            eras=[EraSchema.from_model(era) for era in eras]
        )
        
        schema.id = model.id
        return schema

# === Game Structure ===
class MemberSchema(BaseDocument):
    user: Optional['UserSchema']
    campaign: 'CampaignSchema'
    role: str
    status: str = "active"
    sleeve: Optional['ObjectSchema'] = None
    
    def to_model(self):
        return Member(
            user_id=self.user.id if self.user else None,
            campaign_id=self.campaign.id,
            role=self.role,
            status=self.status,
            sleeve_id=self.sleeve.id if self.sleeve else None
        )
        
    @staticmethod
    def from_model(model: Member):
        user = model.get_user()
        campaign = model.get_campaign()
        sleeve = model.get_sleeve()

        schema = MemberSchema(
            user=UserSchema.from_model(user) if user else None,
            campaign=CampaignSchema.from_model(campaign),
            role=model.role,
            status=model.status,
            sleeve=ObjectSchema.from_model(sleeve) if sleeve else None
        )
        
        schema.id = model.id
        return schema

class ContextSchema(BaseDocument):
    name: str
    type: str
    data: Dict[str, Any] = Field(default_factory=dict)
    
    def to_model(self):
        return Context(
            name=self.name,
            type=self.type,
            data=self.data
        )
        
    @staticmethod
    def from_model(model: Context):
        schema = ContextSchema(
            name=model.name,
            type=model.type,
            data=model.data
        )
        schema.id = model.id
        return schema

# === Blueprint System ===
class BlueprintSchema(BaseDocument):
    name: str
    description: Optional[str]
    creator: 'UserSchema'
    is_public: bool = False
    is_developer: bool = False
    fields: List[CustomField] # fields with default values
    
    def to_model(self):
        return Blueprint(
            name=self.name,
            description=self.description or "",
            creator_id=self.creator.id,
            is_public=self.is_public,
            is_developer=self.is_developer,
            fields=[field for field in self.fields]
        )
        
    @staticmethod
    def from_model(model: Blueprint):
        creator = model.get_creator()
        fields = [field for field in model.fields]

        schema = BlueprintSchema(
            name=model.name,
            description=model.description or "",
            creator=UserSchema.from_model(creator),
            is_public=model.is_public,
            is_developer=model.is_developer,
            fields=fields
        )
        
        schema.id = model.id
        return schema

class ObjectSchema(BaseDocument):
    name: str
    description: Optional[str]
    creator: 'UserSchema'
    blueprint: 'BlueprintSchema'
    fields: List[CustomField] # fields with instance values
    
    def to_model(self):
        return Object(
            name=self.name,
            description=self.description or "",
            creator_id=self.creator.id,
            blueprint_id=self.blueprint.id,
            fields=[field for field in self.fields]
        )
        
    @staticmethod
    def from_model(model: Object):
        creator = model.get_creator()
        blueprint = model.get_blueprint()
        fields = [field for field in model.fields]

        schema = ObjectSchema(
            name=model.name,
            description=model.description or "",
            creator=UserSchema.from_model(creator),
            blueprint=BlueprintSchema.from_model(blueprint),
            fields=fields
        )
        
        schema.id = model.id
        return schema

# === Narrative System ===
class ObjectiveSchema(BaseDocument):
    name: str
    task: str
    progress: int
    children: List['ObjectiveSchema'] = Field(default_factory=list)
    parent: Optional['ObjectiveSchema'] = None
    
    def to_model(self):
        return Objective(
            name=self.name,
            task=self.task,
            progress=self.progress,
            children_ids=[child.id for child in self.children],
            parent_id=self.parent.id if self.parent else None
        )
        
    @staticmethod
    def from_model(model: Objective):
        children = model.get_children()
        parent = model.get_parent()

        schema = ObjectiveSchema(
            name=model.name,
            task=model.task,
            progress=model.progress,
            children=[ObjectiveSchema.from_model(child) for child in children],
            parent=ObjectiveSchema.from_model(parent) if parent else None
        )
        
        schema.id = model.id
        return schema
    

class EraSchema(BaseDocument):
    campaign: 'CampaignSchema'
    name: str
    description: Optional[str]
    objective: 'ObjectiveSchema'
    chapters: List['ChapterSchema'] = Field(default_factory=list)
    
    def to_model(self):
        return Era(
            campaign_id=self.campaign.id,
            name=self.name,
            description=self.description or "",
            objective_id=self.objective.id,
            chapter_ids=[chapter.id for chapter in self.chapters]
        )
        
    @staticmethod
    def from_model(model: Era):
        campaign = model.get_campaign()
        objective = model.get_objective()
        chapters = model.get_chapters()

        schema = EraSchema(
            campaign=CampaignSchema.from_model(campaign),
            name=model.name,
            description=model.description or "",
            objective=ObjectiveSchema.from_model(objective),
            chapters=[ChapterSchema.from_model(chapter) for chapter in chapters]
        )
        
        schema.id = model.id
        return schema

class ChapterSchema(BaseDocument):
    era: 'EraSchema'
    name: str
    description: Optional[str]
    objective: 'ObjectiveSchema'
    encounters: List['EncounterSchema'] = Field(default_factory=list)
    
    def to_model(self):
        return Chapter(
            era_id=self.era.id,
            name=self.name,
            description=self.description or "",
            objective_id=self.objective.id,
            encounter_ids=[encounter.id for encounter in self.encounters]
        )
        
    @staticmethod
    def from_model(model: Chapter):
        era = model.get_era()
        objective = model.get_objective()
        encounters = model.get_encounters()

        schema = ChapterSchema(
            era=EraSchema.from_model(era),
            name=model.name,
            description=model.description or "",
            objective=ObjectiveSchema.from_model(objective),
            encounters=[EncounterSchema.from_model(encounter) for encounter in encounters]
        )
        
        schema.id = model.id
        return schema

class EncounterSchema(BaseDocument):
    chapter: 'ChapterSchema'
    name: str
    description: Optional[str]
    actions: List['ActionSchema'] = Field(default_factory=list)
    
    def to_model(self):
        return Encounter(
            chapter_id=self.chapter.id,
            name=self.name,
            description=self.description or "",
            action_ids=[action.id for action in self.actions]
        )
        
    @staticmethod
    def from_model(model: Encounter):
        chapter = model.get_chapter()
        actions = model.get_actions()

        schema = EncounterSchema(
            chapter=ChapterSchema.from_model(chapter),
            name=model.name,
            description=model.description or "",
            actions=[ActionSchema.from_model(action) for action in actions]
        )
        
        schema.id = model.id
        return schema

# === Gameplay & Events ===

class ActionSchema(BaseDocument):
    encounter: 'EncounterSchema'
    owner_member: 'MemberSchema'
    character_object: Optional['ObjectSchema'] = None
    content: str
    type: str
    dm_response: Optional[str]
    minigame: Optional['MinigameResultSchema'] = None
    
    def to_model(self):
        return Action(
            encounter_id=self.encounter.id,
            owner_member_id=self.owner_member.id,
            character_object_id=self.character_object.id if self.character_object else None,
            content=self.content,
            type=self.type,
            dm_response=self.dm_response,
            minigame_id=self.minigame.id if self.minigame else None
        )
        
    @staticmethod
    def from_model(model: Action):
        encounter = model.get_encounter()
        owner_member = model.get_owner()
        character_object = model.get_character()
        minigame = model.get_minigame()

        schema = ActionSchema(
            encounter=EncounterSchema.from_model(encounter),
            owner_member=MemberSchema.from_model(owner_member),
            character_object=ObjectSchema.from_model(character_object) if character_object else None,
            content=model.content,
            type=model.type,
            dm_response=model.dm_response,
            minigame=MinigameResultSchema.from_model(minigame) if minigame else None
        )
        
        schema.id = model.id
        return schema

class MinigameResultSchema(BaseDocument):
    action: 'ActionSchema'
    type: str
    result: str
    details: Dict[str, Any] = Field(default_factory=dict)
    completed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def to_model(self):
        return MinigameResult(
            action_id=self.action.id,
            type=self.type,
            result=self.result,
            details=self.details,
            completed_at=self.completed_at
        )
        
    @staticmethod
    def from_model(model: MinigameResult):
        action = model.get_action()

        schema = MinigameResultSchema(
            action=ActionSchema.from_model(action),
            type=model.type,
            result=model.result,
            details=model.details,
            completed_at=model.completed_at
        )
        
        schema.id = model.id
        return schema
    