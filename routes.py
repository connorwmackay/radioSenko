from urllib import request
from flask import Blueprint, render_template, url_for, request

routes = Blueprint('routes', __name__)


@routes.route('/create-list', methods=('GET', 'POST'))
def create_list():
    url_for('static', filename='create_list.css')
    url_for('static', filename='create_list.js')

    if request.method == 'POST':
        pass

    return render_template('create_list.html')
