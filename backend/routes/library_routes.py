from fastapi import APIRouter, Depends, HTTPException
from backend.routes.auth_routes import get_current_user
from backend.database.users_database import users_manager
from backend.database.campaigns_database import campaigns_manager
from backend.database.worlds_database import worlds_manager
from backend.models import User, Campaign, World
from backend.routes._schemas import UserResponse, WorldPayload, WorldResponse, CampaignPayload, CampaignResponse

# === Config ===
router = APIRouter()

# === Helper Functions ===


# === Endpoints ===
@router.get("/worlds", response_model=list[WorldResponse])
def all_worlds(current_user: User = Depends(get_current_user)):
    worlds = worlds_manager.get_worlds_by_user(current_user.id)
    print(len(worlds), "worlds found for user", current_user.id)
    return [WorldResponse.from_model(world) for world in worlds]


@router.get("/world/{id}", response_model=WorldResponse)
def world_get(id: str, current_user: User = Depends(get_current_user)):
    if id == "new":
        default_world = World(
            name="Default World",
            description="This is the default world created with your campaign.",
            creator_id=current_user.id,
            is_public=False
        )

        return WorldResponse.from_model(default_world)
    else:
        world = worlds_manager.get_world(id)
        if not world:
            raise HTTPException(status_code=404, detail="World not found")
        
        return WorldResponse.from_model(world)

@router.post("/world/{id}", response_model=WorldResponse)
def world_post(id: str, world_payload: WorldPayload, current_user: User = Depends(get_current_user)):
    # Validate and create the world
    world = world_payload.to_model("EMPTY")
    
    if id == "new":
        world.creator_id = current_user.id
        
        if not worlds_manager.add_world(world):
            raise HTTPException(status_code=400, detail="Failed to create world")
    else:
        existing_world = worlds_manager.get_world(id)
        if not existing_world:
            raise HTTPException(status_code=404, detail="World not found")
        
        world.id = existing_world.id
        world.creator_id = existing_world.creator_id
        
        if not worlds_manager.update_world(world):
            raise HTTPException(status_code=400, detail="Failed to update world")
        
    return WorldResponse.from_model(world)

@router.get("/campaigns", response_model=list[CampaignResponse])
def all_campaigns(current_user: User = Depends(get_current_user)):
    campaigns = campaigns_manager.get_campaigns_by_user(current_user.id)
    print(len(campaigns), "campaigns found for user", current_user.id)
    return [CampaignResponse.from_model(campaign) for campaign in campaigns]

@router.get("/campaign/{id}", response_model=CampaignResponse)
def campaign_get(id: str, current_user: User = Depends(get_current_user)):
    if id == "new":
        default_campaign = Campaign(
            name="Default Campaign",
            description="This is the default campaign created with your world.",
            creator_id=current_user.id,
            is_public=False
        )

        return CampaignResponse.from_model(default_campaign)
    else:
        campaign = campaigns_manager.get_campaign(id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        return CampaignResponse.from_model(campaign)

@router.post("/campaign/{id}", response_model=CampaignResponse)
def campaign_post(id: str, campaign_payload: CampaignPayload, current_user: User = Depends(get_current_user)):
    # Validate and create the campaign
    campaign = campaign_payload.to_model("EMPTY")
    
    if id == "new":
        campaign.creator_id = current_user.id
        
        if not campaigns_manager.add_campaign(campaign):
            raise HTTPException(status_code=400, detail="Failed to create campaign")
    else:
        existing_campaign = campaigns_manager.get_campaign(id)
        if not existing_campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        campaign.id = existing_campaign.id
        campaign.creator_id = existing_campaign.creator_id
        
        if not campaigns_manager.update_campaign(campaign):
            raise HTTPException(status_code=400, detail="Failed to update campaign")
        
    return CampaignResponse.from_model(campaign)

