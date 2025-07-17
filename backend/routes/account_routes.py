from fastapi import APIRouter, Depends, HTTPException
from backend.routes.auth_routes import get_current_user, verify_password, hash_password
from backend.database.users_database import users_manager
from backend.models import User
from backend.routes._schemas import UserPayload, UserResponse

# === Config ===
router = APIRouter()

# === Helper Functions ===


# === Endpoints ===
@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    """
    Get the profile of the currently logged-in user.
    """
    user = users_manager.get_user(current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
    )
    
@router.post("/profile", response_model=UserResponse)
def update_profile(user_update: UserPayload, current_user: User = Depends(get_current_user)):
    """
    Update the profile of the currently logged-in user.
    """
    user = users_manager.get_user(current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.username:
        user.username = user_update.username.strip()
        
    if user_update.email:
        user.email = user_update.email.strip()
        
    if user_update.password and user_update.password_new:
        if not verify_password(user_update.password, user.password_hash):
            raise HTTPException(status_code=400, detail="Incorrect password")
        
        if verify_password(user_update.password_new, user.password_hash):
            raise HTTPException(status_code=400, detail="New password must be different from the old one")
        
        user.password_hash = hash_password(user_update.password_new)

    if not users_manager.update_user(user):
        raise HTTPException(status_code=400, detail="Failed to update user profile")
    
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
    )