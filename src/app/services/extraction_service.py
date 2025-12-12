from google import genai
from google.genai import types
from app.schemas.assessment import DisruptionEvent
from app.core.config import settings
import logging

from typing import Optional, cast

class ExtractionError(Exception):
    pass

class IntelligentExtractionService:
    def __init__(self, project: Optional[str] = None, location: Optional[str] = None):
        self.project = project or settings.GOOGLE_CLOUD_PROJECT
        self.location = location or settings.GOOGLE_CLOUD_LOCATION
        self.client = genai.Client(vertexai=True, project=self.project, location=self.location)

    async def parse_snippet(self, text: str) -> DisruptionEvent:
        try:
            # Using Gemini 2.5 Flash as it is reliable and fast for this.
            response = await self.client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents=settings.EXTRACTION_PROMPT.format(text=text),
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
