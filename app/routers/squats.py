from fastapi import APIRouter, UploadFile, File
from app.services.squat_service import analyze_squats

router = APIRouter()

@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    result = analyze_squats(file.file)
    return result
