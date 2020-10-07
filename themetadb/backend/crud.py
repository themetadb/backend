from typing import Optional, Iterable, Union, cast

from sqlalchemy.orm import Session

from . import models, schemas


def get_movie(db: Session, movie_id: int) -> Optional[models.Movie]:
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()


def get_movie_by_name(db: Session, name: str) -> Optional[models.Movie]:
    return db.query(models.Movie).filter(models.Movie.name == name).first()


def get_movies(db: Session, skip: int = 0, limit: int = 100) -> Iterable[models.Movie]:
    return db.query(models.Movie).offset(skip).limit(limit).all()


def create_movie(db: Session, movie: schemas.Movie) -> Optional[models.Movie]:
    db_movie = models.Movie(name=movie.name, year=movie.year)

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    return db_movie


def delete_movie(db: Session, movie: Union[models.Movie, schemas.Movie, int], commit: bool = True) -> Optional[schemas.Movie]:
    if isinstance(movie, schemas.Movie):
        movie_model = get_movie(db, cast(int, movie.id))
    elif isinstance(movie, int):
        movie_model = get_movie(db, movie)
    elif isinstance(movie, models.Movie):
        movie_model = movie
    else:
        raise TypeError

    movie_obj = schemas.Movie.from_orm(movie_model)

    if movie_model is None:
        return None

    db.delete(movie_model)

    if commit:
        db.commit()

    return movie_obj
