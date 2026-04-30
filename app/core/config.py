from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # Cloudinary
    API_KEY: str
    API_SECRET: str
    CLOUD_NAME: str

    # Email
    RESEND_API_KEY: str
    MAIL_FROM_NAME: str

    #  Firebase
    FIREBASE_CREDENTIALS: str

    # App
    SECRET_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def DATABASE_URL(self) -> str:
        return f"{self.DATABASE_URL}"


settings = Settings()
