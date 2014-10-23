from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    name = Column(String(120), nullable = False)
    released_at = Column(DateTime, nullable = True)
    imdb_url = Column(String(120), nullable = True)

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer, nullable = False)
    user_id = Column(Integer, nullable = False)
    rating = Column(Integer, nullable = False)


### End class declarations

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
