from google import genai
from google.genai import types
from app.schemas.assessment import DisruptionEvent
from app.core.config import settings
import logging

from typing import Optional, cast

class ExtractionError(Exception):
    pass

class IntelligentExtractionService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GOOGLE_API_KEY
        self.client = genai.Client(api_key=self.api_key)

    async def parse_snippet(self, text: str) -> DisruptionEvent:
        try:
            # Using Gemini 1.5 Flash as it is reliable and fast for this.
            response = await self.client.aio.models.generate_content(
                model="gemini-1.5-flash",
                contents=f"Analyze this news snippet and extract supply chain disruption details:\n\n{text}",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=DisruptionEvent
                )
            )
            
            if response.parsed:
                 return cast(DisruptionEvent, response.parsed)
            
            # Fallback validation if parsed is not populated (though it should be)
            if response.text:
                return DisruptionEvent.model_validate_json(response.text)
                
            raise ExtractionError("Empty response from AI")

        except Exception as e:
            logging.error(f"AI Extraction failed: {e}")
            raise ExtractionError(f"AI Extraction failed: {str(e)}")
