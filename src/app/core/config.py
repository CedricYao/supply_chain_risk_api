from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    GOOGLE_CLOUD_PROJECT: str
    GOOGLE_CLOUD_LOCATION: str
    EXTRACTION_PROMPT: str = (
        "Analyze this news snippet and extract supply chain disruption details. "
        "For the 'target_port' field, extract ONLY the city/location name (e.g., use 'Rotterdam' instead of 'Port of Rotterdam'). "
        "Return valid JSON matching the schema.\n\n{text}"
    )
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Pydantic Settings loads values from environment variables, but Mypy expects arguments for required fields.
settings = Settings() # type: ignore[call-arg]
