from typing import List

from fastapi import Depends, FastAPI, HTTPException
# from fastapi.responses import JSONResponse, HTMLResponse
# from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import get_db

app = FastAPI()

# app.mount("/static", StaticFiles(packages=['themetadb.backend']), name="static")


@app.get('/movies', response_model=List[schemas.Movie])
def read_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_movies(db, skip=skip, limit=limit)


@app.post("/movies", response_model=schemas.Movie, status_code=201)
def create_movie(movie: schemas.Movie, db: Session = Depends(get_db)):
    db_name = crud.get_movie_by_name(db, name=movie.name)
    if db_name:
        raise HTTPException(status_code=400, detail="Movie with name already exists")
    return crud.create_movie(db, movie=movie)


@app.get("/movie/{movie_id}", response_model=schemas.Movie)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = crud.get_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie


@app.delete("/movie/{movie_id}", response_model=schemas.Movie)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie_obj = crud.delete_movie(db, movie=movie_id)
    if movie_obj is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie_obj
