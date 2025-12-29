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

# region === Scene API === ===
@router.post("/scene", response_model=Scene)
def scene_create(payload: ScenePayload, current_user: User = Depends(get_current_user)):
    if not payload.campaign_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Campaign ID is required.")

    if not payload.encounter_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Encounter ID is required.")

    if not (encounter := REPO.ENCOUNTERS.get(payload.encounter_id)):
        raise HTTPException(status_code=404, detail="Encounter not found.")

    scene = Scene(
        campaign_id=payload.campaign_id,
        encounter_id=payload.encounter_id,
        content=payload.content or "",
        summary=payload.summary,
        actions=payload.actions or [],
        minute_time=payload.minute_time or 0,
    )

    encounter.scene_ids.append(scene.id)

    batch = fs.create_batch()

    REPO.SCENES.batch_add(batch, scene)
    REPO.ENCOUNTERS.batch_update(batch, encounter)

    if fs.commit_batch(batch):
        return scene
    raise HTTPException(status_code=500, detail="Scene creation failed.")

@router.get("/scene/{scene_id}", response_model=Scene)
def scene_get(scene_id: str, current_user: User = Depends(get_current_user)):
    if (scene := REPO.SCENES.get(scene_id)):
        return scene
    raise HTTPException(status_code=404, detail="Scene not found.")

@router.patch("/scene", response_model=Scene)
def scene_update(payload: ScenePayload, current_user: User = Depends(get_current_user)):
    if not payload.id or payload.id.strip() == "":
        raise HTTPException(status_code=400, detail="Scene ID is required in payload for update.")

    if not (scene := REPO.SCENES.get(payload.id)):
        raise HTTPException(status_code=404, detail="Scene not found.")

    if not payload.campaign_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Campaign ID is required.")

    if not (current_member := get_current_member(current_user, payload.campaign_id)):
        raise HTTPException(status_code=403, detail="You do not have permission to update this scene.")
    
    if not current_member.is_admin or not current_member.is_dm:
        raise HTTPException(status_code=403, detail="Only admins can update scenes.")

    if not (encounter := REPO.ENCOUNTERS.get(scene.encounter_id)):
        raise HTTPException(status_code=404, detail="Encounter not found.")
    
    updated_scene = payload.to_model(scene, preserve=True)

    if not (changes := scene.diff(updated_scene)):
        return scene
    
    batch = fs.create_batch()

    REPO.SCENES.batch_update(batch, updated_scene)
    REPO.ENCOUNTERS.batch_update(batch, encounter)

    if fs.commit_batch(batch):
        return updated_scene
    raise HTTPException(status_code=500, detail="Scene update failed.")

@router.delete("/scene/{scene_id}", response_model=bool)
def scene_delete(scene_id: str, current_user: User = Depends(get_current_user)):
    scene = REPO.SCENES.get(scene_id)
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found.")

    if not (encounter := REPO.ENCOUNTERS.get(scene.encounter_id)):
        raise HTTPException(status_code=404, detail="Encounter not found.")

    if not (current_member := get_current_member(current_user, encounter.campaign_id)):
        raise HTTPException(status_code=403, detail="You do not have permission to delete this scene.")

    batch = fs.create_batch()

    scene.delete(batch)

    if fs.commit_batch(batch):
        return True
    raise HTTPException(status_code=500, detail="Scene deletion failed.")

# Scene-Specific APIs
@router.get("/scene/{scene_id}/campaign", response_model=Campaign)
def scene_get_campaign(scene_id: str, current_user: User = Depends(get_current_user)):
    scene = REPO.SCENES.get(scene_id)
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found.")

    return scene.get_campaign()

@router.get("/scene/{scene_id}/encounter", response_model=Encounter)
def scene_get_encounter(scene_id: str, current_user: User = Depends(get_current_user)):
    scene = REPO.SCENES.get(scene_id)
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found.")

    return scene.get_encounter()
# endregion

# region === Encounter API === ===
@router.post("/encounter", response_model=Encounter)
def encounter_create(payload: EncounterPayload, current_user: User = Depends(get_current_user)):
    if not payload.campaign_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Campaign ID is required.")

    if not payload.chapter_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Chapter ID is required.")

    if not payload.type or payload.type.strip() == "":
        raise HTTPException(status_code=400, detail="Encounter type is required.")

    if not payload.goal or payload.goal.strip() == "":
        raise HTTPException(status_code=400, detail="Encounter goal is required.")

    if not payload.length or payload.length <= 0:
        raise HTTPException(status_code=400, detail="Encounter length must be positive.")

    if not (current_member := get_current_member(current_user, payload.campaign_id)):
        raise HTTPException(status_code=403, detail="You do not have permission to create an encounter in this campaign.")
    
    if not current_member.is_admin or not current_member.is_dm:
        raise HTTPException(status_code=403, detail="Only admins can create encounters.")
    
    if not (chapter := REPO.CHAPTERS.get(payload.chapter_id)):
        raise HTTPException(status_code=404, detail="Chapter not found.")

    encounter = Encounter(
        campaign_id=payload.campaign_id,
        chapter_id=payload.chapter_id,
        type=payload.type,
        goal=payload.goal,
        length=payload.length,
        scene_ids=payload.scene_ids or [],
    )
    

    batch = fs.create_batch()

    chapter.encounter_ids.append(encounter.id)

    REPO.CHAPTERS.batch_update(batch, chapter)
    REPO.ENCOUNTERS.batch_add(batch, encounter)

    if fs.commit_batch(batch):
        return encounter
    raise HTTPException(status_code=500, detail="Encounter creation failed.")

@router.get("/encounter/{encounter_id}", response_model=Encounter)
def encounter_get(encounter_id: str, current_user: User = Depends(get_current_user)):
    encounter = REPO.ENCOUNTERS.get(encounter_id)
    if not encounter:
        raise HTTPException(status_code=404, detail="Encounter not found.")

    if not (current_member := get_current_member(current_user, encounter.campaign_id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    return encounter

@router.patch("/encounter/{encounter_id}", response_model=Encounter)
def encounter_update(encounter_id: str, payload: EncounterPayload, current_user: User = Depends(get_current_user)):
    encounter = REPO.ENCOUNTERS.get(encounter_id)
    if not encounter:
        raise HTTPException(status_code=404, detail="Encounter not found.")

    if not (current_member := get_current_member(current_user, encounter.campaign_id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    if not current_member.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can update encounters.")

    updated_encounter = payload.to_model(encounter, preserve=True)

    if not (changes := encounter.diff(updated_encounter)):
        return encounter

    batch = fs.create_batch()

    REPO.ENCOUNTERS.batch_update(batch, updated_encounter)

    if fs.commit_batch(batch):
        return updated_encounter
    raise HTTPException(status_code=500, detail="Encounter update failed.")

@router.delete("/encounter/{encounter_id}", response_model=bool)
def encounter_delete(encounter_id: str, current_user: User = Depends(get_current_user)):
    encounter = REPO.ENCOUNTERS.get(encounter_id)
    if not encounter:
        raise HTTPException(status_code=404, detail="Encounter not found.")

    current_member = get_current_member(current_user, encounter.campaign_id)
    if not current_member:
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    if not current_member.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can delete encounters.")

    batch = encounter.delete(fs.create_batch())

    if fs.commit_batch(batch):
        return True
    raise HTTPException(status_code=500, detail="Encounter deletion failed.")

# Encounter-Specific APIs
@router.get("/encounter/{encounter_id}/campaign", response_model=Campaign)
def encounter_get_campaign(encounter_id: str, current_user: User = Depends(get_current_user)):
    encounter = REPO.ENCOUNTERS.get(encounter_id)
    if not encounter:
        raise HTTPException(status_code=404, detail="Encounter not found.")

    if not (current_member := get_current_member(current_user, encounter.campaign_id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    return encounter.get_campaign()

@router.get("/encounter/{encounter_id}/chapter", response_model=Chapter)
def encounter_get_chapters(encounter_id: str, current_user: User = Depends(get_current_user)):
    encounter = REPO.ENCOUNTERS.get(encounter_id)
    if not encounter:
        raise HTTPException(status_code=404, detail="Encounter not found.")

    if not (current_member := get_current_member(current_user, encounter.campaign_id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    return encounter.get_chapter()

@router.get("/encounter/{encounter_id}/scenes", response_model=List[Scene])
def encounter_get_scenes(encounter_id: str, current_user: User = Depends(get_current_user)):
    encounter = REPO.ENCOUNTERS.get(encounter_id)
    if not encounter:
        raise HTTPException(status_code=404, detail="Encounter not found.")

    if not (current_member := get_current_member(current_user, encounter.campaign_id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    return encounter.get_scenes()
# endregion

# region === Chapter API === ===
@router.post("/chapter", response_model=Chapter)
def chapter_create(payload: ChapterPayload, current_user: User = Depends(get_current_user)):
    if not payload.campaign_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Campaign ID is required.")
    
    if not (current_member := get_current_member(current_user, payload.campaign_id)):
        raise HTTPException(status_code=403, detail="You do not have permission to create a chapter in this campaign.")

    if not current_member.is_admin or not current_member.is_dm:
        raise HTTPException(status_code=403, detail="Only admins can create chapters.")

    chapter = Chapter(
        campaign_id=payload.campaign_id,
        description=payload.description or "",
        encounter_ids=payload.encounter_ids or [],
    )
    

    batch = fs.create_batch()

    REPO.CHAPTERS.batch_update(batch, chapter)

    if fs.commit_batch(batch):
        return chapter
    raise HTTPException(status_code=500, detail="Chapter creation failed.")

@router.get("/chapter/{chapter_id}", response_model=Chapter)
def chapter_get(chapter_id: str, current_user: User = Depends(get_current_user)):
    chapter = REPO.CHAPTERS.get(chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found.")

    if not (current_member := get_current_member(current_user, chapter.campaign_id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    return chapter

@router.patch("/chapter/{chapter_id}", response_model=Chapter)
def chapter_update(chapter_id: str, payload: ChapterPayload, current_user: User = Depends(get_current_user)):
    chapter = REPO.CHAPTERS.get(chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found.")

    if not (current_member := get_current_member(current_user, chapter.campaign_id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    if not current_member.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can update chapters.")

    payload.campaign_id = chapter.campaign_id

    updated_chapter = payload.to_model(chapter, preserve=True)

    if not (changes := chapter.diff(updated_chapter)):
        return chapter

    batch = fs.create_batch()

    REPO.CHAPTERS.batch_update(batch, updated_chapter)

    if fs.commit_batch(batch):
        return updated_chapter
    raise HTTPException(status_code=500, detail="Chapter update failed.")

@router.delete("/chapter/{chapter_id}", response_model=bool)
def chapter_delete(chapter_id: str, current_user: User = Depends(get_current_user)):
    chapter = REPO.CHAPTERS.get(chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found.")

    current_member = get_current_member(current_user, chapter.campaign_id)
    if not current_member:
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    if not current_member.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can delete chapters.")

    batch = chapter.delete(fs.create_batch())

    if fs.commit_batch(batch):
        return True
    raise HTTPException(status_code=500, detail="Chapter deletion failed.")

# Chapter-Specific APIs
@router.get("/chapter/{chapter_id}/campaign", response_model=Campaign)
def chapter_get_campaign(chapter_id: str, current_user: User = Depends(get_current_user)):
    chapter = REPO.CHAPTERS.get(chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found.")

    if not (current_member := get_current_member(current_user, chapter.campaign_id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    return chapter.get_campaign()

@router.get("/chapter/{chapter_id}/encounters", response_model=List[Encounter])
def chapter_get_encounters(chapter_id: str, current_user: User = Depends(get_current_user)):
    chapter = REPO.CHAPTERS.get(chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found.")

    if not (current_member := get_current_member(current_user, chapter.campaign_id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    return chapter.get_encounters()

@router.get("/chapter/{chapter_id}/scenes", response_model=List[Scene])
def chapter_get_scenes(chapter_id: str, current_user: User = Depends(get_current_user)):
    chapter = REPO.CHAPTERS.get(chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found.")

    if not (current_member := get_current_member(current_user, chapter.campaign_id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    return chapter.get_scenes()
# endregion