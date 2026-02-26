from fastapi import APIRouter, UploadFile, File, Form
from src.services.face_service import face_service

router = APIRouter(prefix="/identify", tags=["Identification"])

@router.post("/")
async def identify_face(image: UploadFile = File(...), max_results: int = Form(5)):
    image_bytes = await image.read()
    return face_service.identify(image_bytes, max_results)
