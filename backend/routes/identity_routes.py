import json
from fastapi import APIRouter, Depends, HTTPException, status, Response, Header
from backend.database import REPO, fs
from backend.models import *
from typing import List, Optional

import os
from passlib.context import CryptContext
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer

from .routes_helper import changes_to_string
import firebase_admin
from firebase_admin import credentials, auth

# region === Config === ===
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7
REFRESH_TOKEN_EXPIRE_MINUTES = REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

def get_firebase_admin_cred():
    creds_json = os.environ.get("FIREBASE_CREDENTIALS")
    if creds_json:
        try:
            service_account_info = json.loads(creds_json)
            return credentials.Certificate(service_account_info)
        except Exception as e:
            raise RuntimeError("Failed to parse FIREBASE_CREDENTIALS: " + str(e))

    creds_path = os.environ.get("FIREBASE_CREDENTIALS_PATH", "backend/Keys/legends-firebase-serviceAccount.json")
    if os.path.exists(creds_path):
        try:
            return credentials.Certificate(creds_path)
        except Exception as e:
            raise RuntimeError("Failed to load credentials from file: " + str(e))

    raise RuntimeError("No Firebase credentials found.")

cred = get_firebase_admin_cred()
firebase_admin.initialize_app(cred)
#endregion

# region === Helper Methods === ===
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing auth token.")

    token = authorization.split(" ")[1]

    try:
        decoded = auth.verify_id_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid auth token." + str(e))

    uid = decoded["uid"]
    user = REPO.USERS.get(uid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user

def get_current_member(user: User, campaign_id: str) -> Member:
    members = REPO.MEMBERS.query([("user_id", "==", user.id), ("campaign_id", "==", campaign_id), ("is_active", "==", True)])
    if not members:
        raise HTTPException(status_code=404, detail="You do not have access to this campaign.")

    return members[0]
# endregion

# region === Current API === ===
@router.get("/current/user", response_model=UserProtected)
async def get_current_user_route(current_user: User = Depends(get_current_user)):
    return UserProtected.from_model(current_user)

@router.get("/current/members", response_model=List[Member])
async def get_current_members(current_user: User = Depends(get_current_user)):
    return current_user.get_members()

@router.get("/current/can_access/{campaign_id}", response_model=bool)
async def check_access(campaign_id: str, current_user: User = Depends(get_current_user)):
    members = REPO.MEMBERS.query([("user_id", "==", current_user.id), ("campaign_id", "==", campaign_id), ("is_active", "==", True)])
    return len(members) > 0
# endregion

# region === User API === ===
@router.post("/user", response_model=UserProtected)
def user_create(payload: UserPayload, response: Response):    
    if not payload.username or payload.username.strip() == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is required.")
    
    if not payload.email or payload.email.strip() == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is required.")
    
    if not payload.password_current or payload.password_current.strip() == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is required.")

    if len(REPO.USERS.query([('email','==', payload.email.strip().lower())])) > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An account with that email already exists.")
    
    user = User(
        username=payload.username,
        email=payload.email.strip().lower(),
        password_hashed=pwd_context.hash(payload.password_current)
    )

    if (created := REPO.USERS.add(user)):
        return UserProtected.from_model(created)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User registration failed")

@router.get("/user/{user_id}", response_model=UserProtected)
def user_get(user_id: str, current_user: User = Depends(get_current_user)):
    if (user := REPO.USERS.get(user_id)):
        return UserProtected.from_model(user)
    raise HTTPException(status_code=404, detail="User not found.")

@router.patch("/user", response_model=UserProtected)
def user_update(payload: UserPayload, current_user: User = Depends(get_current_user)):
    if not payload.id or payload.id.strip() == "":
        raise HTTPException(status_code=400, detail="User ID is required in payload for update.")

    if not current_user.id == payload.id:
        raise HTTPException(status_code=403, detail="You can only update your own user information.")

    user = REPO.USERS.get(payload.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    if payload.password_new:
        if not payload.password_current:
            raise HTTPException(status_code=400, detail="Current password is required to set a new password.")
        
        if not pwd_context.verify(payload.password_current, user.password_hashed):
            raise HTTPException(status_code=403, detail="Current password is incorrect.")
        
        if payload.password_new == payload.password_current:
            raise HTTPException(status_code=400, detail="New password cannot be the same as the old password.")

        user.password_hashed = pwd_context.hash(payload.password_new)

    if payload.email and payload.email.strip().lower() != user.email:
        if len(REPO.USERS.query([('email','==', payload.email.strip().lower())])) > 0:
            raise HTTPException(status_code=400, detail="An account with that email already exists.")

    payload.email = payload.email.strip().lower() if payload.email else None

    updated_user = payload.to_model(user, preserve=True)
    
    if not (changes := user.diff(updated_user)):
        return user

    if (updated_user := REPO.USERS.update(updated_user)):
        return UserProtected.from_model(updated_user)
    raise HTTPException(status_code=500, detail="User update failed.")

@router.delete("/user/{user_id}", response_model=bool)
def user_delete(user_id: str, current_user: User = Depends(get_current_user)):
    user = REPO.USERS.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if not current_user.id == user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own user account.")
        
    batch = user.delete(fs.create_batch())

    if fs.commit_batch(batch):
        return True
    raise HTTPException(status_code=500, detail="User deletion failed.")

# User-Specific APIs
@router.get("/user/{user_id}/members", response_model=List[Member])
def user_get_members(user_id: str, current_user: User = Depends(get_current_user)):
    user = REPO.USERS.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    if not current_user.id == user.id:
        raise HTTPException(status_code=403, detail="You can only access your own members.")

    return user.get_members()

@router.get("/user/{user_id}/worlds", response_model=List[World])
def user_get_worlds(user_id: str, current_user: User = Depends(get_current_user)):
    user = REPO.USERS.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    if not current_user.id == user.id:
        raise HTTPException(status_code=403, detail="You can only access your own worlds.")

    return user.get_worlds()

@router.get("/user/{user_id}/campaigns", response_model=List[Campaign])
def user_get_campaigns(user_id: str, current_user: User = Depends(get_current_user)):
    user = REPO.USERS.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    if not current_user.id == user.id:
        raise HTTPException(status_code=403, detail="You can only access your own campaigns.")

    return user.get_campaigns()
# endregion

# region === Member API === ===
@router.post("/member", response_model=Member)
def member_create(payload: MemberPayload, current_user: User = Depends(get_current_user)):
    if not payload.campaign_id:
        raise HTTPException(status_code=400, detail="Campaign ID is required.")

    if not (campaign := REPO.CAMPAIGNS.get(payload.campaign_id)):
        raise HTTPException(status_code=404, detail="Campaign not found.")

    if not payload.user_id:
        payload.user_id = current_user.id

    if not (user := REPO.USERS.get(payload.user_id)):
        raise HTTPException(status_code=404, detail="User not found.")

    campaign_members = REPO.MEMBERS.query([("campaign_id", "==", payload.campaign_id)])
    if any(member.user_id == payload.user_id for member in campaign_members):
        raise HTTPException(status_code=400, detail="User is already a member of this campaign.")

    member = Member(
        user_id=payload.user_id,
        campaign_id=payload.campaign_id,
        is_admin=False,
        is_dm=False,
        is_active=False,
        character_id=payload.character_id,
        equipped_ids=payload.equipped_ids or [],
        inventory_ids=payload.inventory_ids or [],
    )
    
    campaign.member_ids.append(member.id)
    user.member_ids.append(member.id)

    batch = fs.create_batch()

    REPO.USERS.batch_update(batch, user)
    REPO.CAMPAIGNS.batch_update(batch, campaign)
    REPO.MEMBERS.batch_add(batch, member)

    if fs.commit_batch(batch):
        return member
    raise HTTPException(status_code=500, detail="Member creation failed.")

@router.get("/member/{member_id}", response_model=Member)
def member_get(member_id: str, current_user: User = Depends(get_current_user)):
    member = REPO.MEMBERS.get(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found.")

    if not (current_member := get_current_member(current_user, member.campaign_id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    return member

@router.patch("/member", response_model=Member)
def member_update(payload: MemberPayload, current_user: User = Depends(get_current_user)):
    if not payload.id or payload.id.strip() == "":
        raise HTTPException(status_code=400, detail="Member ID is required in payload for update.")
    
    member = REPO.MEMBERS.get(payload.id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found.")

    current_member = get_current_member(current_user, member.campaign_id)
    if not current_member:
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    if not current_member.is_admin:
        if current_member.id != member.id:
            raise HTTPException(status_code=403, detail="Only admins can update other members.")
        
        if payload.is_admin is not None and payload.is_admin != member.is_admin:
            raise HTTPException(status_code=403, detail="Only admins can change admin status.")

    updated_member = payload.to_model(member, preserve=True)
    
    if not (changes := member.diff(updated_member)):
        return member
    
    batch = fs.create_batch()

    REPO.MEMBERS.batch_update(batch, updated_member)

    if fs.commit_batch(batch):
        return updated_member
    raise HTTPException(status_code=500, detail="Member update failed.")

@router.delete("/member/{member_id}", response_model=bool)
def member_delete(member_id: str, current_user: User = Depends(get_current_user)):
    member = REPO.MEMBERS.get(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found.")

    current_member = get_current_member(current_user, member.campaign_id)
    if not current_member:
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    if not current_member.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can delete members.")

    batch = member.delete(fs.create_batch())
    
    if fs.commit_batch(batch):
        return True
    raise HTTPException(status_code=500, detail="Member deletion failed.")

# Member-Specific APIs
@router.get("/member/{member_id}/user", response_model=UserProtected)
def member_get_user(member_id: str, current_user: User = Depends(get_current_user)):
    member = REPO.MEMBERS.get(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found.")

    if not (current_member := get_current_member(current_user, member.campaign_id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    user = member.get_user()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user

@router.get("/member/{member_id}/campaign", response_model=Campaign)
def member_get_campaign(member_id: str, current_user: User = Depends(get_current_user)):
    member = REPO.MEMBERS.get(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found.")

    if not (current_member := get_current_member(current_user, member.campaign_id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    campaign = member.get_campaign()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found.")

    return campaign

@router.get("/member/{member_id}/character", response_model=Optional[Object])
def member_get_character(member_id: str, current_user: User = Depends(get_current_user)):
    member = REPO.MEMBERS.get(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found.")

    if not (current_member := get_current_member(current_user, member.campaign_id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    return member.get_character()

@router.get("/member/{member_id}/equipped", response_model=List[Object])
def member_get_equipped(member_id: str, current_user: User = Depends(get_current_user)):
    member = REPO.MEMBERS.get(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found.")

    if not (current_member := get_current_member(current_user, member.campaign_id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    return member.get_equipped()

@router.get("/member/{member_id}/inventory", response_model=List[Object])
def member_get_inventory(member_id: str, current_user: User = Depends(get_current_user)):
    member = REPO.MEMBERS.get(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found.")

    if not (current_member := get_current_member(current_user, member.campaign_id)):
        raise HTTPException(status_code=403, detail="You do not have access to this campaign.")

    return member.get_inventory()
# endregion
