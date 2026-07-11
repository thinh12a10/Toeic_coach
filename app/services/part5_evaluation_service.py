from app.services.gemini_service import GeminiService


class Part5EvaluationService:

    PRONUNCIATION_WEIGHT = 0.4
    ORGANIZATION_WEIGHT = 0.3
    DELIVERY_WEIGHT = 0.3

    def __init__(self):
        self.gemini = GeminiService()

    def evaluate(self, original_text: str, audio_bytes: bytes):
        prompt = self._build_prompt(original_text)
        result = self.gemini.generate_json(audio_bytes, prompt, self._response_schema())

        total_score = (
            result["pronunciation"]["score"] * self.PRONUNCIATION_WEIGHT
            + result["organization"]["score"] * self.ORGANIZATION_WEIGHT
            + result["delivery"]["score"] * self.DELIVERY_WEIGHT
        )

        result["total_score"] = round(total_score, 1)
        return result

    def _build_prompt(self, original_text: str) -> str:
        return f"""
You are a professional TOEIC Speaking examiner.

PART:
TOEIC Speaking Part 5 - Express an Opinion

Original Text:
{original_text}

Evaluate the AUDIO recording.

Evaluation Criteria:
1. Essay-like structure: introduction, body with reasons/examples, conclusion
2. Persuasive logic and clarity of opinion
3. Advanced vocabulary and grammar
4. Pronunciation
5. Intonation, stress, and pacing

Identify:
- Mispronounced words
- Missing words
- Added words
- Grammar issues
- Weak structure or missing conclusion
- Weak persuasive logic
- Limited vocabulary
- Stress and intonation issues
- Fluency issues

For every weakness:
- Explain the issue
- Explain why it affects TOEIC score
- Give practical improvement advice

Scoring:
0-10

Return JSON only.
"""

    def _response_schema(self):
        category_schema = {
            "type": "object",
            "properties": {
                "score": {"type": "number"},
                "strengths": {"type": "array", "items": {"type": "string"}},
                "weaknesses": {"type": "array", "items": {"type": "string"}},
                "improvement_tips": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["score", "strengths", "weaknesses", "improvement_tips"],
        }

        pronunciation_schema = {
            "type": "object",
            "properties": {
                "score": {"type": "number"},
                "strengths": {"type": "array", "items": {"type": "string"}},
                "weaknesses": {"type": "array", "items": {"type": "string"}},
                "mispronounced_words": {"type": "array", "items": {"type": "string"}},
                "missing_words": {"type": "array", "items": {"type": "string"}},
                "added_words": {"type": "array", "items": {"type": "string"}},
                "missing_end_sounds": {"type": "array", "items": {"type": "string"}},
                "vowel_issues": {"type": "array", "items": {"type": "string"}},
                "stress_issues": {"type": "array", "items": {"type": "string"}},
                "improvement_tips": {"type": "array", "items": {"type": "string"}},
            },
            "required": [
                "score",
                "strengths",
                "weaknesses",
                "mispronounced_words",
                "missing_words",
                "added_words",
                "missing_end_sounds",
                "vowel_issues",
                "stress_issues",
                "improvement_tips",
            ],
        }

        return {
            "type": "object",
            "properties": {
                "pronunciation": pronunciation_schema,
                "organization": category_schema,
                "delivery": category_schema,
                "overall_feedback": {"type": "string"},
                "study_plan": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["pronunciation", "organization", "delivery", "overall_feedback", "study_plan"],
        }
