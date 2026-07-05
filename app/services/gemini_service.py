import base64
import json
import os
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.utils.config import EVALUATION_MODELS, IMAGE_GENERATION_MODELS, TEXT_GENERATOR_MODELS


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
                text = getattr(response, "text", None)
                if text:
                    return text.strip()
                raise RuntimeError("Gemini returned an empty response.")
            except Exception as exc:
                last_error = exc
                print(f"Error with model {model}: {exc}")

        raise RuntimeError(f"Failed to generate content: {last_error}")

    def generate_image(self, prompt: str) -> str:
        if not self.client:
            raise RuntimeError("Gemini API is not available. Please configure GEMINI_API_KEY.")

        last_error = None
        for model in IMAGE_GENERATION_MODELS:
            try:
                print(f"Trying to generate image with model: {model}")
                response = self.client.models.generate_images(
                    model=model,
                    prompt=prompt,
                    config=types.GenerateImagesConfig(
                        number_of_images=1,
                        output_mime_type="image/jpeg",
                        output_compression_quality=90,
                    ),
                )
                generated_image = response.generated_images[0].image
                image_bytes = generated_image.image_bytes
                if image_bytes:
                    encoded = base64.b64encode(image_bytes).decode("ascii")
                    return f"data:image/jpeg;base64,{encoded}"
                raise RuntimeError("Gemini returned an empty image payload.")
            except Exception as exc:
                last_error = exc
                print(f"Error with image model {model}: {exc}")

        raise RuntimeError(f"Failed to generate image: {last_error}")

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