from flask import Flask, render_template, redirect, request, flash, session
import model

app = Flask(__name__)
app.secret_key = "ABC"

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
        session["user"] = u.email
        flash("Successfully signed up!")

    return redirect("/")

@app.route("/login", methods=["POST"])
def user_login():
    email = request.form.get("email")
    password = request.form.get("password")
    u = model.session.query(model.User).filter(model.User.email == email).filter(model.User.password == password).first()
    if u:
        flash("Login successful")
        session["user"] = u.email
        print session
        return redirect("/")
    else:
        flash("Email/password not valid, please try again.")
        return redirect("/login_form")

@app.route("/logout")
def user_logout():
    session["user"] = None
    flash("Logout successful")
    print session["user"]
    return redirect("/")







if __name__ == "__main__":
    app.run(debug = True)