from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GIGACHAT_AUTH: str
    TG_BOT_TOKEN: str

    class Config:
        env_file = '.env'

settings = Settings()