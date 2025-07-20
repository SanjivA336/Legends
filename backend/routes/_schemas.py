from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from backend.models import *
from backend.database.users_database import users_manager
from backend.database.worlds_database import worlds_manager
from backend.database.campaigns_database import campaigns_manager

# Payload: Client (frontend) to Server (backend)
# Response: Server (backend) to Client (frontend)

# === User Schemas ===   
class UserPayload(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    password_new: Optional[str] = None
    
    def to_model(self) -> User:
        return User(
            username=self.username or "",
            email=self.email or "",
            password_hash=self.password or ""
        )
    
class UserResponse(BaseModel):
    id: str
    username: Optional[str] = None
    email: Optional[str] = None
    
    @staticmethod
    def from_model(user: User):
        return UserResponse(id=user.id, username=user.username, email=user.email)

# === World Schemas ===
class WorldPayload(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False
    context: Dict[str, Any] = {}
    settings: Dict[str, Any] = {}
    
    def to_model(self) -> World:
        return World(
            name=self.name,
            description=self.description,
            creator_id="EMPTY",
            is_public=self.is_public,
            context=self.context,
            settings=self.settings
        )
    
class WorldResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    creator: UserResponse
    is_public: bool = False
    context: Dict[str, Any] = {}
    settings: Dict[str, Any] = {}
    
    @staticmethod
    def from_model(world: World):
        creator = users_manager.get_user(world.creator_id)
        if not creator:
            raise ValueError("Creator not found")
        
        return WorldResponse(
            id=world.id,
            name=world.name,
            description=world.description,
            creator=UserResponse.from_model(creator),
            is_public=world.is_public,
            context=world.context,
            settings=world.settings
        )

# === Campaign Schemas ===
class CampaignPayload(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False
    context: Dict[str, Any] = {}
    settings: Dict[str, Any] = {}
    
    def to_model(self) -> Campaign:
        return Campaign(
            name=self.name,
            description=self.description,
            creator_id="EMPTY",
            world_id="EMPTY",
            is_public=self.is_public,
            context=self.context,
            settings=self.settings
        )

class CampaignResponse(BaseModel):
    id: str
    world: Optional[WorldResponse] = None
    name: str
    description: Optional[str] = None
    creator: UserResponse
    is_public: bool = False
    context: Dict[str, Any] = {}
    settings: Dict[str, Any] = {}
    members: Dict[UserResponse, str] = {}
    turn_queue: List[str] = []
    eras: List[str] = []
    
    @staticmethod
    def from_model(campaign: Campaign):
        creator = users_manager.get_user(campaign.creator_id)
        if not creator:
            raise ValueError("Creator not found")
        
        world_response = None
        if campaign.world_id:
            world = worlds_manager.get_world(campaign.world_id)
            if world:
                world_response = WorldResponse.from_model(world)

        members = {}
        for member_id, role in campaign.members.items():
            user = users_manager.get_user(member_id)
            if user:
                members[UserResponse.from_model(user)] = role

        return CampaignResponse(
            id=campaign.id,
            world=world_response,
            name=campaign.name,
            description=campaign.description,
            creator=UserResponse.from_model(creator),
            is_public=campaign.is_public,
            context=campaign.context,
            settings=campaign.settings,
            members=members,
            turn_queue=campaign.turn_queue,
            eras=campaign.era_ids
        )

