from fastapi import APIRouter, UploadFile, Form, Header, HTTPException
from utils import verify_firebase_token, upload_image_to_gcs
from models.user import UserModel
from models.post import PostModel
from datetime import datetime

router = APIRouter()

@router.post("/create")
async def create_post(
    file: UploadFile,
    caption: str = Form(...),
    id_token: str = Header(..., convert_underscores=False)
):
    """Create a new post with image and caption."""
    try:
        print("file:", file.filename)
        print("caption:", caption)
        print("id_token:", id_token)

        if file.content_type not in ["image/png", "image/jpeg"]:
            raise HTTPException(status_code=400, detail="Only PNG and JPG allowed")

        user_info = verify_firebase_token(id_token)
        uid = user_info["localId"]
        username = user_info.get("displayName", f"user_{uid[:6]}")

        image_url = upload_image_to_gcs(file, file.filename)
        PostModel.create_post(uid, username, image_url, caption)

        return {"status": "post created", "image_url": image_url}

    except Exception as e:
        print("🚨 Upload failed:", e)
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


@router.get("/user/{username}")
def get_user_posts(username: str):
    """Get posts of a specific user."""
    return PostModel.get_user_posts(username)


@router.get("/timeline")
def get_timeline(id_token: str = Header(None)):
    """Get timeline posts of current user and followed users."""
    if not id_token:
        raise HTTPException(status_code=401, detail="Missing id_token header")

    user_info = verify_firebase_token(id_token)
    uid = user_info["localId"]
    user_data = UserModel.get_user(uid)
    usernames = [user_data["Username"]] + [
        UserModel.get_user(uid)["Username"] for uid in user_data.get("Following", [])
    ]
    return PostModel.get_timeline_posts(usernames)


@router.post("/comment/{post_id}")
def add_comment(post_id: str, comment: str = Form(...), id_token: str = Header(...)):
    """Add a comment to a post (max 200 characters)."""
    if len(comment) > 200:
        raise HTTPException(status_code=400, detail="Comment too long")

    user_info = verify_firebase_token(id_token)
    username = user_info.get("displayName", f"user_{user_info['localId'][:6]}")

    comment_data = {
        "username": username,
        "comment": comment,
        "timestamp": datetime.utcnow().isoformat()
    }

    PostModel.add_comment(post_id, comment_data)
    return {"status": "comment added"}

@router.post("/like/{post_id}")
def like_post(post_id: str, id_token: str = Header(...)):
    user_info = verify_firebase_token(id_token)
    uid = user_info["localId"]
    PostModel.toggle_like(post_id, uid)
    return {"status": "like toggled"}

