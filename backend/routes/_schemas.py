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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password_current: Optional[str] = None
    password_new: Optional[str] = None

    def to_model(self) -> User:
        return User(
            id=self.id or EMPTY_STRING,
            created_at=self.created_at or datetime.now(timezone.utc),
            updated_at=self.updated_at or datetime.now(timezone.utc),
            username=self.username or EMPTY_STRING,
            email=self.email or EMPTY_STRING,
            password_hash=EMPTY_STRING,
        )


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
        sch = UserResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            username=model.username,
            email=model.email,
            password_current=None,
            password_new=None,
        )
        return sch

# === World ===

class WorldPayload(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    name: Optional[str] = None
    description: Optional[str] = None
    creator: Optional[UserPayload] = None
    contexts: Optional[List['ContextPayload']] = None
    settings: Optional[WorldSetting] = None

    def to_model(self) -> World:
        return World(
            id=self.id or EMPTY_STRING,
            created_at=self.created_at or datetime.now(timezone.utc),
            updated_at=self.updated_at or datetime.now(timezone.utc),
            name=self.name or EMPTY_STRING,
            description=self.description or EMPTY_STRING,
            creator_id=self.creator.id or EMPTY_STRING if self.creator else EMPTY_STRING,
            context_ids=[c.id for c in self.contexts if c.id is not None] if self.contexts else [],
            settings=self.settings or WorldSetting(is_public=False)
        )


class WorldResponse(BaseModel):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    name: str
    description: Optional[str] = None
    creator: UserResponse
    contexts: List['ContextResponse']
    settings: WorldSetting

    @staticmethod
    def from_model(model: World) -> "WorldResponse":
        creator = model.get_creator()
        contexts = model.get_context()
        sch = WorldResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            name=model.name,
            description=model.description,
            creator=UserResponse.from_model(creator),
            contexts=[ContextResponse.from_model(c) for c in contexts],
            settings=model.settings,
        )
        return sch


# === Campaign ===

class CampaignPayload(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    name: Optional[str] = None
    description: Optional[str] = None
    creator: Optional[UserPayload] = None
    world: Optional[WorldPayload] = None
    contexts: Optional[List['ContextPayload']] = None
    settings: Optional[WorldSetting] = None
    members: Optional[List['MemberPayload']] = None
    eras: Optional[List['EraPayload']] = None

    def to_model(self) -> Campaign:
        return Campaign(
            id=self.id or EMPTY_STRING,
            created_at=self.created_at or datetime.now(timezone.utc),
            updated_at=self.updated_at or datetime.now(timezone.utc),
            name=self.name or EMPTY_STRING,
            description=self.description,
            creator_id=self.creator.id or EMPTY_STRING if self.creator else EMPTY_STRING,
            world_id=self.world.id if self.world else None,
            context_ids=[c.id for c in self.contexts if c.id is not None] if self.contexts else [],
            settings=self.settings or WorldSetting(is_public=False),
            member_ids=[m.id for m in self.members if m.id is not None] if self.members else [],
            era_ids=[e.id for e in self.eras if e.id is not None] if self.eras else []
        )


class CampaignResponse(BaseModel):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    name: str
    description: Optional[str] = None
    creator: UserResponse
    world: Optional[WorldResponse] = None
    contexts: List['ContextResponse']
    settings: WorldSetting
    members: List['MemberResponse']
    eras: List['EraResponse']

    @staticmethod
    def from_model(model: Campaign) -> "CampaignResponse":
        creator = model.get_creator()
        world = model.get_world()
        contexts = model.get_context()
        members = model.get_members()
        eras = model.get_eras()

        sch = CampaignResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            name=model.name,
            description=model.description,
            creator=UserResponse.from_model(creator),
            world=WorldResponse.from_model(world) if world else None,
            contexts=[ContextResponse.from_model(c) for c in contexts],
            settings=model.settings,
            members=[MemberResponse.from_model(m) for m in members],
            eras=[EraResponse.from_model(e) for e in eras],
        )
        return sch


# === Member ===

class MemberPayload(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    user: Optional[UserPayload] = None
    campaign: Optional[CampaignPayload] = None
    role: Optional[str] = None
    status: Optional[str] = None
    sleeve: Optional['ObjectPayload'] = None

    def to_model(self) -> Member:
        return Member(
            id=self.id or EMPTY_STRING,
            created_at=self.created_at or datetime.now(timezone.utc),
            updated_at=self.updated_at or datetime.now(timezone.utc),
            user_id=self.user.id if self.user else None,
            campaign_id=self.campaign.id or EMPTY_STRING if self.campaign else EMPTY_STRING,
            role=self.role or EMPTY_STRING,
            status=self.status or "active",
            sleeve_id=self.sleeve.id if self.sleeve else None
        )


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

        sch = MemberResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            user=UserResponse.from_model(user) if user else None,
            campaign=CampaignResponse.from_model(campaign),
            role=model.role,
            status=model.status,
            sleeve=ObjectResponse.from_model(sleeve) if sleeve else None
        )
        return sch


# === Context ===

class ContextPayload(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    name: Optional[str] = None
    type: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

    def to_model(self) -> Context:
        return Context(
            id=self.id or EMPTY_STRING,
            created_at=self.created_at or datetime.now(timezone.utc),
            updated_at=self.updated_at or datetime.now(timezone.utc),
            name=self.name or EMPTY_STRING,
            type=self.type or EMPTY_STRING,
            data=self.data or {},
        )


class ContextResponse(BaseModel):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    name: str
    type: str
    data: Dict[str, Any]

    @staticmethod
    def from_model(model: Context) -> "ContextResponse":
        sch = ContextResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            name=model.name,
            type=model.type,
            data=model.data,
        )
        return sch


# === Blueprint ===
class BlueprintPayload(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    name: Optional[str] = None
    description: Optional[str] = None
    creator: Optional[UserPayload] = None
    is_public: Optional[bool] = None
    is_developer: Optional[bool] = None
    fields: Optional[List[CustomField]] = None

    def to_model(self) -> Blueprint:
        return Blueprint(
            id=self.id or EMPTY_STRING,
            created_at=self.created_at or datetime.now(timezone.utc),
            updated_at=self.updated_at or datetime.now(timezone.utc),
            name=self.name or EMPTY_STRING,
            description=self.description,
            creator_id=self.creator.id or EMPTY_STRING if self.creator else EMPTY_STRING,
            is_public=self.is_public or False,
            is_developer=self.is_developer or False,
            fields=self.fields or [],
        )


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
        sch = BlueprintResponse(
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
        return sch


# === Object ===

class ObjectPayload(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    name: Optional[str] = None
    description: Optional[str] = None
    creator: Optional[UserPayload] = None
    blueprint: Optional[BlueprintPayload] = None
    fields: Optional[List[CustomField]] = None

    def to_model(self) -> Object:
        return Object(
            id=self.id or EMPTY_STRING,
            created_at=self.created_at or datetime.now(timezone.utc),
            updated_at=self.updated_at or datetime.now(timezone.utc),
            name=self.name or EMPTY_STRING,
            description=self.description,
            creator_id=self.creator.id or EMPTY_STRING if self.creator else EMPTY_STRING,
            blueprint_id=self.blueprint.id or EMPTY_STRING if self.blueprint else EMPTY_STRING,
            fields=self.fields or [],
        )


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

        sch = ObjectResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            name=model.name,
            description=model.description,
            creator=UserResponse.from_model(creator),
            blueprint=BlueprintResponse.from_model(blueprint),
            fields=model.fields,
        )
        return sch


# === Narrative System ===

class ObjectivePayload(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    name: Optional[str] = None
    task: Optional[str] = None
    progress: Optional[int] = None
    children: Optional[List['ObjectivePayload']] = None
    parent: Optional['ObjectivePayload'] = None

    def to_model(self) -> Objective:
        return Objective(
            id=self.id or EMPTY_STRING,
            created_at=self.created_at or datetime.now(timezone.utc),
            updated_at=self.updated_at or datetime.now(timezone.utc),
            name=self.name or EMPTY_STRING,
            task=self.task or EMPTY_STRING,
            progress=self.progress or 0,
            children_ids=[child.id for child in self.children if child.id is not None] if self.children else [],
            parent_id=self.parent.id if self.parent else None,
        )


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
        sch = ObjectiveResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            name=model.name,
            task=model.task,
            progress=model.progress,
            children=[ObjectiveResponse.from_model(c) for c in children],
            parent=ObjectiveResponse.from_model(parent) if parent else None,
        )
        return sch


class EraPayload(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    campaign: Optional[CampaignPayload] = None
    name: Optional[str] = None
    description: Optional[str] = None
    objective: Optional[ObjectivePayload] = None
    chapters: Optional[List['ChapterPayload']] = None

    def to_model(self) -> Era:
        return Era(
            id=self.id or EMPTY_STRING,
            created_at=self.created_at or datetime.now(timezone.utc),
            updated_at=self.updated_at or datetime.now(timezone.utc),
            campaign_id=self.campaign.id or EMPTY_STRING if self.campaign else EMPTY_STRING,
            name=self.name or EMPTY_STRING,
            description=self.description,
            objective_id=self.objective.id or EMPTY_STRING if self.objective else EMPTY_STRING,
            chapter_ids=[c.id for c in self.chapters if c.id is not None] if self.chapters else [],
        )


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

        sch = EraResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            campaign=CampaignResponse.from_model(campaign),
            name=model.name,
            description=model.description,
            objective=ObjectiveResponse.from_model(objective),
            chapters=[ChapterResponse.from_model(c) for c in chapters],
        )
        return sch


class ChapterPayload(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    era: Optional[EraPayload] = None
    name: Optional[str] = None
    description: Optional[str] = None
    objective: Optional[ObjectivePayload] = None
    encounters: Optional[List['EncounterPayload']] = None

    def to_model(self) -> Chapter:
        return Chapter(
            id=self.id or EMPTY_STRING,
            created_at=self.created_at or datetime.now(timezone.utc),
            updated_at=self.updated_at or datetime.now(timezone.utc),
            era_id=self.era.id or EMPTY_STRING if self.era else EMPTY_STRING,
            name=self.name or EMPTY_STRING,
            description=self.description,
            objective_id=self.objective.id or EMPTY_STRING if self.objective else EMPTY_STRING,
            encounter_ids=[e.id for e in self.encounters if e.id is not None] if self.encounters else [],
        )


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

        sch = ChapterResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            era=EraResponse.from_model(era),
            name=model.name,
            description=model.description,
            objective=ObjectiveResponse.from_model(objective),
            encounters=[EncounterResponse.from_model(c) for c in encounters],
        )
        return sch


class EncounterPayload(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    chapter: Optional[ChapterPayload] = None
    name: Optional[str] = None
    description: Optional[str] = None
    actions: Optional[List['ActionPayload']] = None

    def to_model(self) -> Encounter:
        return Encounter(
            id=self.id or EMPTY_STRING,
            created_at=self.created_at or datetime.now(timezone.utc),
            updated_at=self.updated_at or datetime.now(timezone.utc),
            chapter_id=self.chapter.id or EMPTY_STRING if self.chapter else EMPTY_STRING,
            name=self.name or EMPTY_STRING,
            description=self.description,
            action_ids=[a.id for a in self.actions if a.id is not None] if self.actions else [],
        )


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

        sch = EncounterResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            chapter=ChapterResponse.from_model(chapter),
            name=model.name,
            description=model.description,
            actions=[ActionResponse.from_model(c) for c in actions],
        )
        return sch


# === Action & Events ===

class ActionPayload(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    encounter: Optional[EncounterPayload] = None
    owner_member: Optional[MemberPayload] = None
    character_object: Optional[ObjectPayload] = None
    content: Optional[str] = None
    type: Optional[str] = None
    dm_response: Optional[str] = None
    minigame: Optional['MinigameResultPayload'] = None

    def to_model(self) -> Action:
        return Action(
            id=self.id or EMPTY_STRING,
            created_at=self.created_at or datetime.now(timezone.utc),
            updated_at=self.updated_at or datetime.now(timezone.utc),
            encounter_id=self.encounter.id or EMPTY_STRING if self.encounter else EMPTY_STRING,
            owner_member_id=self.owner_member.id or EMPTY_STRING if self.owner_member else EMPTY_STRING,
            character_object_id=self.character_object.id or EMPTY_STRING if self.character_object else EMPTY_STRING,
            content=self.content or EMPTY_STRING,
            type=self.type or EMPTY_STRING,
            dm_response=self.dm_response,
            minigame_id=self.minigame.id or EMPTY_STRING if self.minigame else EMPTY_STRING,
        )


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

        sch = ActionResponse(
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
        return sch


class MinigameResultPayload(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    action: Optional[ActionPayload] = None
    type: Optional[str] = None
    result: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    completed_at: Optional[datetime] = None

    def to_model(self) -> MinigameResult:
        return MinigameResult(
            id=self.id or EMPTY_STRING,
            created_at=self.created_at or datetime.now(timezone.utc),
            updated_at=self.updated_at or datetime.now(timezone.utc),
            action_id=self.action.id or EMPTY_STRING if self.action else EMPTY_STRING,
            type=self.type or EMPTY_STRING,
            result=self.result or EMPTY_STRING,
            details=self.details or {},
            completed_at=self.completed_at or datetime.now(timezone.utc),
        )


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
        sch = MinigameResultResponse(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            action=ActionResponse.from_model(action),
            type=model.type,
            result=model.result,
            details=model.details,
            completed_at=model.completed_at,
        )
        return sch


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
