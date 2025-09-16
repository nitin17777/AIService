from fastapi import APIRouter, UploadFile, File
from app.services.pushup_service import analyze_pushups

router = APIRouter()

@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    result = analyze_pushups(file.file)
    return result
