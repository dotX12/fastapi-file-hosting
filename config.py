from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    DB_USERNAME: str = Field(env='DB_USERNAME')
    DB_PASSWORD: str = Field(env='DB_PASSWORD')
    DB_PORT: int = Field(env='DB_PORT')
    DB_HOST: str = Field(env='DB_HOST')
    DB_BASENAME: str = Field(env='DB_BASENAME')

    @property
    def dsn(self):
        return (
            f"postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_BASENAME}"
        )

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings_app = Settings()
