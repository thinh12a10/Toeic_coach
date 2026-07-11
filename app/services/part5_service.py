import random
import uuid

from app.services.gemini_service import GeminiService


class Part5Service:
    """Generate TOEIC Speaking Part 5 practice prompts for expressing an opinion."""

    TOPICS = [
        "remote work",
        "social media",
        "workplace flexibility",
        "public transportation",
        "environmental habits",
        "online shopping",
        "teamwork in education",
        "company wellness programs",
        "city development",
        "digital learning",
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
            print(f"Part 5 generation fallback used: {exc}")
            parsed = self._build_fallback_questions(topic)

        return {
            "id": str(uuid.uuid4())[:8],
            "part": 5,
            "task_type": "express_opinion",
            "instruction": "State and defend your opinion clearly. Use an introduction, supporting reasons and examples, and a conclusion.",
            "topic": parsed["topic"],
            "questions": parsed["questions"],
        }

    def _build_generation_prompt(self, topic: str) -> str:
        return f"""
Generate TOEIC Speaking Part 5 practice material for Question 11.
Topic: {topic}
Requirements:
- Create one opinion-based prompt about a workplace or social issue.
- The prompt should ask the speaker to state a personal opinion and defend it.
- The response should be about 60 seconds long.
- The preparation time should be 45 seconds.
Return EXACTLY:
[TOPIC] topic_name
[QUESTION11] question text
"""

    def _parse_response(self, response: str, fallback_topic: str) -> dict:
        topic = fallback_topic
        questions = []

        for line in response.splitlines():
            stripped = line.strip()
            if stripped.startswith("[TOPIC]"):
                topic = stripped.replace("[TOPIC]", "").strip() or fallback_topic
            elif stripped.startswith("[QUESTION11]"):
                questions.append(
                    self._build_question(11, 45, 60, stripped.replace("[QUESTION11]", "").strip())
                )

        if len(questions) != 1:
            return self._build_fallback_questions(topic)

        return {"topic": topic, "questions": questions}

    def _build_question(self, question_number: int, preparation_time: int, response_time: int, text: str) -> dict:
        return {
            "id": str(uuid.uuid4())[:8],
            "question_number": question_number,
            "part": 5,
            "task_type": "express_opinion",
            "instruction": "State your opinion clearly and support it with reasons and examples.",
            "preparation_time": preparation_time,
            "response_time": response_time,
            "text": text or "Do you agree or disagree that workplaces should encourage remote work? State your opinion and explain why.",
            "topic": "workplace or social issue",
        }

    def _build_fallback_questions(self, topic: str) -> dict:
        fallback_prompts = {
            "remote work": "Do you agree or disagree that remote work should become the standard for many companies? State your opinion and explain why.",
            "social media": "Do you think social media has more benefits than drawbacks for young people? State your opinion and support it.",
            "workplace flexibility": "Do you agree that companies should give employees more flexibility in their work schedules? Explain your position.",
            "public transportation": "Do you think public transportation should be improved in your city? State your opinion and defend it.",
            "environmental habits": "Do you agree that individuals should do more to protect the environment in their daily lives? Explain your view.",
            "online shopping": "Do you think online shopping is better than shopping in physical stores? State your opinion and justify it.",
            "teamwork in education": "Do you agree that students should learn teamwork skills at school? Explain your opinion with examples.",
            "company wellness programs": "Do you think companies should offer wellness programs to their employees? State your opinion and explain why.",
            "city development": "Do you agree that cities should invest more in public parks and green spaces? Support your opinion.",
            "digital learning": "Do you believe online learning is as effective as classroom learning? State your opinion and explain it.",
        }

        question_text = fallback_prompts.get(topic, fallback_prompts["remote work"])
        return {
            "topic": topic,
            "questions": [self._build_question(11, 45, 60, question_text)],
        }
