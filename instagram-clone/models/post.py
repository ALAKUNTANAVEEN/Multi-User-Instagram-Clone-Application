from google.cloud import firestore
from datetime import datetime

db = firestore.Client()

class PostModel:
    @staticmethod
    def create_post(uid: str, username: str, image_url: str, caption: str):
        """Create a new post with image, caption, and initialize likes."""
        post_ref = db.collection("Post").document()
        post_ref.set({
            "UserID": uid,
            "Username": username,
            "ImageURL": image_url,
            "Caption": caption,
            "Date": datetime.utcnow(),
            "Comments": [],
            "Likes": [],  # ✅ initialize likes
        })

    @staticmethod
    def get_user_posts(username: str):
        """Get all posts by a specific user in reverse chronological order."""
        posts_ref = db.collection("Post") \
                      .where("Username", "==", username) \
                      .order_by("Date", direction=firestore.Query.DESCENDING)
        return [{"id": doc.id, **doc.to_dict()} for doc in posts_ref.stream()]  # ✅ include ID

    @staticmethod
    def get_timeline_posts(usernames: list):
        """Get posts by current user and followed users for timeline."""
        if not usernames:
            return []
        posts = []
        for username in usernames:
            posts += PostModel.get_user_posts(username)  # user posts already include ID
        return sorted(posts, key=lambda x: x["Date"], reverse=True)[:50]

    @staticmethod
    def add_comment(post_id: str, comment_data: dict):
        """Add a comment to a post."""
        post_ref = db.collection("Post").document(post_id)
        post_ref.update({
            "Comments": firestore.ArrayUnion([comment_data])
        })

    @staticmethod
    def get_post_by_id(post_id: str):
        """Retrieve a post by ID."""
        post_doc = db.collection("Post").document(post_id).get()
        if post_doc.exists:
            return {"id": post_doc.id, **post_doc.to_dict()}  # ✅ include ID
        return None

    @staticmethod
    def toggle_like(post_id: str, uid: str):
        """Toggle like/unlike for a user on a post."""
        post_ref = db.collection("Post").document(post_id)
        post_doc = post_ref.get()
        if post_doc.exists:
            post_data = post_doc.to_dict()
            likes = post_data.get("Likes", [])
            if uid in likes:
                post_ref.update({"Likes": firestore.ArrayRemove([uid])})
            else:
                post_ref.update({"Likes": firestore.ArrayUnion([uid])})
