from datetime import datetime, timezone
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from .models import *

# === Config ===
EMPTY_STRING = ""
UNKNOWN = "Unknown"
UNNAMED = "Unnamed"

# === === Responses === ===

# === User (Protected) ===
class UserProtected(BaseDocument):
    username: str
    email: EmailStr
    member_ids: List[str] = Field(default_factory=list)
    world_ids: List[str] = Field(default_factory=list)
    campaign_ids: List[str] = Field(default_factory=list)

    @staticmethod
    def from_model(model: User) -> 'UserProtected':
        
        schema = UserProtected(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            username=model.username or UNKNOWN,
            email=model.email,
            member_ids=model.member_ids or [],
            world_ids=model.world_ids or [],
            campaign_ids=model.campaign_ids or []
        )
        return schema

# === === Base === ===
class BasePayload(BaseModel):
    id: Optional[str] = None

# === === Identification Payloads === ===
class UserPayload(BasePayload):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password_current: Optional[str] = None
    password_new: Optional[str] = None
    member_ids: Optional[List[str]] = None
    world_ids: Optional[List[str]] = None
    campaign_ids: Optional[List[str]] = None

    def to_model(self, model: User, preserve: bool) -> User:
        update_data = self.model_dump(exclude_unset=True)
        if preserve:
            updated_model = model.model_copy(deep=True)
            for field, value in update_data.items():
                setattr(updated_model, field, value)
            return updated_model
        else:
            for field, value in update_data.items():
                setattr(model, field, value)
            return model

class MemberPayload(BasePayload):
    user_id: Optional[str] = None
    campaign_id: Optional[str] = None
    is_admin: Optional[bool] = None
    is_dm: Optional[bool] = None
    is_active: Optional[bool] = None
    character_id: Optional[str] = None
    equipped_ids: Optional[List[str]] = None
    inventory_ids: Optional[List[str]] = None

    def to_model(self, model: 'Member', preserve: bool) -> 'Member':
        update_data = self.model_dump(exclude_unset=True)
        if preserve:
            updated = model.model_copy(deep=True)
            for k, v in update_data.items():
                setattr(updated, k, v)
            return updated
        else:
            for k, v in update_data.items():
                setattr(model, k, v)
            return model

# === Game Setting Payloads ===
class WorldPayload(BasePayload):
    name: Optional[str] = None
    description: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None
    blueprint_ids: Optional[List[str]] = None
    object_ids: Optional[List[str]] = None
    context_ids: Optional[List[str]] = None

    def to_model(self, model: 'World', preserve: bool) -> 'World':
        update_data = self.model_dump(exclude_unset=True)
        if preserve:
            updated = model.model_copy(deep=True)
            for k, v in update_data.items():
                setattr(updated, k, v)
            return updated
        else:
            for k, v in update_data.items():
                setattr(model, k, v)
            return model

class CampaignPayload(BasePayload):
    world_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None
    member_ids: Optional[List[str]] = None
    blueprint_ids: Optional[List[str]] = None
    object_ids: Optional[List[str]] = None
    context_ids: Optional[List[str]] = None
    quest_ids: Optional[List[str]] = None

    def to_model(self, model: 'Campaign', preserve: bool) -> 'Campaign':
        update_data = self.model_dump(exclude_unset=True)
        if preserve:
            updated = model.model_copy(deep=True)
            for k, v in update_data.items():
                setattr(updated, k, v)
            return updated
        else:
            for k, v in update_data.items():
                setattr(model, k, v)
            return model

# === Content Payloads ===
class BlueprintPayload(BasePayload):
    name: Optional[str] = None
    description: Optional[str] = None
    blueprint_binding: Optional[BlueprintBinding] = None
    attributes: Optional[List[Attribute]] = None

    def to_model(self, model: 'Blueprint', preserve: bool) -> 'Blueprint':
        update_data = self.model_dump(exclude_unset=True)
        if preserve:
            updated = model.model_copy(deep=True)
            for k, v in update_data.items():
                setattr(updated, k, v)
            return updated
        else:
            for k, v in update_data.items():
                setattr(model, k, v)
            return model

class ObjectPayload(BasePayload):
    blueprint_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    blueprint_binding: Optional[BlueprintBinding] = None
    attributes: Optional[List[Attribute]] = None

    def to_model(self, model: 'Object', preserve: bool) -> 'Object':
        update_data = self.model_dump(exclude_unset=True)
        if preserve:
            updated = model.model_copy(deep=True)
            for k, v in update_data.items():
                setattr(updated, k, v)
            return updated
        else:
            for k, v in update_data.items():
                setattr(model, k, v)
            return model

class ContextPayload(BasePayload):
    name: Optional[str] = None
    content: Optional[str] = None

    def to_model(self, model: 'Context', preserve: bool) -> 'Context':
        update_data = self.model_dump(exclude_unset=True)
        if preserve:
            updated = model.model_copy(deep=True)
            for k, v in update_data.items():
                setattr(updated, k, v)
            return updated
        else:
            for k, v in update_data.items():
                setattr(model, k, v)
            return model

class QuestPayload(BasePayload):
    name: Optional[str] = None
    description: Optional[str] = None
    task: Optional[str] = None
    is_main: Optional[bool] = None
    is_active: Optional[bool] = None
    is_complete: Optional[bool] = None
    parent_id: Optional[str] = None
    children_ids: Optional[List[str]] = None

    def to_model(self, model: 'Quest', preserve: bool) -> 'Quest':
        update_data = self.model_dump(exclude_unset=True)
        if preserve:
            updated = model.model_copy(deep=True)
            for k, v in update_data.items():
                setattr(updated, k, v)
            return updated
        else:
            for k, v in update_data.items():
                setattr(model, k, v)
            return model

# === === Timeline Payloads === ===

class ScenePayload(BasePayload):
    campaign_id: Optional[str] = None
    encounter_id: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    actions: Optional[List[Action]] = None
    minute_time: Optional[int] = None

    def to_model(self, model: 'Scene', preserve: bool) -> 'Scene':
        update_data = self.model_dump(exclude_unset=True)
        if preserve:
            updated = model.model_copy(deep=True)
            for k, v in update_data.items():
                setattr(updated, k, v)
            return updated
        else:
            for k, v in update_data.items():
                setattr(model, k, v)
            return model

class EncounterPayload(BasePayload):
    campaign_id: Optional[str] = None
    chapter_id: Optional[str] = None
    type: Optional[str] = None
    goal: Optional[str] = None
    length: Optional[int] = None
    scene_ids: Optional[List[str]] = None

    def to_model(self, model: 'Encounter', preserve: bool) -> 'Encounter':
        update_data = self.model_dump(exclude_unset=True)
        if preserve:
            updated = model.model_copy(deep=True)
            for k, v in update_data.items():
                setattr(updated, k, v)
            return updated
        else:
            for k, v in update_data.items():
                setattr(model, k, v)
            return model

class ChapterPayload(BasePayload):
    campaign_id: Optional[str] = None
    description: Optional[str] = None
    encounter_ids: Optional[List[str]] = None

    def to_model(self, model: 'Chapter', preserve: bool) -> 'Chapter':
        update_data = self.model_dump(exclude_unset=True)
        if preserve:
            updated = model.model_copy(deep=True)
            for k, v in update_data.items():
                setattr(updated, k, v)
            return updated
        else:
            for k, v in update_data.items():
                setattr(model, k, v)
            return model

# === === Pydantic Model Rebuilds === ===
UserProtected.model_rebuild()

UserPayload.model_rebuild()
MemberPayload.model_rebuild()
WorldPayload.model_rebuild()
CampaignPayload.model_rebuild()
BlueprintPayload.model_rebuild()
ObjectPayload.model_rebuild()
ContextPayload.model_rebuild()
QuestPayload.model_rebuild()
ScenePayload.model_rebuild()
EncounterPayload.model_rebuild()
ChapterPayload.model_rebuild()

