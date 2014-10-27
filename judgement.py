from flask import Flask, render_template, redirect, request, flash
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
        return render_template("signup_form.html")
    # if doesn't exist, add user info to database as new user
    else:
        u = model.User()
        u.email = email
        u.password = password
        u.age = age
        u.zipcode = zipcode
        model.session.add(u)
        model.session.commit()
        flash("Successfully signed up!")

    return redirect("/")






if __name__ == "__main__":
    app.run(debug = True)