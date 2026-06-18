from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DATABASE_URL: str
    API_KEY: str
    API_SECRET: str
    CLOUD_NAME: str
    RESEND_API_KEY: str
    MAIL_FROM_NAME: str
    FIREBASE_CREDENTIALS: str
    GOOGLE_CLIENT_ID: str
    SECRET_KEY: str
    ALLOWED_ORIGINS: str = "*"


settings = Settings()
