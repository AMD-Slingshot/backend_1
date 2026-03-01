from fastapi import APIRouter
from pydantic import BaseModel
from app.services.gemini_service import generate_text

router = APIRouter()

class TextRequest(BaseModel):
    prompt: str

@router.post("/generate")
def generate(request: TextRequest):
    result = generate_text(request.prompt)
    return {"output": result}