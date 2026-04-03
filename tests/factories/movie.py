from datetime import date

from factory import Faker
from factory.alchemy import SQLAlchemyModelFactory

from app.models.movie import Movie


class MovieFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Movie
        sqlalchemy_session_persistence = "flush"

    title = Faker("sentence")
    description = Faker("paragraph")
    genre = Faker("word")
    director = Faker("name")
    critic_rating = Faker("random_int", min=1, max=5)
    age_rating = "PG-13"
    release_date = date(1999, 3, 31)
    copies_available = Faker("random_int", min=0, max=50)
    rental_price = Faker("pyfloat", min_value=0.99, max_value=5.99, right_digits=2)
    is_active = True
