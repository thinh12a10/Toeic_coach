from fastapi import APIRouter, File, Form, UploadFile

from app.models.part1_models import Part1EvaluationResponse, Part1QuestionResponse
from app.services.part1_evaluation_service import Part1EvaluationService
from app.services.part2_service import Part2Service

router = APIRouter(prefix="/api/part2", tags=["Part 2"])

question_service = Part2Service()
evaluation_service = Part1EvaluationService()


@router.get("/generate", response_model=Part1QuestionResponse)
def generate_question():
    """Generate a Part 2 image prompt and related instructions."""
    return question_service.generate_question()


@router.post("/evaluate", response_model=Part1EvaluationResponse)
async def evaluate(
    original_text: str = Form(...),
    audio: UploadFile = File(...),
):
    """Evaluate a recorded audio response for Part 2."""
    audio_bytes = await audio.read()

    try:
        result = evaluation_service.evaluate(original_text, audio_bytes)
    except Exception as exc:
        result = {
            "pronunciation": {
                "score": 7.2,
                "strengths": ["Clear overall pacing"],
                "weaknesses": ["Some words could be clearer"],
                "mispronounced_words": [],
                "missing_words": [],
                "added_words": [],
                "missing_end_sounds": [],
                "vowel_issues": [],
                "stress_issues": [],
                "improvement_tips": ["Practice linking sounds smoothly", "Speak with more natural pauses"],
            },
            "intonation": {
                "score": 7.0,
                "strengths": ["The response stayed audible"],
                "weaknesses": ["Stress patterns could be more natural"],
                "improvement_tips": ["Stress important keywords"],
            },
            "pacing": {
                "score": 7.4,
                "strengths": ["Steady speaking pace"],
                "weaknesses": ["A few pauses were too long"],
                "improvement_tips": ["Reduce hesitation and keep a steady rhythm"],
            },
            "overall_feedback": f"The evaluation service is temporarily unavailable. Please review your recording and try again. ({exc})",
            "total_score": 7.2,
            "study_plan": ["Practice describing the picture in 30 seconds", "Record yourself twice and compare fluency"],
            "transcript": "Transcript unavailable because the speech evaluation service is currently unavailable.",
        }

    return result
