from urllib import request
from flask import Blueprint, render_template, url_for, request, session, redirect, jsonify
import bcrypt
import base64
from db import newUser, User, new_list, List, new_list_item, ListItem
import uuid
import pytube
import glob
import ffmpeg
import os

routes = Blueprint('routes', __name__)


@routes.route("/")
def index():
    url_for('static', filename='style.css')

    username = None
    if 'username' in session:
        username = session['username']

        user = User.query.filter_by(username=username).first()
        lists = List.query.filter_by(user_id=user.id)
        list_names = []

        for list in lists:
            list_names.append({"uuid": list.uuid, "name": list.name})

    list_items = []
    list_query = request.args.get("list")
    if list_query:
        if list_query != "none":
            list_db = List.query.filter_by(
                uuid=list_query, user_id=user.id).first()
            list_items_db = ListItem.query.filter_by(list_id=list_db.id)
            for item in list_items_db:
                list_items.append(item.name)

    return render_template('index.jinja', username=username, list_names=list_names, list_items=list_items)


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


@routes.route('/radio/request/<track_name>/<op>')
def radio_request(track_name, op):
    yt_video = pytube.Search(track_name + op).results[0]
    target_stream = yt_video.streams.get_audio_only()
    file_name = "static/downloads/{}.mp4".format(track_name + op)

    if not os.path.isfile(file_name):
        target_stream.download(
            output_path="", filename=file_name, max_retries=1)
        return jsonify({})
    else:
        return jsonify({})
