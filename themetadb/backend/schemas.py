from typing import Optional, Dict, Any, List, cast

from sqlalchemy import String
from pydantic import BaseModel
from pydantic.fields import ModelField, Field
from furl import furl  # type: ignore

from . import models


class Url(furl):
    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        field_schema.update(type='string', format='uri')

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field: ModelField):
        return furl(v).url


class ExternalProvider(BaseModel):
    id: int  # 1
    slug: str  # imdb
    name: str  # IMDb
    url: Optional[Url]  # https://www.imdb.com/


class ExternalProviderId(BaseModel):
    provider: ExternalProvider  # imdb
    id: str  # tt0133093


class Movie(BaseModel):
    id: Optional[int]
    name: str = Field(..., max_length=cast(String, models.Movie.name.type).length)
    year: Optional[int]

    external_ids: List[ExternalProviderId]

    class Config:
        orm_mode = True
