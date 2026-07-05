import base64
import random
import uuid

from app.services.gemini_service import GeminiService


class Part2Service:
    """Generate TOEIC Speaking Part 2 prompts with a scene-specific illustration."""

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

        try:
            image_url = self.gemini.generate_image(
                f"Create a realistic TOEIC Speaking Part 2 picture of: {scenario}. "
                f"The image should look like a clear exam scene that a learner can describe in English."
            )
        except Exception as exc:
            print(f"Part 2 image generation fallback used: {exc}")
            image_url = self._build_scene_image(scenario, description)

        return {
            "id": str(uuid.uuid4())[:8],
            "part": 2,
            "task_type": "describe_a_picture",
            "instruction": "Describe the picture in one minute.",
            "preparation_time": 15,
            "response_time": 45,
            "text": description,
            "topic": "picture_description",
            "image_url": image_url,
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
        cleaned = (response or "").strip().strip("[]")
        return cleaned or "Describe the scene in the picture clearly and naturally."

    def _build_scene_image(self, scenario: str, description: str) -> str:
        combined = f"{scenario} {description}".lower()

        if any(keyword in combined for keyword in ["office", "meeting", "conference", "project"]):
            svg = """
<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='800'>
  <rect width='100%' height='100%' fill='#f8fafc'/>
  <rect x='60' y='60' width='1080' height='680' rx='24' fill='#ffffff' stroke='#cbd5e1' stroke-width='3'/>
  <rect x='120' y='150' width='420' height='250' rx='24' fill='#dbeafe'/>
  <rect x='620' y='170' width='360' height='220' rx='20' fill='#ecfeff'/>
  <rect x='180' y='320' width='220' height='120' rx='20' fill='#60a5fa'/>
  <rect x='700' y='240' width='180' height='90' rx='16' fill='#f59e0b'/>
  <circle cx='248' cy='240' r='70' fill='#fde68a'/>
  <rect x='220' y='430' width='280' height='140' rx='20' fill='#bfdbfe'/>
  <circle cx='315' cy='240' r='24' fill='#1f2937'/>
  <circle cx='745' cy='250' r='22' fill='#1f2937'/>
  <rect x='720' y='280' width='80' height='60' rx='12' fill='#1f2937'/>
</svg>
"""
        elif any(keyword in combined for keyword in ["library", "book", "study", "student"]):
            svg = """
<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='800'>
  <rect width='100%' height='100%' fill='#f8fafc'/>
  <rect x='60' y='60' width='1080' height='680' rx='24' fill='#ffffff' stroke='#cbd5e1' stroke-width='3'/>
  <rect x='120' y='140' width='420' height='260' rx='24' fill='#fef3c7'/>
  <rect x='620' y='180' width='360' height='220' rx='20' fill='#dcfce7'/>
  <rect x='180' y='320' width='220' height='120' rx='20' fill='#86efac'/>
  <rect x='720' y='220' width='180' height='120' rx='16' fill='#60a5fa'/>
  <rect x='180' y='470' width='280' height='130' rx='18' fill='#fde68a'/>
  <rect x='720' y='470' width='200' height='90' rx='16' fill='#1d4ed8'/>
  <rect x='160' y='200' width='40' height='100' rx='8' fill='#7c3aed'/>
  <rect x='220' y='200' width='40' height='100' rx='8' fill='#7c3aed'/>
</svg>
"""
        elif any(keyword in combined for keyword in ["restaurant", "dinner", "food", "meal"]):
            svg = """
<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='800'>
  <rect width='100%' height='100%' fill='#f8fafc'/>
  <rect x='60' y='60' width='1080' height='680' rx='24' fill='#ffffff' stroke='#cbd5e1' stroke-width='3'/>
  <rect x='120' y='160' width='420' height='260' rx='24' fill='#fff7ed'/>
  <circle cx='260' cy='260' r='70' fill='#fda4af'/>
  <rect x='650' y='180' width='320' height='220' rx='20' fill='#fee2e2'/>
  <rect x='180' y='440' width='260' height='120' rx='18' fill='#f59e0b'/>
  <rect x='700' y='430' width='200' height='90' rx='16' fill='#86efac'/>
  <circle cx='790' cy='240' r='36' fill='#fb923c'/>
</svg>
"""
        elif any(keyword in combined for keyword in ["park", "picnic", "tree", "grass"]):
            svg = """
<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='800'>
  <rect width='100%' height='100%' fill='#f8fafc'/>
  <rect x='60' y='60' width='1080' height='680' rx='24' fill='#ffffff' stroke='#cbd5e1' stroke-width='3'/>
  <rect x='120' y='150' width='400' height='260' rx='24' fill='#dcfce7'/>
  <circle cx='260' cy='250' r='70' fill='#fde68a'/>
  <circle cx='820' cy='245' r='90' fill='#86efac'/>
  <rect x='180' y='430' width='250' height='120' rx='18' fill='#f5f5f4'/>
  <path d='M760 180 L820 120 L880 180 Z' fill='#16a34a'/>
  <path d='M760 220 L820 160 L880 220 Z' fill='#22c55e'/>
</svg>
"""
        elif any(keyword in combined for keyword in ["bus", "stop", "rain", "umbrella"]):
            svg = """
<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='800'>
  <rect width='100%' height='100%' fill='#f8fafc'/>
  <rect x='60' y='60' width='1080' height='680' rx='24' fill='#ffffff' stroke='#cbd5e1' stroke-width='3'/>
  <rect x='160' y='160' width='420' height='250' rx='24' fill='#dbeafe'/>
  <rect x='660' y='180' width='260' height='170' rx='20' fill='#e2e8f0'/>
  <path d='M720 300 L820 300 L850 360 L700 360 Z' fill='#f59e0b'/>
  <path d='M710 220 L790 220 L820 300 L730 300 Z' fill='#1d4ed8'/>
  <rect x='220' y='460' width='220' height='100' rx='18' fill='#38bdf8'/>
  <path d='M800 180 L760 120 L780 120 L820 180 Z' fill='#0f172a'/>
</svg>
"""
        else:
            svg = """
<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='800'>
  <rect width='100%' height='100%' fill='#f8fafc'/>
  <rect x='60' y='60' width='1080' height='680' rx='24' fill='#ffffff' stroke='#cbd5e1' stroke-width='3'/>
  <circle cx='360' cy='320' r='120' fill='#fde68a'/>
  <rect x='620' y='220' width='290' height='180' rx='24' fill='#bfdbfe'/>
  <rect x='180' y='470' width='300' height='120' rx='20' fill='#bbf7d0'/>
  <circle cx='720' cy='310' r='54' fill='#f59e0b'/>
</svg>
"""

        encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")
        return f"data:image/svg+xml;base64,{encoded}"
