from fastapi import APIRouter, Header, HTTPException
from utils import verify_firebase_token
from models.user import UserModel

router = APIRouter()

@router.post("/login")
def login(id_token: str = Header(...)):
    """
    Verifies Firebase token and initializes user if first login.
    """
    user_info = verify_firebase_token(id_token)
    uid = user_info["localId"]
    username = user_info.get("displayName", f"user_{uid[:6]}")

    user = UserModel.get_user(uid)
    if not user:
        UserModel.create_user(uid, username)

    return {"uid": uid, "username": username}
