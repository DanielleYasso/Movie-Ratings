import model
import csv
from datetime import datetime

def load_users(session):
    # use u.user, separated by |
    # user_id | age | gender | occupation | zip_code
    f = open("seed_data/u.user")
    for line in f:
        user_data = line.strip().split("|")

        user_id, age, zip_code = user_data[0], user_data[1], user_data[4]
        new_user = model.User(id=user_id, age=age, zipcode=zip_code)

        session.add(new_user)

    # only commit once!  OTHERWISE IT WILL BE SLOW AS HELL
    session.commit()


def load_movies(session):
    # use u.item, |
    # movie id | movie title | release date | video release date |
              # IMDb URL | unknown | Action | Adventure | Animation |
              # Children's | Comedy | Crime | Documentary | Drama | Fantasy |
              # Film-Noir | Horror | Musical | Mystery | Romance | Sci-Fi |
              # Thriller | War | Western |
    f = open("seed_data/u.item")
    for line in f:
        movie_data = line.strip().split("|")

        movie_id, title, released, imdb = movie_data[0], movie_data[1], movie_data[2], movie_data[4]
        
        # creates a string that stores data as unicode, so we can use accent marks in titles
        title = title.split("(")[0]
        title = title.decode("latin-1")

        # convert date from string to datetime object
        released = released.replace("-", "")

        # Fixes error with empty string
        if released == "":
            new_movie = model.Movie(id=movie_id, name=title, imdb_url=imdb)
            session.add(new_movie)
            continue

        datetime_released = datetime.strptime(released, "%d%b%Y")
        
        new_movie = model.Movie(id=movie_id, name=title, released_at=datetime_released, imdb_url=imdb)

        session.add(new_movie)

    session.commit()


def load_ratings(session):
    # use u.data, tabular
    # user_id     movie_id     rating     timestamp
    f = open("seed_data/u.data")
    for line in f:
        rating_data = line.strip().split("\t")

        user_id, movie_id, rating = rating_data[0:3]
        new_rating = model.Rating(movie_id=movie_id, user_id=user_id, rating=rating)

        session.add(new_rating)

    session.commit()
        

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    load_ratings(session)
    load_movies(session)

if __name__ == "__main__":
    s= model.connect()
    main(s)
