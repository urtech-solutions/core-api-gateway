from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    device_registry_url: str = "http://localhost:8001"
    telemetry_api_url: str = "http://localhost:8002"
    jwt_secret: str = "change-me"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        case_sensitive=False,
    )


settings = Settings()
