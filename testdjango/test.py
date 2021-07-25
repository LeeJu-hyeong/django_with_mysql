from pathlib import Path
import os

BASE_DIR = str(Path(__file__).resolve().parent.parent)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=BASE_DIR + "/" + "soma-ishadow-f22031078929.json"


def upload_file():
    from google.cloud import storage

    storage_client = storage.Client()
    bucket = storage_client.bucket("soma123")
    blob = bucket.blob("a1.wav")

    blob.upload_from_filename("a1.wav")

upload_file()