import base64
import random
import uuid

from app.services.gemini_service import GeminiService


class Part2Service:
    """Generate TOEIC Speaking Part 2 prompts with a simple placeholder image."""

    SCENARIOS = [
        "A busy office meeting room with people discussing a project.",
        "A family having dinner together at a restaurant.",
        "A student studying in a library with many books around.",
        "A group of friends enjoying a picnic in a park.",
        "A man and a woman waiting at a bus stop during the rain.",
    ]

    def __init__(self):
        self.gemini = GeminiService()

    def generate_question(self) -> dict:
        scenario = random.choice(self.SCENARIOS)
        prompt = self._build_prompt(scenario)

        try:
            response = self.gemini.generate(prompt)
            description = self._parse_response(response)
        except Exception as exc:
            description = f"Describe the scene in this picture. {scenario}"
            print(f"Part 2 generation fallback used: {exc}")

        return {
            "id": str(uuid.uuid4())[:8],
            "part": 2,
            "task_type": "describe_a_picture",
            "instruction": "Describe the picture in one minute.",
            "preparation_time": 15,
            "response_time": 45,
            "text": description,
            "topic": "picture_description",
            "image_url": self._build_placeholder_image(scenario),
        }

    def _build_prompt(self, scenario: str) -> str:
        return f"""
Create a natural TOEIC Speaking Part 2 prompt for describing a picture.
Scenario: {scenario}
Requirements:
- One sentence describing the image clearly.
- Suitable for a speaking practice prompt.
- No bullet points.
Return a single sentence only.
"""

    def _parse_response(self, response: str) -> str:
        cleaned = response.strip().strip("[]")
        return cleaned or "Describe the scene in the picture clearly and naturally."

    def _build_placeholder_image(self, scenario: str) -> str:
        safe_text = scenario.replace("'", "&#39;")
        svg = f"""
<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='800'>
  <rect width='100%' height='100%' fill='#f8fafc'/>
  <rect x='40' y='40' width='1120' height='720' rx='24' fill='#ffffff' stroke='#cbd5e1' stroke-width='3'/>
  <rect x='90' y='120' width='420' height='260' rx='20' fill='#dbeafe'/>
  <rect x='620' y='140' width='420' height='240' rx='20' fill='#dcfce7'/>
  <circle cx='260' cy='250' r='70' fill='#fde68a'/>
  <rect x='180' y='320' width='160' height='120' rx='20' fill='#60a5fa'/>
  <rect x='700' y='220' width='220' height='110' rx='20' fill='#f9a8d4'/>
  <rect x='950' y='220' width='80' height='110' rx='20' fill='#86efac'/>
  <text x='600' y='520' text-anchor='middle' font-family='Arial, sans-serif' font-size='28' fill='#1e3a8a'>Picture prompt for TOEIC Speaking Part 2</text>
  <text x='600' y='565' text-anchor='middle' font-family='Arial, sans-serif' font-size='22' fill='#475569'>{safe_text}</text>
</svg>
"""
        encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")
        return f"data:image/svg+xml;base64,{encoded}"
