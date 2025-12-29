import json
from fastapi import APIRouter, Depends, HTTPException, status, Response, Header
from backend.database import REPO, fs
from backend.models import *
from typing import List

import os
from passlib.context import CryptContext
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer

from .routes_helper import changes_to_string
from identity_routes import get_current_user, get_current_member

# region === Config === ===
router = APIRouter()
#endregion

# region === Blueprint API === ===
@router.post("/blueprint/{owner_id}", response_model=Blueprint)
def blueprint_create(owner_id: str, payload: BlueprintPayload, current_user: User = Depends(get_current_user)):
    if not payload.name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name is required.")

    blueprint = Blueprint(
        name=payload.name,
        description=payload.description,
        blueprint_binding=payload.blueprint_binding,
        attributes=payload.attributes or [],
    )
    
    batch = fs.create_batch()

    if owner_id.startswith("WRL"):
        if not (world := REPO.WORLDS.get(owner_id)):
            raise HTTPException(status_code=404, detail="World not found.")
        world.blueprint_ids.append(blueprint.id)
        REPO.WORLDS.batch_update(batch, world)
    elif owner_id.startswith("CMP"):
        if not (campaign := REPO.CAMPAIGNS.get(owner_id)):
            raise HTTPException(status_code=404, detail="Campaign not found.")
        campaign.blueprint_ids.append(blueprint.id)
        REPO.CAMPAIGNS.batch_update(batch, campaign)

    REPO.BLUEPRINTS.batch_add(batch, blueprint)

    if fs.commit_batch(batch):
        return blueprint
    raise HTTPException(status_code=500, detail="Blueprint creation failed.")

@router.get("/blueprint/{blueprint_id}", response_model=Blueprint)
def blueprint_get(blueprint_id: str, current_user: User = Depends(get_current_user)):
    if (blueprint := REPO.BLUEPRINTS.get(blueprint_id)):
        return blueprint
    raise HTTPException(status_code=404, detail="Blueprint not found.")

@router.patch("/blueprint", response_model=Blueprint)
def blueprint_update(payload: BlueprintPayload, current_user: User = Depends(get_current_user)):
    if not payload.id or payload.id.strip() == "":
        raise HTTPException(status_code=400, detail="Blueprint ID is required in payload for update.")

    blueprint = REPO.BLUEPRINTS.get(payload.id)
    if not blueprint:
        raise HTTPException(status_code=404, detail="Blueprint not found.")
    

    updated_blueprint = payload.to_model(blueprint, preserve=True)

    if not (changes := blueprint.diff(updated_blueprint)):
        return blueprint

    batch = fs.create_batch()
    
    objects = blueprint.get_objects()

    for obj in objects:
        obj.normalize()
        REPO.OBJECTS.batch_update(batch, obj)

    REPO.BLUEPRINTS.batch_update(batch, updated_blueprint)

    if fs.commit_batch(batch):
        return updated_blueprint
    raise HTTPException(status_code=500, detail="Blueprint update failed.")

@router.delete("/blueprint/{blueprint_id}", response_model=bool)
def blueprint_delete(blueprint_id: str, current_user: User = Depends(get_current_user)):
    blueprint = REPO.BLUEPRINTS.get(blueprint_id)
    if not blueprint:
        raise HTTPException(status_code=404, detail="Blueprint not found.")
    
    batch = blueprint.delete(fs.create_batch())

    if fs.commit_batch(batch):
        return True
    raise HTTPException(status_code=500, detail="Blueprint deletion failed.")

# Blueprint-Specific APIs
@router.get("/blueprint/{blueprint_id}/owner", response_model=Campaign | World)
def blueprint_get_owner(blueprint_id: str, current_user: User = Depends(get_current_user)):
    blueprint = REPO.BLUEPRINTS.get(blueprint_id)
    if not blueprint:
        raise HTTPException(status_code=404, detail="Blueprint not found.")
    return blueprint.get_owner()

@router.get("/blueprint/{blueprint_id}/objects", response_model=List[Object])
def blueprint_get_objects(blueprint_id: str, current_user: User = Depends(get_current_user)):
    blueprint = REPO.BLUEPRINTS.get(blueprint_id)
    if not blueprint:
        raise HTTPException(status_code=404, detail="Blueprint not found.")
    return blueprint.get_objects()
# endregion

# region === Object API === ===
@router.post("/object/{owner_id}", response_model=Object)
def object_create(owner_id: str, payload: ObjectPayload, current_user: User = Depends(get_current_user)):
    if not payload.name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name is required.")

    if not payload.blueprint_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Blueprint ID is required.")

    object = Object(
        blueprint_id=payload.blueprint_id,
        name=payload.name,
        description=payload.description,
        blueprint_binding=payload.blueprint_binding,
        attributes=payload.attributes or [],
    )
    
    batch = fs.create_batch()

    if owner_id.startswith("WRL"):
        if not (world := REPO.WORLDS.get(owner_id)):
            raise HTTPException(status_code=404, detail="World not found.")
        world.object_ids.append(object.id)
        REPO.WORLDS.batch_update(batch, world)
    elif owner_id.startswith("CMP"):
        if not (campaign := REPO.CAMPAIGNS.get(owner_id)):
            raise HTTPException(status_code=404, detail="Campaign not found.")
        campaign.object_ids.append(object.id)
        REPO.CAMPAIGNS.batch_update(batch, campaign)

    REPO.OBJECTS.batch_add(batch, object)

    if fs.commit_batch(batch):
        return object
    raise HTTPException(status_code=500, detail="Object creation failed.")

@router.get("/object/{object_id}", response_model=Object)
def object_get(object_id: str, current_user: User = Depends(get_current_user)):
    if (object := REPO.OBJECTS.get(object_id)):
        return object
    raise HTTPException(status_code=404, detail="Object not found.")

@router.patch("/object", response_model=Object)
def object_update(payload: ObjectPayload, current_user: User = Depends(get_current_user)):
    if not payload.id or payload.id.strip() == "":
        raise HTTPException(status_code=400, detail="Object ID is required in payload for update.")

    object = REPO.OBJECTS.get(payload.id)
    if not object:
        raise HTTPException(status_code=404, detail="Object not found.")

    if payload.blueprint_id and object.blueprint_id != payload.blueprint_id:
        raise HTTPException(status_code=400, detail="Cannot change the blueprint_id of an existing object.")
    
    if payload.blueprint_binding and object.blueprint_binding != payload.blueprint_binding:
        raise HTTPException(status_code=400, detail="Cannot change the blueprint_binding of an existing object.")

    if payload.attributes and ({attr.name for attr in payload.attributes} == {attr.name for attr in object.attributes}):
        raise HTTPException(status_code=400, detail="Cannot change the attributes of an existing object.")

    updated_object = payload.to_model(object, preserve=True)

    if not (changes := object.diff(updated_object)):
        return object

    batch = fs.create_batch()

    REPO.OBJECTS.batch_update(batch, updated_object)

    if fs.commit_batch(batch):
        return updated_object
    raise HTTPException(status_code=500, detail="Object update failed.")

@router.delete("/object/{object_id}", response_model=bool)
def object_delete(object_id: str, current_user: User = Depends(get_current_user)):
    object = REPO.OBJECTS.get(object_id)
    if not object:
        raise HTTPException(status_code=404, detail="Object not found.")

    batch = object.delete(fs.create_batch())

    if fs.commit_batch(batch):
        return True
    raise HTTPException(status_code=500, detail="Object deletion failed.")

# Object-Specific APIs
@router.get("/object/{object_id}/owner", response_model=Campaign | World)
def object_get_owner(object_id: str, current_user: User = Depends(get_current_user)):
    object = REPO.OBJECTS.get(object_id)
    if not object:
        raise HTTPException(status_code=404, detail="Object not found.")
    return object.get_owner()

@router.get("/object/{object_id}/blueprints", response_model=Blueprint)
def object_get_blueprint(object_id: str, current_user: User = Depends(get_current_user)):
    object = REPO.OBJECTS.get(object_id)
    if not object:
        raise HTTPException(status_code=404, detail="Object not found.")
    return object.get_blueprint()
#endregion

# region === Context API === ===
@router.post("/context/{owner_id}", response_model=Context)
def context_create(owner_id: str, payload: ContextPayload, current_user: User = Depends(get_current_user)):
    if not payload.name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name is required.")

    if not payload.content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Content is required.")

    context = Context(
        name=payload.name,
        content=payload.content,
    )
    
    batch = fs.create_batch()

    if owner_id.startswith("WRL"):
        if not (world := REPO.WORLDS.get(owner_id)):
            raise HTTPException(status_code=404, detail="World not found.")
        world.context_ids.append(context.id)
        REPO.WORLDS.batch_update(batch, world)
    elif owner_id.startswith("CMP"):
        if not (campaign := REPO.CAMPAIGNS.get(owner_id)):
            raise HTTPException(status_code=404, detail="Campaign not found.")
        campaign.context_ids.append(context.id)
        REPO.CAMPAIGNS.batch_update(batch, campaign)

    REPO.CONTEXTS.batch_add(batch, context)

    if fs.commit_batch(batch):
        return context
    raise HTTPException(status_code=500, detail="Context creation failed.")

@router.get("/context/{context_id}", response_model=Context)
def context_get(context_id: str, current_user: User = Depends(get_current_user)):
    if (context := REPO.CONTEXTS.get(context_id)):
        return context
    raise HTTPException(status_code=404, detail="Context not found.")

@router.patch("/context", response_model=Context)
def context_update(payload: ContextPayload, current_user: User = Depends(get_current_user)):
    if not payload.id or payload.id.strip() == "":
        raise HTTPException(status_code=400, detail="Context ID is required in payload for update.")

    context = REPO.CONTEXTS.get(payload.id)
    if not context:
        raise HTTPException(status_code=404, detail="Context not found.")

    updated_context = payload.to_model(context, preserve=True)

    if not (changes := context.diff(updated_context)):
        return context

    batch = fs.create_batch()

    REPO.CONTEXTS.batch_update(batch, updated_context)

    if fs.commit_batch(batch):
        return updated_context
    raise HTTPException(status_code=500, detail="Context update failed.")

@router.delete("/context/{context_id}", response_model=bool)
def context_delete(context_id: str, current_user: User = Depends(get_current_user)):
    context = REPO.CONTEXTS.get(context_id)
    if not context:
        raise HTTPException(status_code=404, detail="Context not found.")

    batch = context.delete(fs.create_batch())

    if fs.commit_batch(batch):
        return True
    raise HTTPException(status_code=500, detail="Context deletion failed.")

# Context-Specific APIs
@router.get("/context/{context_id}/owner", response_model=Campaign | World)
def context_get_owner(context_id: str, current_user: User = Depends(get_current_user)):
    context = REPO.CONTEXTS.get(context_id)
    if not context:
        raise HTTPException(status_code=404, detail="Context not found.")
    return context.get_owner()
# endregion

# region === Quest API === ===
@router.post("/quest/{owner_id}", response_model=Quest)
def quest_create(owner_id: str, payload: QuestPayload, current_user: User = Depends(get_current_user)):
    if not payload.name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name is required.")

    if not payload.task: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task is required.")

    quest = Quest(
        name=payload.name,
        description=payload.description,
        task=payload.task,
        is_main=payload.is_main or False,
        is_active=payload.is_active or True,
        is_complete=payload.is_complete or False,
        parent_id=payload.parent_id,
        children_ids=payload.children_ids or [],
    )
    
    batch = fs.create_batch()

    if not (campaign := REPO.CAMPAIGNS.get(owner_id)):
        raise HTTPException(status_code=404, detail="Campaign not found.")
    campaign.quest_ids.append(quest.id)
    REPO.CAMPAIGNS.batch_update(batch, campaign)

    REPO.QUESTS.batch_add(batch, quest)

    if fs.commit_batch(batch):
        return quest
    raise HTTPException(status_code=500, detail="Quest creation failed.")

@router.get("/quest/{quest_id}", response_model=Quest)
def quest_get(quest_id: str, current_user: User = Depends(get_current_user)):
    if (quest := REPO.QUESTS.get(quest_id)):
        return quest
    raise HTTPException(status_code=404, detail="Quest not found.")

@router.patch("/quest", response_model=Quest)
def quest_update(payload: QuestPayload, current_user: User = Depends(get_current_user)):
    if not payload.id or payload.id.strip() == "":
        raise HTTPException(status_code=400, detail="Quest ID is required in payload for update.")

    quest = REPO.QUESTS.get(payload.id)
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found.")

    updated_quest = payload.to_model(quest, preserve=True)

    if not (changes := quest.diff(updated_quest)):
        return quest

    batch = fs.create_batch()

    REPO.QUESTS.batch_update(batch, updated_quest)

    if fs.commit_batch(batch):
        return updated_quest
    raise HTTPException(status_code=500, detail="Quest update failed.")

@router.delete("/quest/{quest_id}", response_model=bool)
def quest_delete(quest_id: str, current_user: User = Depends(get_current_user)):
    quest = REPO.QUESTS.get(quest_id)
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found.")

    batch = quest.delete(fs.create_batch())

    if fs.commit_batch(batch):
        return True
    raise HTTPException(status_code=500, detail="Quest deletion failed.")

# Quest-Specific APIs
@router.get("/quest/{quest_id}/owner", response_model=Campaign | World)
def quest_get_owner(quest_id: str, current_user: User = Depends(get_current_user)):
    quest = REPO.QUESTS.get(quest_id)
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found.")
    return quest.get_owner()
# endregion

