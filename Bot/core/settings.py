import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    bot_token: str
    openai_api_key: str
    assistant_id:str

    class Config:
        env_file = '.env'

settings = Settings()