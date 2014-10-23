import model
import csv

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
    # use u.item, tabular
    pass

def load_ratings(session):
    # use u.data, tabular
    # user_id     movie_id     rating     timestamp
    pass

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)

if __name__ == "__main__":
    s= model.connect()
    main(s)
