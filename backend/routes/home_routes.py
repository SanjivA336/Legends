from fastapi import APIRouter, Depends, HTTPException
from backend.routes.auth_routes import get_current_user
from backend.database.users_database import users_manager
from backend.database.campaigns_database import campaigns_manager
from backend.routes._schemas import HomePage, UserResponse, CampaignCard
from backend.models import User, Campaign

# === Config ===
router = APIRouter()

# === Helper Functions ===


# === Endpoints ===
@router.get("/home", response_model=HomePage)
def get_profile(current_user: User = Depends(get_current_user)):
    campaigns = campaigns_manager.get_campaigns_by_user(current_user.id)
    
    data = HomePage(
        user=UserResponse(
            id=current_user.id,
            username=current_user.username,
            email=current_user.email
        ),
        campaigns=[]
    )
    
    for campaign in campaigns:
        data.campaigns.append(
            CampaignCard(
                id=campaign.id,
                name=campaign.name,
                description=campaign.description,
                is_public=campaign.is_public
            )
        )
        
    return data