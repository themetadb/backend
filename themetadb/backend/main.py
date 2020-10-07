# from sqlalchemy_utils import database_exists

from .app import app
from .database import engine, Base


def main():
    Base.metadata.create_all(bind=engine)

    return app


main()
