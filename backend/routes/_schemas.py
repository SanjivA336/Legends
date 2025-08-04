from datetime import datetime, timezone
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from backend.models import *

# === Config ===
EMPTY_STRING = ""

# === Users & Core Entities ===

# --- Payload: all optional fields, no from_model ---
class UserPayload(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password_current: Optional[str] = None
    password_new: Optional[str] = None

    def to_model(self, model: User) -> User:
        update_data = self.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(model, field, value)
        return model



# --- Response: fields required, from_model included, no to_model ---
class UserResponse(BaseModel):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    username: str
    email: EmailStr
    password_current: Optional[str] = None
    password_new: Optional[str] = None

    @staticmethod
    def from_model(model: User) -> "UserResponse":
        schema = UserResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            username=model.username,
            email=model.email,
            password_current=None,
            password_new=None,
        )
        return schema

# === World ===

class WorldPayload(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    creator_id: Optional[str] = None
    context_ids: Optional[List[str]] = None
    blueprint_ids: Optional[List[str]] = None
    object_ids: Optional[List[str]] = None
    settings: Optional[WorldSetting] = None

    def to_model(self, model: World) -> World:
        update_data = self.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(model, field, value)
        return model


class WorldResponse(BaseModel):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    name: str
    description: Optional[str] = None
    creator: UserResponse
    contexts: List['ContextResponse']
    blueprints: List['BlueprintResponse'] = []
    objects: List['ObjectResponse'] = []
    settings: WorldSetting

    @staticmethod
    def from_model(model: World) -> "WorldResponse":
        creator = model.get_creator()
        contexts = model.get_context()
        blueprints = model.get_blueprints()
        objects = model.get_objects()
        
        schema = WorldResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            name=model.name,
            description=model.description,
            creator=UserResponse.from_model(creator),
            contexts=[ContextResponse.from_model(c) for c in contexts],
            blueprints=[BlueprintResponse.from_model(b) for b in blueprints],
            objects=[ObjectResponse.from_model(o) for o in objects],
            settings=model.settings,
        )
        return schema


# === Campaign ===

class CampaignPayload(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    creator_id: Optional[str] = None
    world_id: Optional[str] = None
    context_ids: Optional[List[str]] = None
    blueprint_ids: Optional[List[str]] = None
    object_ids: Optional[List[str]] = None
    settings: Optional[WorldSetting] = None
    member_ids: Optional[List[str]] = None
    era_ids: Optional[List[str]] = None

    def to_model(self, model: Campaign) -> Campaign:
        update_data = self.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(model, field, value)
        return model


class CampaignResponse(BaseModel):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    name: str
    description: Optional[str] = None
    creator: UserResponse
    world: Optional[WorldResponse] = None
    contexts: List['ContextResponse']
    blueprints: List['BlueprintResponse']
    objects: List['ObjectResponse']
    settings: WorldSetting
    members: List['MemberResponse']
    eras: List['EraResponse']

    @staticmethod
    def from_model(model: Campaign) -> "CampaignResponse":
        creator = model.get_creator()
        world = model.get_world()
        contexts = model.get_context()
        blueprints = model.get_blueprints()
        objects = model.get_objects()
        members = model.get_members()
        eras = model.get_eras()

        schema = CampaignResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            name=model.name,
            description=model.description,
            creator=UserResponse.from_model(creator),
            world=WorldResponse.from_model(world) if world else None,
            contexts=[ContextResponse.from_model(c) for c in contexts],
            blueprints=[BlueprintResponse.from_model(b) for b in blueprints],
            objects=[ObjectResponse.from_model(o) for o in objects],
            settings=model.settings,
            members=[MemberResponse.from_model(m) for m in members],
            eras=[EraResponse.from_model(e) for e in eras],
        )
        return schema


# === Member ===

class MemberPayload(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    campaign_id: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None
    sleeve_id: Optional[str] = None

    def to_model(self, model: Member) -> Member:
        update_data = self.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(model, field, value)
        return model


class MemberResponse(BaseModel):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    user: Optional[UserResponse]
    campaign: CampaignResponse
    role: str
    status: str
    sleeve: Optional['ObjectResponse']

    @staticmethod
    def from_model(model: Member) -> "MemberResponse":
        user = model.get_user()
        campaign = model.get_campaign()
        sleeve = model.get_sleeve()

        schema = MemberResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            user=UserResponse.from_model(user) if user else None,
            campaign=CampaignResponse.from_model(campaign),
            role=model.role,
            status=model.status,
            sleeve=ObjectResponse.from_model(sleeve) if sleeve else None
        )
        return schema


# === Context ===

class ContextPayload(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    content: Optional[str] = None

    def to_model(self, model: Context) -> Context:
        update_data = self.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(model, field, value)
        return model


class ContextResponse(BaseModel):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    name: str
    content: str

    @staticmethod
    def from_model(model: Context) -> "ContextResponse":
        schema = ContextResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            name=model.name,
            content=model.content,
        )
        return schema


# === Blueprint ===
class BlueprintPayload(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    creator_id: Optional[str] = None
    is_public: Optional[bool] = None
    is_developer: Optional[bool] = None
    fields: Optional[List[CustomField]] = None

    def to_model(self, model: Blueprint) -> Blueprint:
        update_data = self.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(model, field, value)
        return model


class BlueprintResponse(BaseModel):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    name: str
    description: Optional[str] = None
    creator: UserResponse
    is_public: bool
    is_developer: bool
    fields: List[CustomField]

    @staticmethod
    def from_model(model: Blueprint) -> "BlueprintResponse":
        creator = model.get_creator()
        schema = BlueprintResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            name=model.name,
            description=model.description,
            creator=UserResponse.from_model(creator),
            is_public=model.is_public,
            is_developer=model.is_developer,
            fields=model.fields,
        )
        return schema


# === Object ===

class ObjectPayload(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    creator_id: Optional[str] = None
    blueprint_id: Optional[str] = None
    fields: Optional[List[CustomField]] = None

    def to_model(self, model: Object) -> Object:
        update_data = self.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(model, field, value)
        return model

class ObjectResponse(BaseModel):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    name: str
    description: Optional[str] = None
    creator: UserResponse
    blueprint: BlueprintResponse
    fields: List[CustomField]

    @staticmethod
    def from_model(model: Object) -> "ObjectResponse":
        creator = model.get_creator()
        blueprint = model.get_blueprint()

        schema = ObjectResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            name=model.name,
            description=model.description,
            creator=UserResponse.from_model(creator),
            blueprint=BlueprintResponse.from_model(blueprint),
            fields=model.fields,
        )
        return schema


# === Narrative System ===

class ObjectivePayload(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    task: Optional[str] = None
    progress: Optional[int] = None
    children_ids: Optional[List[str]] = None
    parent_id: Optional[str] = None

    def to_model(self, model: Objective) -> Objective:
        update_data = self.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(model, field, value)
        return model


class ObjectiveResponse(BaseModel):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    name: str
    task: str
    progress: int
    children: List['ObjectiveResponse']
    parent: Optional['ObjectiveResponse']

    @staticmethod
    def from_model(model: Objective) -> "ObjectiveResponse":
        children = model.get_children()
        parent = model.get_parent()
        schema = ObjectiveResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            name=model.name,
            task=model.task,
            progress=model.progress,
            children=[ObjectiveResponse.from_model(c) for c in children],
            parent=ObjectiveResponse.from_model(parent) if parent else None,
        )
        return schema


class EraPayload(BaseModel):
    id: Optional[str] = None
    campaign_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    objective_id: Optional[str] = None
    chapter_ids: Optional[List[str]] = None

    def to_model(self, model: Era) -> Era:
        update_data = self.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(model, field, value)
        return model


class EraResponse(BaseModel):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    campaign: CampaignResponse
    name: str
    description: Optional[str] = None
    objective: ObjectiveResponse
    chapters: List['ChapterResponse']

    @staticmethod
    def from_model(model: Era) -> "EraResponse":
        campaign = model.get_campaign()
        objective = model.get_objective()
        chapters = model.get_chapters()

        schema = EraResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            campaign=CampaignResponse.from_model(campaign),
            name=model.name,
            description=model.description,
            objective=ObjectiveResponse.from_model(objective),
            chapters=[ChapterResponse.from_model(c) for c in chapters],
        )
        return schema


class ChapterPayload(BaseModel):
    id: Optional[str] = None
    era_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    objective_id: Optional[str] = None
    encounter_ids: Optional[List[str]] = None

    def to_model(self, model: Chapter) -> Chapter:
        update_data = self.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(model, field, value)
        return model


class ChapterResponse(BaseModel):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    era: EraResponse
    name: str
    description: Optional[str] = None
    objective: ObjectiveResponse
    encounters: List['EncounterResponse']

    @staticmethod
    def from_model(model: Chapter) -> "ChapterResponse":
        era = model.get_era()
        objective = model.get_objective()
        encounters = model.get_encounters()

        schema = ChapterResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            era=EraResponse.from_model(era),
            name=model.name,
            description=model.description,
            objective=ObjectiveResponse.from_model(objective),
            encounters=[EncounterResponse.from_model(c) for c in encounters],
        )
        return schema


class EncounterPayload(BaseModel):
    id: Optional[str] = None
    chapter_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    action_ids: Optional[List[str]] = None

    def to_model(self, model: Encounter) -> Encounter:
        update_data = self.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(model, field, value)
        return model

class EncounterResponse(BaseModel):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    chapter: ChapterResponse
    name: str
    description: Optional[str] = None
    actions: List['ActionResponse']

    @staticmethod
    def from_model(model: Encounter) -> "EncounterResponse":
        chapter = model.get_chapter()
        actions = model.get_actions()

        schema = EncounterResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            chapter=ChapterResponse.from_model(chapter),
            name=model.name,
            description=model.description,
            actions=[ActionResponse.from_model(c) for c in actions],
        )
        return schema


# === Action & Events ===

class ActionPayload(BaseModel):
    id: Optional[str] = None
    encounter: Optional[EncounterPayload] = None
    owner_member_id: Optional[str] = None
    character_object_id: Optional[str] = None
    content: Optional[str] = None
    type: Optional[str] = None
    dm_response: Optional[str] = None
    minigame_id: Optional[str] = None

    def to_model(self, model: Action) -> Action:
        update_data = self.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(model, field, value)
        return model


class ActionResponse(BaseModel):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    encounter: EncounterResponse
    owner_member: MemberResponse
    character_object: Optional[ObjectResponse] = None
    content: str
    type: str
    dm_response: Optional[str] = None
    minigame: Optional['MinigameResultResponse'] = None

    @staticmethod
    def from_model(model: Action) -> "ActionResponse":
        encounter = model.get_encounter()
        owner_member = model.get_owner()
        character_object = model.get_character()
        minigame = model.get_minigame()

        schema = ActionResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            encounter=EncounterResponse.from_model(encounter),
            owner_member=MemberResponse.from_model(owner_member),
            character_object=ObjectResponse.from_model(character_object) if character_object else None,
            content=model.content,
            type=model.type,
            dm_response=model.dm_response,
            minigame=MinigameResultResponse.from_model(minigame) if minigame else None,
        )
        return schema


class MinigameResultPayload(BaseModel):
    id: Optional[str] = None
    action_id: Optional[str] = None
    type: Optional[str] = None
    result: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    completed_at: Optional[datetime] = None

    def to_model(self, model: MinigameResult) -> MinigameResult:
        update_data = self.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(model, field, value)
        return model


class MinigameResultResponse(BaseModel):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    action: ActionResponse
    type: str
    result: str
    details: Dict[str, Any]
    completed_at: datetime

    @staticmethod
    def from_model(model: MinigameResult) -> "MinigameResultResponse":
        action = model.get_action()
        schema = MinigameResultResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            action=ActionResponse.from_model(action),
            type=model.type,
            result=model.result,
            details=model.details,
            completed_at=model.completed_at,
        )
        return schema


# Resolve forward refs
UserPayload.model_rebuild()
UserResponse.model_rebuild()
WorldPayload.model_rebuild()
WorldResponse.model_rebuild()
CampaignPayload.model_rebuild()
CampaignResponse.model_rebuild()
MemberPayload.model_rebuild()
MemberResponse.model_rebuild()
ContextPayload.model_rebuild()
ContextResponse.model_rebuild()
BlueprintPayload.model_rebuild()
BlueprintResponse.model_rebuild()
ObjectPayload.model_rebuild()
ObjectResponse.model_rebuild()
ObjectivePayload.model_rebuild()
ObjectiveResponse.model_rebuild()
EraPayload.model_rebuild()
EraResponse.model_rebuild()
ChapterPayload.model_rebuild()
ChapterResponse.model_rebuild()
EncounterPayload.model_rebuild()
EncounterResponse.model_rebuild()
ActionPayload.model_rebuild()
ActionResponse.model_rebuild()
MinigameResultPayload.model_rebuild()
MinigameResultResponse.model_rebuild()
