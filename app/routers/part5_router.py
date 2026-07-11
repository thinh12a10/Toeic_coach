from fastapi import APIRouter, File, Form, UploadFile

from app.models.part3_models import Part3EvaluationResponse
from app.models.part5_models import Part5QuestionResponse
from app.services.part5_evaluation_service import Part5EvaluationService
from app.services.part5_service import Part5Service

router = APIRouter(prefix="/api/part5", tags=["Part 5"])

question_service = Part5Service()
evaluation_service = Part5EvaluationService()


@router.get("/generate", response_model=Part5QuestionResponse)
def generate_questions():
    return question_service.generate_questions()


@router.post("/evaluate", response_model=Part3EvaluationResponse)
async def evaluate(
    original_text: str = Form(...),
    audio: UploadFile = File(...),
):
    audio_bytes = await audio.read()
    return evaluation_service.evaluate(original_text, audio_bytes)
