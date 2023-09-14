from app import app, db, login_manager, bcrypt
from flask import render_template, session, redirect, url_for, request, jsonify
import functools

from .models import User
from .forms import LoginForm, CreateUserForm

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.username.data)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                session["username"] = form.username.data
                return redirect("/")
    return render_template("user_login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = CreateUserForm()
    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        user = User(username=username, password=bcrypt.generate_password_hash(password).decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        return redirect("/")
    return render_template("user_register.html", form=form)

@app.route("/logout", methods=["GET"])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/')
@login_required
def index():
    return render_template("index.html", title="Hello, world!")