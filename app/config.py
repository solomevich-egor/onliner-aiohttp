from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGO_HOST: SecretStr
    MONGO_PORT: SecretStr
    MONGO_USER: SecretStr
    MONGO_PASS: SecretStr
    MONGO_DB: SecretStr

    model_config = SettingsConfigDict(env_file=".env.dev", env_file_encoding="utf-8")


settings = Settings()
