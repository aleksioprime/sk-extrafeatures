from app import app, db, login_manager, bcrypt
from flask import render_template, session, redirect, url_for, request
import functools

from .models import User
from .forms import LoginForm, CreateUserForm

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(form.email.data)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                session["email"] = user.email
                session["id"] = user.id
                session["username"] = f"{ user.first_name } { user.last_name }"
                return redirect("/")
    return render_template("user_login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = CreateUserForm()
    if form.validate_on_submit():
        password = request.form.get('password')
        user = User(email=request.form.get('email'),
                    password=bcrypt.generate_password_hash(password).decode('utf-8'),
                    first_name=request.form.get('first_name'),
                    last_name=request.form.get('last_name'))
        db.session.add(user)
        db.session.commit()
        return redirect("/")
    return render_template("user_register.html", form=form)

@app.route("/logout", methods=["GET"])
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/')
@login_required
def index():
    return render_template("index.html", title="Главная страница")

@app.route('/dnevnik_reports')
@login_required
def dnevnik_reports():
    user = User.query.filter_by(id=session["id"]).first()
    return render_template("dnevnik_reports.html", title="Формирование выписки для студента", user = user)

@app.route('/other_reports')
@login_required
def other_reports():
    user = User.query.filter_by(id=session["id"]).first()
    return render_template("other_reports.html", title="Формирование выписки для студента", user = user)


