from sqlalchemy.orm import Session

from app.modules.movies.model import Movie


def get_by_id(db: Session, entity_id: int) -> Movie | None:
    return db.query(Movie).filter(Movie.id == entity_id).first()


def get_by_name(db: Session, name: str) -> list[Movie]:
    return db.query(Movie).filter(Movie.title.ilike(f"%{name}%")).all()


def get_all(db: Session) -> list[Movie]:
    return db.query(Movie).all()


def create(db: Session, movie: Movie) -> Movie:
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie
