import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    bot_token: str
    openai_api_key: str

    class Config:
        env_file = '.env'

settings = Settings()