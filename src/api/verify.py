from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from src.services.face_service import face_service

router = APIRouter(prefix="/verify", tags=["Verification"])

@router.post("/")
async def verify_face(user_id: str = Form(...), image: UploadFile = File(...)):
    if not image.content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image")
    
    image_bytes = await image.read()
    result = face_service.verify(user_id, image_bytes)
    
    if not result["success"]:
        if result.get("error") == "User not found":
            raise HTTPException(404, result["error"])
        raise HTTPException(400, result["error"])
    
    return result
