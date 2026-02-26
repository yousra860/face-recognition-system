from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from src.services.face_service import face_service

router = APIRouter(prefix="/enroll", tags=["Enrollment"])

@router.post("/")
async def enroll_face(
    user_id: str = Form(...),
    full_name: str = Form(...),
    email: Optional[str] = Form(None),
    department: Optional[str] = Form(None),
    image: UploadFile = File(...)
):
    if not image.content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image")
    
    image_bytes = await image.read()
    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(400, "File too large")
    
    result = face_service.enroll(user_id, image_bytes, full_name, email, department)
    
    if not result["success"]:
        status_code = 409 if "already exists" in result["error"] else 400
        raise HTTPException(status_code, result["error"])
    
    return result
