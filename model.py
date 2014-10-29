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

        other_movies = session.query(Movie).join(Movie.ratings).filter_by(user_id=self.id).all()

        similarities = [ (Movie.similarity(movie, m), m) for m in other_movies ]
        similarities.sort(reverse = True)
        similarities = [ sim for sim in similarities if sim[0] > 0 ]
        if not similarities:
            return None

        # starting from the beginning of the list, stop when you find a movie the user has rated
        sim, top_movie = similarities[0]
        for rating in top_movie.ratings:
            if self.id == rating.user_id:
                self_rating_of_other_movie = rating.rating
                break


        self_rating = self_rating_of_other_movie * sim
        self_rating = round(self_rating, 1)

        # error check for less than one instances
        if self_rating < 1:
            self_rating = 1

        return self_rating


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    name = Column(String(120), nullable = False)
    released_at = Column(DateTime, nullable = True)
    imdb_url = Column(String(120), nullable = True)

    def similarity(self, other_movie):

        movie_ratings = {}
        paired_ratings = []

        # loop through all the ratings for self (the movie in question)
        for rating in self.ratings:
            # get all the user_ids and their ratings for that movie (self)
            # dictionary key = user_id, value = rating, for self
            movie_ratings[rating.user_id] = rating.rating 

        # loop through all the ratings for the other movie (being compared to self)
        for rating in other_movie.ratings:

            # for each rating, if a user has rated this AND rated self (check dictionary),
            # store that rating in movie_rating
            movie_rating = movie_ratings.get(rating.user_id, False)

            # if movie_rating exists (there was a match - this user rated both self and other_movie)
            if movie_rating:
                # add the tuple of movie_rating (self rating, and other_movie's rating)
                paired_ratings.append( (movie_rating, rating.rating) )

        if paired_ratings:
            return correlation.pearson(paired_ratings)
        else:
            return 0.0

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
