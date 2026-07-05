import random
import uuid

from app.services.gemini_service import GeminiService


class Part3Service:
    """Generate TOEIC Speaking Part 3 questions 5-7 for short responses."""

    TOPICS = [
        "daily routine",
        "shopping",
        "transportation",
        "health and fitness",
        "home life",
        "technology use",
        "leisure activities",
        "food and dining",
        "neighborhood life",
        "work habits",
    ]

    def __init__(self):
        self.gemini = GeminiService()

    def generate_questions(self) -> dict:
        topic = random.choice(self.TOPICS)
        prompt = self._build_generation_prompt(topic)

        try:
            response = self.gemini.generate(prompt)
            parsed = self._parse_response(response, topic)
        except Exception as exc:
            print(f"Part 3 generation fallback used: {exc}")
            parsed = self._build_fallback_questions(topic)

        return {
            "id": str(uuid.uuid4())[:8],
            "part": 3,
            "task_type": "respond_to_questions",
            "instruction": "Answer the questions naturally and completely. Respond immediately after the beep.",
            "topic": parsed["topic"],
            "questions": parsed["questions"],
        }

    def _build_generation_prompt(self, topic: str) -> str:
        return f"""
Generate TOEIC Speaking Part 3 practice questions 5-7.
Topic: {topic}
Requirements:
- Three consecutive questions about the same everyday lifestyle topic.
- Speaker is an interviewee in a marketing survey or telephone interview.
- Question 5 and 6 should each require a 15-second response.
- Question 7 should require a 30-second response.
- Questions should sound natural and conversational.
Return EXACTLY:
[TOPIC] topic_name
[QUESTION5] question text
[QUESTION6] question text
[QUESTION7] question text
"""

    def _parse_response(self, response: str, fallback_topic: str) -> dict:
        topic = fallback_topic
        questions = []

        current_key = None
        for line in response.splitlines():
            stripped = line.strip()
            if stripped.startswith("[TOPIC]"):
                topic = stripped.replace("[TOPIC]", "").strip() or fallback_topic
                current_key = None
            elif stripped.startswith("[QUESTION5]"):
                questions.append(self._build_question(5, 15, stripped.replace("[QUESTION5]", "").strip()))
                current_key = None
            elif stripped.startswith("[QUESTION6]"):
                questions.append(self._build_question(6, 15, stripped.replace("[QUESTION6]", "").strip()))
                current_key = None
            elif stripped.startswith("[QUESTION7]"):
                questions.append(self._build_question(7, 30, stripped.replace("[QUESTION7]", "").strip()))
                current_key = None

        if len(questions) != 3:
            return self._build_fallback_questions(topic)

        return {"topic": topic, "questions": questions}

    def _build_question(self, question_number: int, response_time: int, text: str) -> dict:
        return {
            "id": str(uuid.uuid4())[:8],
            "question_number": question_number,
            "part": 3,
            "task_type": "respond_to_questions",
            "instruction": "Answer the question clearly and naturally.",
            "preparation_time": 0,
            "response_time": response_time,
            "text": text or f"Please answer this question about your daily life.",
            "topic": "everyday lifestyle",
        }

    def _build_fallback_questions(self, topic: str) -> dict:
        fallback_map = {
            "daily routine": [
                "How do you usually spend your mornings before work or school?",
                "What do you do to relax after a busy day?",
                "Can you tell me about a recent weekend activity you enjoyed?",
            ],
            "shopping": [
                "How often do you shop for groceries or daily necessities?",
                "What do you usually look for when buying clothes?",
                "Tell me about a recent purchase that made you happy.",
            ],
            "transportation": [
                "How do you usually travel to work or school?",
                "What are the advantages of using public transportation?",
                "Describe a trip you took recently and how you traveled there.",
            ],
            "health and fitness": [
                "How do you keep yourself healthy in your daily life?",
                "What kind of exercise do you enjoy doing?",
                "Tell me about a healthy habit you want to keep in the future.",
            ],
            "home life": [
                "What do you usually do at home on a typical evening?",
                "How do you organize your living space?",
                "Describe a recent change you made to improve your home life.",
            ],
            "technology use": [
                "How often do you use your smartphone during the day?",
                "What kind of apps or websites do you use most often?",
                "Tell me about a technology device that has made your life easier.",
            ],
            "leisure activities": [
                "What do you like to do in your free time?",
                "How do you usually spend a holiday or day off?",
                "Tell me about a hobby you have been enjoying recently.",
            ],
            "food and dining": [
                "What kinds of food do you enjoy eating most?",
                "How often do you eat out with friends or family?",
                "Tell me about a meal you recently enjoyed.",
            ],
            "neighborhood life": [
                "What facilities are near your home?",
                "How do you usually spend time with your neighbors?",
                "Tell me about a place in your neighborhood that you like.",
            ],
            "work habits": [
                "How do you usually organize your workday?",
                "What helps you stay productive at work?",
                "Tell me about a recent work task you handled successfully.",
            ],
        }

        questions = fallback_map.get(topic, fallback_map["daily routine"])
        built_questions = [
            self._build_question(5, 15, questions[0]),
            self._build_question(6, 15, questions[1]),
            self._build_question(7, 30, questions[2]),
        ]

        return {"topic": topic, "questions": built_questions}
