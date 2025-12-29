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

# region === World API === ===
@router.post("/world", response_model=World)
def world_create(payload: WorldPayload, current_user: User = Depends(get_current_user)):
    if not payload.name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name is required.")

    world = World(
        name=payload.name,
        description=payload.description,
        settings=payload.settings or {},
        blueprint_ids=payload.blueprint_ids or [],
        object_ids=payload.object_ids or [],
        context_ids=payload.context_ids or [],
    )

    current_user.world_ids.append(world.id)

    batch = fs.create_batch()

    REPO.WORLDS.batch_add(batch, world)
    REPO.USERS.batch_update(batch, current_user)

    if fs.commit_batch(batch):
        return world
    raise HTTPException(status_code=500, detail="World creation failed.")

@router.get("/world/{world_id}", response_model=World)
def world_get(world_id: str, current_user: User = Depends(get_current_user)):
    if (world := REPO.WORLDS.get(world_id)):
        return world
    raise HTTPException(status_code=404, detail="World not found.")

@router.patch("/world", response_model=World)
def world_update(payload: WorldPayload, current_user: User = Depends(get_current_user)):
    if not payload.id or payload.id.strip() == "":
        raise HTTPException(status_code=400, detail="World ID is required in payload for update.")

    world = REPO.WORLDS.get(payload.id)
    if not world:
        raise HTTPException(status_code=404, detail="World not found.")
    
    if not (world.id in current_user.world_ids):
        raise HTTPException(status_code=403, detail="You do not have permission to update this world.")

    updated_world = payload.to_model(world, preserve=True)

    if not (changes := world.diff(updated_world)):
        return world

    if (updated_world := REPO.WORLDS.update(updated_world)):
        return updated_world
    raise HTTPException(status_code=500, detail="World update failed.")

@router.delete("/world/{world_id}", response_model=bool)
def world_delete(world_id: str, current_user: User = Depends(get_current_user)):
    world = REPO.WORLDS.get(world_id)
    if not world:
        raise HTTPException(status_code=404, detail="World not found.")

    if not (world.id in current_user.world_ids):
        raise HTTPException(status_code=403, detail="You do not have permission to delete this world.")

    batch = world.delete(fs.create_batch())

    if fs.commit_batch(batch):
        return True
    raise HTTPException(status_code=500, detail="World deletion failed.")

# World-Specific APIs
@router.get("/world/{world_id}/blueprints", response_model=List[Blueprint])
def world_get_blueprints(world_id: str, current_user: User = Depends(get_current_user)):
    world = REPO.WORLDS.get(world_id)
    if not world:
        raise HTTPException(status_code=404, detail="World not found.")

    return world.get_blueprints()

@router.get("/world/{world_id}/objects", response_model=List[Object])
def world_get_objects(world_id: str, current_user: User = Depends(get_current_user)):
    world = REPO.WORLDS.get(world_id)
    if not world:
        raise HTTPException(status_code=404, detail="World not found.")

    return world.get_objects()

@router.get("/world/{world_id}/contexts", response_model=List[Context])
def world_get_contexts(world_id: str, current_user: User = Depends(get_current_user)):
    world = REPO.WORLDS.get(world_id)
    if not world:
        raise HTTPException(status_code=404, detail="World not found.")

    return world.get_contexts()
# endregion

# region === Campaign API === ===
@router.post("/campaign", response_model=Campaign)
def campaign_create(payload: CampaignPayload, current_user: User = Depends(get_current_user)):
    if not payload.name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name is required.")
    
    if payload.world_id:
        if not (world := REPO.WORLDS.get(payload.world_id)):
            raise HTTPException(status_code=404, detail="World not found.")
        
        campaign = world.to_campaign()

    else:
        campaign = Campaign(
            name=payload.name,
            description=payload.description,
            settings=payload.settings or {},
            member_ids=[],
            blueprint_ids=[],
            object_ids=[],
            context_ids=[],
            quest_ids=[],
        )

    member = Member(
        user_id=current_user.id,
        campaign_id=campaign.id,
        is_admin=True,
        is_dm=False,
        is_active=True,
        character_id=None,
        equipped_ids=[],
        inventory_ids=[],
    )

    current_user.campaign_ids.append(campaign.id)
    campaign.member_ids.append(member.id)

    batch = fs.create_batch()

    REPO.CAMPAIGNS.batch_add(batch, campaign)
    REPO.MEMBERS.batch_add(batch, member)
    REPO.USERS.batch_update(batch, current_user)
    
    if fs.commit_batch(batch):
        return campaign
    raise HTTPException(status_code=500, detail="Campaign creation failed.")

@router.get("/campaign/{campaign_id}", response_model=Campaign)
def campaign_get(campaign_id: str, current_user: User = Depends(get_current_user)):
    campaign = REPO.CAMPAIGNS.get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found.")

    if not (current_member := get_current_member(current_user, campaign.id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    return campaign

@router.patch("/campaign/{campaign_id}", response_model=Campaign)
def campaign_update(campaign_id: str, payload: CampaignPayload, current_user: User = Depends(get_current_user)):
    campaign = REPO.CAMPAIGNS.get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found.")

    if not (current_member := get_current_member(current_user, campaign.id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    if not current_member.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can update campaigns.")

    updated_campaign = payload.to_model(campaign, preserve=True)

    if not (changes := campaign.diff(updated_campaign)):
        return campaign

    batch = fs.create_batch()

    REPO.CAMPAIGNS.batch_update(batch, updated_campaign)

    if fs.commit_batch(batch):
        return updated_campaign
    raise HTTPException(status_code=500, detail="Campaign update failed.")

@router.delete("/campaign/{campaign_id}", response_model=bool)
def campaign_delete(campaign_id: str, current_user: User = Depends(get_current_user)):
    campaign = REPO.CAMPAIGNS.get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found.")

    current_member = get_current_member(current_user, campaign.id)
    if not current_member:
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    if not current_member.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can delete campaigns.")

    batch = campaign.delete(fs.create_batch())

    if fs.commit_batch(batch):
        return True
    raise HTTPException(status_code=500, detail="Campaign deletion failed.")

# Campaign-Specific APIs
@router.get("/campaign/{campaign_id}/world", response_model=World)
def campaign_get_world(campaign_id: str, current_user: User = Depends(get_current_user)):
    campaign = REPO.CAMPAIGNS.get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found.")

    if not (current_member := get_current_member(current_user, campaign.id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    return campaign.get_world()

@router.get("/campaign/{campaign_id}/members", response_model=List[Member])
def campaign_get_members(campaign_id: str, current_user: User = Depends(get_current_user)):
    campaign = REPO.CAMPAIGNS.get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found.")

    if not (current_member := get_current_member(current_user, campaign.id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    return campaign.get_members()

@router.get("/campaign/{campaign_id}/blueprints", response_model=List[Blueprint])
def campaign_get_blueprints(campaign_id: str, current_user: User = Depends(get_current_user)):
    campaign = REPO.CAMPAIGNS.get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found.")

    if not (current_member := get_current_member(current_user, campaign.id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    return campaign.get_blueprints()

@router.get("/campaign/{campaign_id}/objects", response_model=List[Object])
def campaign_get_objects(campaign_id: str, current_user: User = Depends(get_current_user)):
    campaign = REPO.CAMPAIGNS.get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found.")

    if not (current_member := get_current_member(current_user, campaign.id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    return campaign.get_objects()

@router.get("/campaign/{campaign_id}/contexts", response_model=List[Context])
def campaign_get_contexts(campaign_id: str, current_user: User = Depends(get_current_user)):
    campaign = REPO.CAMPAIGNS.get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found.")

    if not (current_member := get_current_member(current_user, campaign.id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    return campaign.get_contexts()

@router.get("/campaign/{campaign_id}/quests", response_model=List[Quest])
def campaign_get_quests(campaign_id: str, current_user: User = Depends(get_current_user)):
    campaign = REPO.CAMPAIGNS.get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found.")

    if not (current_member := get_current_member(current_user, campaign.id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    return campaign.get_quests()
# endregion
