from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# Payload: Client (frontend) to Server (backend)
# Response: Server (backend) to Client (frontend)

# === User Schemas ===   
class UserPayload(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    password_new: Optional[str] = None
    
class UserResponse(BaseModel):
    id: str
    username: Optional[str] = None
    email: Optional[str] = None

# === Campaign Schemas ===
class CampaignCard(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    is_public: bool

# === Page Schemas ===
class HomePage(BaseModel):
    user: UserResponse
    campaigns: List[CampaignCard] = []