import random
import uuid

from app.services.gemini_service import GeminiService

class Part1Service:

    TOPICS = [
        "business",
        "office",
        "customer service",
        "travel",
        "technology",
        "education",
        "health",
        "shopping",
        "transportation",
        "environment"
    ]

    def __init__(self):
        self.gemini = GeminiService()

    def generate_question(self) -> dict:
        prompt = self._build_generation_prompt()

        response = self.gemini.generate(prompt)

        parsed = self._parse_response(response)

        return {
            "id": str(uuid.uuid4())[:8],
            "part": 1,
            "task_type": "read_aloud",
            "instruction": "Please read the following text aloud.",
            "preparation_time": 45,
            "response_time": 45,
            "text": parsed["text"],
            "topic": parsed["topic"]
        }

    def _build_generation_prompt(self) -> str:

        topic = random.choice(self.TOPICS)

        return f"""
Generate ONE TOEIC Speaking Part 1 (Read Aloud) passage.

Requirements:
- Topic: {topic}
- Length: 60-100 words
- Natural business or daily-life English
- Similar to official TOEIC Speaking Part 1 passages
- Grammatically correct
- No bullet points
- No title

Return EXACTLY:

[QUESTION] passage text
[TOPIC] topic_name
"""

    def _parse_response(self, response: str) -> dict:

        result = {
            "text": "",
            "topic": "general"
        }

        for line in response.splitlines():

            if line.startswith("[QUESTION]"):
                result["text"] = (
                    line.replace("[QUESTION]", "")
                    .strip()
                )

            elif line.startswith("[TOPIC]"):
                result["topic"] = (
                    line.replace("[TOPIC]", "")
                    .strip()
                )

        if not result["text"]:
            raise ValueError(
                "Failed to parse Gemini response."
            )

        return result