from urllib import request
from flask import Blueprint, render_template, url_for, request, session, redirect
import bcrypt
import base64
from db import newUser, User, new_list, List, new_list_item, ListItem
import uuid

routes = Blueprint('routes', __name__)


@routes.route("/")
def index():
    url_for('static', filename='style.css')

    username = None
    if 'username' in session:
        username = session['username']

    return render_template('index.jinja', username=username, track_src='#', track_title='Track Title')


@routes.route('/create-list', methods=('GET', 'POST'))
def create_list():
    url_for('static', filename='style.css')
    url_for('static', filename='create_list.css')
    url_for('static', filename='create_list.js')

    username = None
    if 'username' in session:
        username = session['username']

    if request.method == 'POST':
        list_name = request.form["listName"]
        anime_list = request.form.getlist('animeList[]')
        user = User.query.filter_by(username=username).first()
        if user:
            random_uuid = uuid.uuid4()
            new_list(List(list_name, random_uuid, user.id))

            for anime in anime_list:
                list_inst = List.query.filter_by(
                    uuid=random_uuid).first()
                new_list_item(ListItem(anime, list_inst.id))

    return render_template('create_list.jinja', username=username)


@routes.route('/login', methods=('GET', 'POST'))
def login():
    url_for('static', filename='style.css')
    url_for('static', filename='login.css')

    is_login_done = False
    password_check = False
    username = ''

    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        is_login_done = True

        if user:
            password_check = bcrypt.checkpw(password.encode(
                'utf-8'), bytes.fromhex(user.passwordHash))
            session['username'] = username
            return redirect(url_for('routes.index'))

    if 'username' in session:
        username = session['username']

    return render_template('login.jinja', is_logged_in=password_check, username=username, is_login_done=is_login_done)


@routes.route('/signup', methods=('GET', 'POST'))
def signup():
    url_for('static', filename='style.css')
    url_for('static', filename='signup.css')

    if request.method == 'POST':
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        print("New User: {}, {}, {}".format(username, email, password))
        # Hash Password
        hashedPassword = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        print("Hashed Password:", hashedPassword)

        newUser(User(username, email, hashedPassword.hex()))

    username = None
    if 'username' in session:
        username = session['username']

    return render_template('signup.jinja', username=username)


@routes.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('routes.index'))
