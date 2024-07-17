\\from flask import Flask, render_template, request, g, flash, abort, redirect, session, url_for
import os
import sqlite3
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = '/tmp/mm.db'
DEBUG = True
SECRET_KEY = 'fd4sdg56yrhdasu6d33gsfs'

title = ["Главная", "Регистрация", "Войти", "Каталог", "Профиль"]
menu = [
    {"name": "Главная", "url": "/"},
    {"name": "Каталог", "url": "catalog"},
    {"name": "Войти", "url": "login"},
    {"name": "Регистрация", "url": "register"},
    {"name": "Профиль", "url": "profile"}
]

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'mm.db')))

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route("/")
def index():
    return render_template('index.html', title=title[0], menu=menu)

@app.route("/profiledetails")
def portfoliodetails():
    return render_template('profile-details.html')

@app.route("/catalog")
def catalog():
    return render_template('catalog.html', title=title[3], menu=menu)

@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    
    if request.method == 'POST':
        user = dbase.getUserByEmail(request.form['username']) # type: ignore
        if user and check_password_hash(user['password_hash'], request.form['password']):
            session['userLogged'] = user['username']
            flash('Вы успешно вошли в систему', 'success')
            return redirect(url_for('profile', username=user['username']))
        else:
            flash('Неправильное имя пользователя или пароль', 'error')

    return render_template('login.html', title=title[2], menu=menu)

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        if len(request.form['username']) > 4 and len(request.form['email']) > 4 \
                and len(request.form['password_hash']) > 4 and request.form['password_hash'] == request.form['password_hash2']:
            hash = generate_password_hash(request.form['password_hash'])
            res = dbase.addUser(request.form['username'], request.form['email'], hash) # type: ignore
            if res:
                flash("Вы зарегистрировались", "success")
                return redirect(url_for('login'))
            else:
                flash("Ошибка регистрации", "error")
    return render_template('register.html', title=title[1], menu=menu)

@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return render_template('profile.html', title=title[4], menu=menu, username=username)

if __name__ == "__main__":
    app.run(debug=True)
