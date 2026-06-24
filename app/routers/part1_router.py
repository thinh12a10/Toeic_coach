from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form
)

from app.models.part1_models import (
    Part1QuestionResponse,
    Part1EvaluationResponse
)

from app.services.part1_service import (
    Part1Service
)

from app.services.part1_evaluation_service import (
    Part1EvaluationService
)

router = APIRouter(
    prefix="/api/part1",
    tags=["Part 1"]
)

question_service = Part1Service()

evaluation_service = (
    Part1EvaluationService()
)


@router.get(
    "/generate",
    response_model=Part1QuestionResponse
)
def generate_question():

    return question_service.generate_question()


@router.post(
    "/evaluate",
    response_model=Part1EvaluationResponse
)
async def evaluate(
    original_text: str = Form(...),
    audio: UploadFile = File(...)
):

    audio_bytes = await audio.read()

    return evaluation_service.evaluate(
        original_text,
        audio_bytes
    )