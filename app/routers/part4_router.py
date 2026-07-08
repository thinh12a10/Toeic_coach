from fastapi import APIRouter, File, Form, UploadFile

from app.models.part3_models import Part3EvaluationResponse
from app.models.part4_models import Part4QuestionResponse
from app.services.part4_evaluation_service import Part4EvaluationService
from app.services.part4_service import Part4Service

router = APIRouter(prefix="/api/part4", tags=["Part 4"])

question_service = Part4Service()
evaluation_service = Part4EvaluationService()


@router.get("/generate", response_model=Part4QuestionResponse)
def generate_questions():
    return question_service.generate_questions()


@router.post("/evaluate", response_model=Part3EvaluationResponse)
async def evaluate(
    document: str = Form(...),
    original_text: str = Form(...),
    audio: UploadFile = File(...),
):
    audio_bytes = await audio.read()
    return evaluation_service.evaluate(document, original_text, audio_bytes)
