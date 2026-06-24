import os

from dotenv import load_dotenv
from google import genai
import json
from google.genai import types
from app.utils.config import TEXT_GENERATOR_MODELS

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
    ) -> str:

        for model in TEXT_GENERATOR_MODELS:
            try:
                print(f"Trying to generate text with model: {model}")
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt
                )
                break  # Exit the loop if the request is successful
            except Exception as e:
                print(f"Error with model {model}: {e}")

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