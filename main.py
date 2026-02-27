from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import hashlib
from datetime import datetime, timezone
import os
from google.cloud import storage

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok", "service": "wildlife-ingest-api"}

@app.post("/ingest")
async def ingest(
    file: UploadFile = File(...),
    camera_id: str = Form("unknown"),
    captured_at: str = Form("")
):
    content = await file.read()
    sha256 = hashlib.sha256(content).hexdigest()
    received_at = datetime.now(timezone.utc).isoformat()

    bucket_name = os.environ["BUCKET_NAME"]

    ext = ".jpg"
    date_prefix = captured_at[:10] if captured_at else received_at[:10]
    object_name = f"raw/{camera_id}/{date_prefix}/{sha256}{ext}"

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    blob.upload_from_string(content, content_type="image/jpeg")

    return JSONResponse({
        "ok": True,
        "camera_id": camera_id,
        "captured_at": captured_at,
        "received_at": received_at,
        "sha256": sha256,
        "gcs_bucket": bucket_name,
        "gcs_object": object_name
    })
