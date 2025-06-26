from fastapi import APIRouter, Header, HTTPException
from models.user import UserModel
from utils import verify_firebase_token

router = APIRouter()

@router.get("/profile/{uid}")
def get_profile(uid: str):
    """Fetch user profile data."""
    user = UserModel.get_user(uid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/follow/{target_uid}")
def follow_user(target_uid: str, id_token: str = Header(...)):
    """Current user follows another user."""
    user_info = verify_firebase_token(id_token)
    current_uid = user_info["localId"]
    if current_uid == target_uid:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    UserModel.follow_user(current_uid, target_uid)
    return {"status": "followed"}

@router.post("/unfollow/{target_uid}")
def unfollow_user(target_uid: str, id_token: str = Header(...)):
    """Current user unfollows another user."""
    user_info = verify_firebase_token(id_token)
    current_uid = user_info["localId"]
    UserModel.unfollow_user(current_uid, target_uid)
    return {"status": "unfollowed"}

@router.get("/search/{prefix}")
def search_users(prefix: str):
    """Search users by profile name prefix."""
    return UserModel.search_users_by_profile_prefix(prefix)
