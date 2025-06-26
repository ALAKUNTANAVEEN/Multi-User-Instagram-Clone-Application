from dotenv import load_dotenv
load_dotenv()

import os
import uuid
import requests
from fastapi import UploadFile, HTTPException
from google.cloud import storage

# Firebase configuration
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
FIREBASE_VERIFY_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={FIREBASE_API_KEY}"

# Google Cloud Storage configuration
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")


def verify_firebase_token(id_token: str):
    """Verify Firebase ID token and return user info."""
    response = requests.post(FIREBASE_VERIFY_URL, json={"idToken": id_token})
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid Firebase ID token")
    return response.json()["users"][0]


def upload_image_to_gcs(file: UploadFile, filename: str) -> str:
    """Upload image to Google Cloud Storage and return its public URL."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(f"posts/{uuid.uuid4()}_{filename}")
    blob.upload_from_file(file.file, content_type=file.content_type)

    # No ACL changes needed
    return f"https://storage.googleapis.com/{GCS_BUCKET_NAME}/{blob.name}"
