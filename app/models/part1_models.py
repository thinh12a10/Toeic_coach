from pydantic import BaseModel


class Part1QuestionResponse(BaseModel):
    id: str
    part: int
    task_type: str
    instruction: str
    preparation_time: int
    response_time: int
    text: str
    topic: str


class EvaluationCategory(BaseModel):
    score: float
    strengths: list[str]
    weaknesses: list[str]
    improvement_tips: list[str]


class PronunciationEvaluation(BaseModel):
    score: float

    strengths: list[str]

    weaknesses: list[str]

    mispronounced_words: list[str]

    missing_words: list[str]

    missing_end_sounds: list[str]

    vowel_issues: list[str]

    stress_issues: list[str]

    improvement_tips: list[str]

class Part1EvaluationResponse(BaseModel):
    pronunciation: PronunciationEvaluation
    intonation: EvaluationCategory
    pacing: EvaluationCategory

    overall_feedback: str

    total_score: float

    study_plan: list[str]