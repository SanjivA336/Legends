from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict, Optional, Any
from uuid import uuid4

class User(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    username: str
    email: EmailStr
    password_hash: str

class Campaign(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    name: str
    description: Optional[str] = None
    creator_id: str
    members: Dict[str, str]  # user.id -> role (e.g., {"user123": "DM", "user456": "player"})
    turn_queue: List[str]    # List of user IDs in turn order
    is_public: bool = False
    era_ids: List[str]       # List of TimelineNode IDs (Era nodes)
    settings: Dict[str, Any] # Flexible settings dictionary

class TimelineNode(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    type: str  # "Era", "Chapter", "Encounter", "Action", or "other"
    description: str
    data: Dict[str, Any]     # Variable contents based on type
    subnode_ids: List[str]   # IDs of child TimelineNodes

class Actor(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    creator_id: str
    owner_id: Optional[str]  # None if not currently controlled
    campaign_id: str
    data: Dict[str, Any]     # Variable contents based on controller role

class Item(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    creator_id: str
    holder_id: Optional[str]  # None if not currently held
    type: str
    data: Dict[str, Any]      # Variable contents based on type

class Objective(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    name: str
    task: str
    subobjective_ids: List[str]  # List of Objective IDs
