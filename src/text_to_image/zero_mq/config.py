import logging
from pydantic_settings import BaseSettings, SettingsConfigDict

"""
This should read from os.envir automatically


"""

class Config(BaseSettings):
    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env`
        env_file=('.env.example', '.env'),
        env_file_encoding="utf-8"
    )

    host: str = "*"
    port: str = '8672'
    loglevel: str = 'info'

