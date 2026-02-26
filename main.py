from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import hashlib
from datetime import datetime, timezone

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok", "service": "camera-ingest-api"}

@app.post("/ingest")
async def ingest(
    file: UploadFile = File(...),
    camera_id: str = Form("unknown"),
    captured_at: str = Form("")
):
    content = await file.read()
    sha256 = hashlib.sha256(content).hexdigest()
    received_at = datetime.now(timezone.utc).isoformat()

    return JSONResponse({
        "ok": True,
        "camera_id": camera_id,
        "captured_at": captured_at,
        "received_at": received_at,
        "filename": file.filename,
        "bytes": len(content),
        "sha256": sha256
    })
