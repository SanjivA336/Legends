import uuid
from fastapi import APIRouter, Depends, HTTPException
from backend.routes.auth_routes import get_current_user
from backend.database.repos import worlds_repo, campaigns_repo, blueprints_repo, context_repo, objects_repo
from backend.models import User, World, WorldSetting, Blueprint, Context, Object
from backend.routes._schemas import ContextResponse, ContextPayload, ObjectResponse, WorldPayload, WorldResponse, BlueprintResponse, BlueprintPayload, ObjectPayload, ObjectResponse

# === Config ===
router = APIRouter()

# === Defaults ===
DefaultWorld = World(
    name="My World",
    description="This world was created by the user.",
    creator_id="None",
    settings=WorldSetting(
        is_public=False,
    )
)

DefaultBlueprint = Blueprint(
    name="My Blueprint",
    description="This blueprint was created by the user.",
    creator_id="None",
    fields=[]
)

DefaultContext = Context(
    name="New Context",
    content="",
)

DefaultObject = Object(
    name="New Object",
    description="",
    creator_id="None",
    fields=[],
    blueprint_id="74b6c915777f48c59ab52e8a06ef1a3d" # Developer's Player Class
)

# === Helper Functions ===


# === World Endpoints ===
@router.get("/worlds", response_model=list[WorldResponse])
def all_worlds(current_user: User = Depends(get_current_user)):
    worlds = worlds_repo.query([('creator_id', '==', current_user.id)])
    return [WorldResponse.from_model(world) for world in worlds]

@router.get("/world/{id}", response_model=WorldResponse)
def world_get(id: str, current_user: User = Depends(get_current_user)):
    if id == "new":
        world = DefaultWorld.model_copy(deep=True)
        
        world.creator_id = current_user.id
        
        return WorldResponse.from_model(world)
    else:
        world = worlds_repo.get(id)
        
        if not world:
            raise HTTPException(status_code=404, detail="World not found")
        
        if world.creator_id != current_user.id:
            raise HTTPException(status_code=403, detail="You do not have permission to access this world")

        return WorldResponse.from_model(world)

@router.post("/world/{id}", response_model=WorldResponse)
def world_post(id: str, payload: WorldPayload, current_user: User = Depends(get_current_user)):    
    if id == "new":
        world = payload.to_model(DefaultWorld.model_copy(deep=True))
        
        world.creator_id = current_user.id
        
        if not worlds_repo.add(world):
            raise HTTPException(status_code=400, detail="Failed to create world")
    else:
        world = worlds_repo.get(id)
        
        if not world:
            raise HTTPException(status_code=404, detail="World not found")
        
        if world.creator_id != current_user.id:
            raise HTTPException(status_code=403, detail="You do not have permission to update this world")

        world = payload.to_model(world)
        
        if not worlds_repo.update(world):
            raise HTTPException(status_code=400, detail="Failed to update world")

    return WorldResponse.from_model(world)

# === Blueprint Endpoints ===
@router.get("/blueprints", response_model=list[BlueprintResponse])
def all_blueprints(current_user: User = Depends(get_current_user)):
    blueprints = blueprints_repo.query([('creator_id', '==', current_user.id)])
    return [BlueprintResponse.from_model(bp) for bp in blueprints]

@router.get("/blueprint/{id}", response_model=BlueprintResponse)
def blueprint_get(id: str, current_user: User = Depends(get_current_user)):
    if id == "new":
        blueprint = DefaultBlueprint.model_copy(deep=True)
        blueprint.creator_id = current_user.id
        return BlueprintResponse.from_model(blueprint)
    else:
        blueprint = blueprints_repo.get(id)
        if not blueprint:
            raise HTTPException(status_code=404, detail="Blueprint not found")
        if blueprint.creator_id != current_user.id:
            raise HTTPException(status_code=403, detail="You do not have permission to access this blueprint")
        
        return BlueprintResponse.from_model(blueprint)

@router.post("/blueprint/{id}", response_model=BlueprintResponse)
def blueprint_post(id: str, payload: BlueprintPayload, current_user: User = Depends(get_current_user)):
    if id == "new":
        blueprint = payload.to_model(DefaultBlueprint.model_copy(deep=True))
        blueprint.creator_id = current_user.id
        if not blueprints_repo.add(blueprint):
            raise HTTPException(status_code=400, detail="Failed to create blueprint")
    else:
        blueprint = blueprints_repo.get(id)
        if not blueprint:
            raise HTTPException(status_code=404, detail="Blueprint not found")
        if blueprint.creator_id != current_user.id:
            raise HTTPException(status_code=403, detail="You do not have permission to update this blueprint")
        
        blueprint = payload.to_model(blueprint)
        if not blueprints_repo.update(blueprint):
            raise HTTPException(status_code=400, detail="Failed to update blueprint")

    return BlueprintResponse.from_model(blueprint)

@router.get("/blueprint/{id}/delete", response_model=None)
def blueprint_delete(id: str, current_user: User = Depends(get_current_user)):
    # Step 1: Validate blueprint existence and ownership
    blueprint = blueprints_repo.get(id)
    if not blueprint:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    if blueprint.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this blueprint")

    # Step 2: Remove blueprint from all worlds
    worlds = worlds_repo.query([("blueprint_ids", "array-contains", id)])
    for world in worlds:
        world.blueprint_ids = [b for b in world.blueprint_ids if b != id]
        worlds_repo.update(world)

    # Step 3: Remove blueprint from all campaigns (if campaigns also reference blueprint IDs)
    campaigns = campaigns_repo.query([("blueprint_ids", "array-contains", id)])
    for campaign in campaigns:
        campaign.blueprint_ids = [b for b in campaign.blueprint_ids if b != id]
        campaigns_repo.update(campaign)

    # Step 4: Delete all objects tied to this blueprint
    objects = objects_repo.query([("blueprint_id", "==", id)])
    for obj in objects:
        objects_repo.delete(obj.id)

    # Step 5: Delete the blueprint itself
    if not blueprints_repo.delete(id):
        raise HTTPException(status_code=400, detail="Failed to delete blueprint")

    return None

@router.get("/context/{id}", response_model=ContextResponse)
def context_get(id: str, current_user: User = Depends(get_current_user)):
    if id == "new":
        context = DefaultContext.model_copy(deep=True)
        return ContextResponse.from_model(context)
    else:
        context = context_repo.get(id)
        if not context:
            raise HTTPException(status_code=404, detail="Context not found")
        
        return ContextResponse.from_model(context)

@router.post("/context/{id}", response_model=ContextResponse)
def context_post(id: str, payload: ContextPayload, current_user: User = Depends(get_current_user)):
    if id == "new":
        context = payload.to_model(DefaultContext.model_copy(deep=True))
        if not context_repo.add(context):
            raise HTTPException(status_code=400, detail="Failed to create context")
    else:
        context = context_repo.get(id)
        if not context:
            raise HTTPException(status_code=404, detail="Context not found")

        context = payload.to_model(context)
        if not context_repo.update(context):
            raise HTTPException(status_code=400, detail="Failed to update context")

    return ContextResponse.from_model(context)

@router.post("/context/{id}/delete")
def context_delete(id: str, current_user: User = Depends(get_current_user)):
    context = context_repo.get(id)
    if not context:
        return None
    
    

    if not context_repo.delete(id):
        raise HTTPException(status_code=400, detail="Failed to delete context")

    return None

@router.get("/object/{id}", response_model=ObjectResponse)
def object_get(id: str, current_user: User = Depends(get_current_user)):
    if id == "new":
        object = DefaultObject.model_copy(deep=True)
        object.creator_id = current_user.id
        object.id = uuid.uuid4().hex
        return ObjectResponse.from_model(object)
    else:
        object = objects_repo.get(id)
        if not object:
            raise HTTPException(status_code=404, detail="Object not found")

        return ObjectResponse.from_model(object)

@router.post("/object/{id}", response_model=ObjectResponse)
def object_post(id: str, payload: ObjectPayload, current_user: User = Depends(get_current_user)):
    if id == "new":
        object = payload.to_model(DefaultObject.model_copy(deep=True))
        object.creator_id = current_user.id
        if not objects_repo.add(object):
            raise HTTPException(status_code=400, detail="Failed to create object")
    else:
        object = objects_repo.get(id)
        if not object:
            raise HTTPException(status_code=404, detail="Object not found")

        object = payload.to_model(object)
        if not objects_repo.update(object):
            raise HTTPException(status_code=400, detail="Failed to update object")

    return ObjectResponse.from_model(object)