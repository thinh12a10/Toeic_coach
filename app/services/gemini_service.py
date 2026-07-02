import json
import os
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.utils.config import EVALUATION_MODELS, TEXT_GENERATOR_MODELS


class GeminiService:

    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")

        self.client = None
        self.default_model = "gemini-2.5-flash"

        if not api_key:
            print("GEMINI_API_KEY is not set. Gemini features will be unavailable.")
            return

        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt: str) -> str:
        if not self.client:
            raise RuntimeError("Gemini API is not available. Please configure GEMINI_API_KEY.")

        last_error = None
        for model in TEXT_GENERATOR_MODELS:
            try:
                print(f"Trying to generate text with model: {model}")
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                )
                return response.text.strip()
            except Exception as exc:
                last_error = exc
                print(f"Error with model {model}: {exc}")

        raise RuntimeError(f"Failed to generate content: {last_error}")

    def generate_json(
        self,
        audio_bytes: bytes,
        prompt: str,
        response_schema: dict[str, Any],
    ):
        if not self.client:
            raise RuntimeError("Gemini API is not available. Please configure GEMINI_API_KEY.")

        last_error = None
        for model in EVALUATION_MODELS:
            try:
                print(f"Trying to generate JSON with model: {model}")
                response = self.client.models.generate_content(
                    model=model,
                    contents=[
                        types.Part.from_bytes(
                            data=audio_bytes,
                            mime_type="audio/webm",
                        ),
                        prompt,
                    ],
                    config=types.GenerateContentConfig(
                        temperature=0.2,
                        response_mime_type="application/json",
                        response_schema=response_schema,
                    ),
                )
                return json.loads(response.text)
            except Exception as exc:
                last_error = exc
                print(f"Error with model {model}: {exc}")

        raise RuntimeError(f"Failed to generate evaluation JSON: {last_error}")