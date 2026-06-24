import os

from dotenv import load_dotenv
from google import genai
import json
from google.genai import types

class GeminiService:

    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not set."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.default_model = "gemini-2.5-flash"

    def generate(
        self,
        prompt: str,
        model: str | None = None
    ) -> str:

        model_name = model or self.default_model

        response = self.client.models.generate_content(
            model=model_name,
            contents=prompt
        )

        return response.text.strip()
    
    def generate_json(
        self,
        prompt: str,
        response_schema: dict
    ):

        response = self.client.models.generate_content(
            model=self.default_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                response_mime_type="application/json",
                response_schema=response_schema
            )
        )

        return json.loads(
            response.text
        )