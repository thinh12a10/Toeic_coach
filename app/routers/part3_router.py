from fastapi import APIRouter, File, Form, UploadFile

from app.models.part1_models import Part3EvaluationResponse, Part3QuestionResponse
from app.services.part3_evaluation_service import Part3EvaluationService
from app.services.part3_service import Part3Service

router = APIRouter(prefix="/api/part3", tags=["Part 3"])

question_service = Part3Service()
evaluation_service = Part3EvaluationService()


@router.get("/generate", response_model=Part3QuestionResponse)
def generate_questions():
    return question_service.generate_questions()


@router.post("/evaluate", response_model=Part3EvaluationResponse)
async def evaluate(
    original_text: str = Form(...),
    audio: UploadFile = File(...),
):
    audio_bytes = await audio.read()
    return evaluation_service.evaluate(original_text, audio_bytes)
