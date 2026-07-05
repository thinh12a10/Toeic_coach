from typing import Optional

from pydantic import BaseModel

class Part3Question(BaseModel):
    id: str
    question_number: int
    part: int
    task_type: str
    instruction: str
    preparation_time: int
    response_time: int
    text: str
    topic: str


class Part3QuestionResponse(BaseModel):
    id: str
    part: int
    task_type: str
    instruction: str
    topic: str
    questions: list[Part3Question]


class EvaluationCategory(BaseModel):
    score: float
    strengths: list[str]
    weaknesses: list[str]
    improvement_tips: list[str]


class PronunciationEvaluationPart3(BaseModel):
    score: float

    strengths: list[str]

    weaknesses: list[str]

    mispronounced_words: list[str]

    missing_words: list[str]

    missing_end_sounds: list[str]

    vowel_issues: list[str]

    stress_issues: list[str]

    improvement_tips: list[str]

class Part3EvaluationResponse(BaseModel):
    pronunciation: PronunciationEvaluationPart3
    intonation: EvaluationCategory
    pacing: EvaluationCategory

    overall_feedback: str

    total_score: float

    study_plan: list[str]
    transcript: Optional[str] = None