from enum import Enum
from typing import Optional

from pydantic import BaseModel, BaseSettings, SecretStr, validator


class Env(Enum):
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"


class UrlModel(BaseModel):
    url: str

    @validator("url", pre=True)
    def strip_trailing_slash(cls, v):
        return v.rstrip("/")

    def __str__(self):
        return self.url


class EODCSettings(BaseSettings):
    ENVIRONMENT: Env = Env.DEVELOPMENT
    BASE_URL: Optional[str] = None
    FAAS_URL: Optional[str] = None
    DASK_URL: Optional[str] = None
    CHILLER_URL: Optional[UrlModel] = UrlModel(url="https://chiller.eodc.eu/")
    API_KEY: Optional[SecretStr] = None

    @property
    def NAMESPACE(self):
        return "development" if self.ENVIRONMENT == Env.DEVELOPMENT else "production"


settings = EODCSettings()
