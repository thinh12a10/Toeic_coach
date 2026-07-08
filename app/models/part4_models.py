from pydantic import BaseModel


class Part4Question(BaseModel):
    id: str
    question_number: int
    part: int
    task_type: str
    instruction: str
    preparation_time: int
    response_time: int
    text: str
    topic: str


class Part4QuestionResponse(BaseModel):
    id: str
    part: int
    task_type: str
    instruction: str
    topic: str
    document: str
    questions: list[Part4Question]
