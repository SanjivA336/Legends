from fastapi import APIRouter, Depends, HTTPException
from backend.routes.auth_routes import get_current_user, verify_password, hash_password
from backend.database.users_database import users_manager
from backend.models import User
from backend.routes._schemas import UserPayload, UserResponse

# === Config ===
router = APIRouter()

# === Helper Functions ===


# === Endpoints ===
@router.get("/account", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    """
    Get the profile of the currently logged-in user.
    """
    return UserResponse.from_model(current_user)
    
@router.post("/account", response_model=UserResponse)
def update_profile(user_update: UserPayload, current_user: User = Depends(get_current_user)):
    """
    Update the profile of the currently logged-in user.
    """
    if user_update.username:
        current_user.username = user_update.username.strip()
        
    if user_update.email:
        current_user.email = user_update.email.strip()

    if user_update.password and user_update.password_new:
        if not verify_password(user_update.password, current_user.password_hash):
            raise HTTPException(status_code=400, detail="Current password is incorrect")

        if verify_password(user_update.password_new, current_user.password_hash):
            raise HTTPException(status_code=400, detail="New password must be different from the current password")

        current_user.password_hash = hash_password(user_update.password_new)

    if not users_manager.update_user(current_user):
        raise HTTPException(status_code=400, detail="Failed to update user profile")

    return UserResponse.from_model(current_user)