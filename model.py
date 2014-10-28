from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
import correlation


ENGINE = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=ENGINE, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = session.query_property()


### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)

    def similarity(self, other):
        user_ratings = {}
        paired_ratings = []
        for rating in self.ratings:
            user_ratings[rating.movie_id] = rating

        for rating in other.ratings:
            user_rating = user_ratings.get(rating.movie_id)
            if user_rating:
                paired_ratings.append( (user_rating.rating, rating.rating) )

        if paired_ratings:
            return correlation.pearson(paired_ratings)
        else:
            return 0.0

    def predict_rating(self, movie):
        other_ratings = movie.ratings
        other_users = [ rating.user for rating in other_ratings ]
        similarities = [ (self.similarity(other_user), other_user) for other_user in other_users ]
        similarities.sort(reverse = True)
        top_user = similarities[0]
        matched_rating = None
        for rating in other_ratings:
            if rating.user_id == top_user[1].id:
                matched_rating = rating
                break

        # return the predicted rating: top_user's rating times top_user's similarity to user
        return matched_rating.rating * top_user[0]

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    name = Column(String(120), nullable = False)
    released_at = Column(DateTime, nullable = True)
    imdb_url = Column(String(120), nullable = True)

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable = False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = False)
    rating = Column(Integer, nullable = False)

    # adds attribute user to Rating class. adds attribute ratings to User class
    user = relationship("User", backref=backref("ratings", order_by=id))
    movie = relationship("Movie", backref=backref("ratings", order_by=id))

### End class declarations




def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
