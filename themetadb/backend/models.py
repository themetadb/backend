from typing import Iterable

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime  # noqa: F401
from sqlalchemy.orm import relationship, RelationshipProperty
from sqlalchemy_utils.types import URLType  # type: ignore

from .database import Base


class ExternalProvider(Base):
    __tablename__ = 'external_provider'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    url = Column(URLType, nullable=False, unique=True)

    movies: Iterable['Movie'] = relationship("ExternalProviderId", back_populates="provider")

    def __repr__(self):
        return '<{} {} {}>'.format(self.__class__.__name__, self.name, self.url)


class ExternalProviderId(Base):
    # https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#association-object
    __tablename__ = 'external_provider_id'

    movie_id = Column(Integer, ForeignKey('movie.id'), primary_key=True)
    provider_id = Column(Integer, ForeignKey('external_provider.id'), primary_key=True)

    id = Column(String(32))

    movie: RelationshipProperty = relationship("Movie", back_populates="providers")
    provider: RelationshipProperty = relationship("ExternalProvider", back_populates="movies")

    def __repr__(self):
        return '<{} {} {}>'.format(self.__class__.__name__, self.provider.name, self.id)


class Movie(Base):
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    year = Column(Integer)
    external_ids: Iterable[ExternalProviderId] = relationship("ExternalProviderId", back_populates="movie")

    def __repr__(self):
        return '<{} {} ({})>'.format(self.__class__.__name__, self.name, self.year)
