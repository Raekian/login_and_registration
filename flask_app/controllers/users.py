from flask_app.models.user import User
from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/home")
def homepage():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard_page():
    data = {
        "id" : session["user_id"]
    }
    user = User.get_one_user(data)
    print(user)
    return render_template("dashboard.html", user = user)

#============================
# creat user route
#============================

@app.route("/create_user", methods=["POST"])
def create_user():
    if not User.validate_user(request.form):
        return redirect("/home")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
    }
    new_user_id = User.create_user(data)
    session['user_id'] = new_user_id
    return redirect("/home")

#===========================
# login and logout routes
#===========================

@app.route("/login", methods=["POST"])
def login():
    data = {
        "email": request.form["loginEmail"]
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/home")

    if not bcrypt.check_password_hash(user_in_db.password, request.form['loginPassword']):
        flash("Invald Email/Password")
        return redirect("/home")

    session['user_id'] = user_in_db.id
    return redirect("/dashboard")


@app.route("/logout")
def user_logout():
    session.clear()
    return redirect("/home")