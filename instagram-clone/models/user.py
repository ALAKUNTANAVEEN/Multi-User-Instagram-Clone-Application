from google.cloud import firestore

db = firestore.Client()

class UserModel:
    @staticmethod
    def create_user(uid: str, username: str):
        """Initialize a new user document."""
        user_ref = db.collection("User").document(uid)
        user_ref.set({
            "Username": username,
            "Followers": [],
            "Following": [],
        })

    @staticmethod
    def get_user(uid: str):
        """Retrieve user document by UID."""
        user_doc = db.collection("User").document(uid).get()
        if user_doc.exists:
            return user_doc.to_dict()
        return None

    @staticmethod
    def follow_user(current_uid: str, target_uid: str):
        """Current user follows another user."""
        db.collection("User").document(current_uid).update({
            "Following": firestore.ArrayUnion([target_uid])
        })
        db.collection("User").document(target_uid).update({
            "Followers": firestore.ArrayUnion([current_uid])
        })

    @staticmethod
    def unfollow_user(current_uid: str, target_uid: str):
        """Current user unfollows another user."""
        db.collection("User").document(current_uid).update({
            "Following": firestore.ArrayRemove([target_uid])
        })
        db.collection("User").document(target_uid).update({
            "Followers": firestore.ArrayRemove([current_uid])
        })

    @staticmethod
    def search_users_by_profile_prefix(prefix: str):
        """Search users by profile name prefix."""
        users_ref = db.collection("User").where("Username", ">=", prefix).where("Username", "<=", prefix + "\uf8ff")
        return [doc.to_dict() for doc in users_ref.stream()]
