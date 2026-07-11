from typing import Optional
from pydantic import BaseModel


class Part5Question(BaseModel):
    id: str
    question_number: int
    part: int
    task_type: str
    instruction: str
    preparation_time: int
    response_time: int
    text: str
    topic: str


class Part5QuestionResponse(BaseModel):
    id: str
    part: int
    task_type: str
    instruction: str
    topic: str
    questions: list[Part5Question]


class PronunciationEvaluationPart5(BaseModel):
    score: float
    strengths: list[str]
    weaknesses: list[str]
    mispronounced_words: list[str]
    missing_words: list[str]
    added_words: list[str]
    missing_end_sounds: list[str]
    vowel_issues: list[str]
    stress_issues: list[str]
    improvement_tips: list[str]


class EvaluationCategory(BaseModel):
    score: float
    strengths: list[str]
    weaknesses: list[str]
    improvement_tips: list[str]


class Part5EvaluationResponse(BaseModel):
    pronunciation: PronunciationEvaluationPart5
    organization: EvaluationCategory
    delivery: EvaluationCategory
    overall_feedback: str
    study_plan: list[str]
    total_score: float
