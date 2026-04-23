from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    # Cloudinary
    API_KEY: str
    API_SECRET: str
    CLOUD_NAME: str

    # Email
    MAIL_USERNAME: str | None = None
    MAIL_PASSWORD: str | None = None
    MAIL_FROM: str | None = None
    MAIL_FROM_NAME: str | None = None
    MAIL_PORT: int = 587
    MAIL_SERVER: str | None = None
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS : bool = False

    # App
    SECRET_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?sslmode=require"
        )


settings = Settings()