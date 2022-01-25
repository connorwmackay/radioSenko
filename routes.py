from urllib import request
from flask import Blueprint, render_template, url_for, request

routes = Blueprint('routes', __name__)


@routes.route("/")
def index():
    url_for('static', filename='style.css')
    return render_template('index.jinja', track_src='#', track_title='Track Title')


@routes.route('/create-list', methods=('GET', 'POST'))
def create_list():
    url_for('static', filename='style.css')
    url_for('static', filename='create_list.css')
    url_for('static', filename='create_list.js')

    if request.method == 'POST':
        list_name = request.form["listName"]
        anime_list = request.form.getlist('animeList[]')
        print("List: {}".format(list_name))
        print(anime_list)

    return render_template('create_list.jinja')


@routes.route('/login', methods=('GET', 'POST'))
def login():
    url_for('static', filename='style.css')
    url_for('static', filename='login.css')
    return render_template('login.jinja')


@routes.route('/signup', methods=('GET', 'POST'))
def signup():
    url_for('static', filename='style.css')
    url_for('static', filename='signup.css')
    return render_template('signup.jinja')
