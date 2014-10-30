from flask import Flask, render_template, redirect, request, flash, session, g
import model

app = Flask(__name__)
app.secret_key = "ABC"


@app.before_request
def check_login():
    user_id = session.get('user_id')
    if user_id:
        g.user = model.session.query(model.User).get(user_id)
    else:
        g.user = None

@app.route("/")
def index():
    return render_template("index.html")
    # user_list = model.session.query(model.User).limit(5).all()
    # return render_template("user_list.html", users=user_list)

@app.route("/login_form")
def login_form():
    return render_template("login.html")

@app.route("/signup_form")
def signup_form():
    return render_template("signup_form.html")

@app.route("/signup", methods=["POST"])
def user_signup():
    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")


    # ERROR CHECKING
    if not email:
        flash("Please enter a valid email address")
        return redirect("/signup_form")
    if not password:
        flash("Please enter a password")
        return redirect("/signup_form")
    if not age.isdigit():
        flash("Please type a numeric age")
        return redirect("/signup_form")
    if len(zipcode) != 5 or not zipcode.isdigit():
        flash ("Please type a valid 5 digit zipcode")
        return redirect("/signup_form")

    # check for email
    u = model.session.query(model.User).filter(model.User.email==email).first()

    # if exists, ask if they want to login
    if u:
        flash("User already exists! LOGIN DAMMIT")
        return redirect("/signup_form")
    # if doesn't exist, add user info to database as new user
    else:
        u = model.User()
        u.email = email
        u.password = password
        u.age = age
        u.zipcode = zipcode
        model.session.add(u)
        model.session.commit()
        
        session["user_email"] = u.email
        session["user_id"] = str(u.id)
        print session
        flash("Successfully signed up!")


    return redirect("/")

@app.route("/login", methods=["POST"])
def user_login():
    email = request.form.get("email")
    password = request.form.get("password")
    u = model.session.query(model.User).filter_by(email = email).filter_by(password = password).first()
    if u:
        flash("Login successful")
        session["user_email"] = u.email
        session["user_id"] = str(u.id)
        print session
        return redirect("/")
    else:
        flash("Email/password not valid, please try again.")
        return redirect("/login_form")

@app.route("/logout")
def user_logout():
    session["user_email"] = None
    session["user_id"] = None
    flash("Logout successful")
    print session
    return redirect("/")

@app.route("/get_user_list")
def get_user_list():
    # user_list = model.session.query(model.User).limit(10).all()
    user_list = model.session.query(model.User).filter(model.User.id>=935).all()
    # for extra_user in extra_users:
        # user_list.append(extra_user)
    # extra_user = model.session.query(model.User).filter_by(id=945).first()
    # user_list.append(extra_user)

    return render_template("user_list.html", users=user_list)

@app.route("/display_user_info")
def display_user_info():
    user = request.args.get("user")
    user_ratings = model.session.query(model.Rating).filter_by(user_id = user).all()

    return render_template("user_info.html", user_ratings = user_ratings, user = user)

@app.route("/get_movie_list")
def get_movie_list():
    movie_list = model.session.query(model.Movie).limit(20).all()
   
    return render_template("movie_list.html", movies=movie_list)

@app.route("/movie/<int:id>")
def view_movie(id):
    movie = model.session.query(model.Movie).get(id)
    ratings = movie.ratings
    rating_nums = []
    user_rating = None
    prediction = None
    beratement = None
    for r in ratings:
        if g.user and r.user_id == g.user.id:
            user_rating = r.rating
        rating_nums.append(r.rating)
    avg_rating = round(float(sum(rating_nums))/len(rating_nums), 1)

    if g.user:
        # Prediction code: only predict if the user hasn't rated it
        # user = model.session.query(User).get(session["user_id"])
        prediction = None
        if not user_rating:
            prediction = g.user.predict_rating(movie)
            effective_rating = prediction
        else:
            effective_rating = user_rating
        # End prediction

        # THE EYE
        the_eye = model.session.query(model.User).filter_by(email="theeye@ofjudgement.com").one()
        eye_rating = model.session.query(model.Rating).filter_by(user_id=the_eye.id, movie_id=movie.id).first()

        if not eye_rating:
            eye_rating = the_eye.predict_rating(movie)
        else:
            eye_rating = eye_rating.rating

        difference = abs(eye_rating - effective_rating)

        messages = [ "Brother from another mother? Sister from another mister? I LOVE YOU!",
                     "You're almost perfect. Not really. You suck.",
                     "Fuckkkk youuuuuuu.",
                     "You're dead to me.",
                     "Really??? Why don't you just take your movie ticket and use it to slit your own throat." ]

        beratement = messages[int(difference)]

    # so we can pass to movie_list, which requires a list
    movies = [movie]

    return render_template("movie_list.html", movies=movies, average=avg_rating, user_rating=user_rating, 
        prediction=prediction, beratement=beratement)

@app.route("/update_movie_rating", methods=["POST"])
def update_movie_rating():
    # user_id in session
    movie_id = request.args.get("movie")
    rating = request.form.get("rating")
    url = "/movie/%s" % movie_id

    if not rating.isdigit():
        flash("Please type a number 1-5")
        return redirect(url)
    elif not 1 <= int(rating) <= 5:
        flash("Please type a number between 1 and 5")
        return redirect(url)
    user_id = session["user_id"]
    # print movie_id
    # print rating
    rating_record = model.session.query(model.Rating).filter_by(user_id = user_id).filter_by(movie_id = movie_id).first()
    
    if rating_record:
        rating_record.rating = rating
        flash("Your rating has been updated.")
    else:
        r = model.Rating()
        r.user_id = user_id
        r.movie_id = movie_id
        r.rating = rating
        model.session.add(r)
        flash("Your rating has been added.")

    model.session.commit()

    return redirect(url)






if __name__ == "__main__":
    app.run(debug = True)