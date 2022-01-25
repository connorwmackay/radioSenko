from flask import Flask, render_template, url_for
from routes import routes
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from db import db

load_dotenv('.env')


def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@127.0.0.1:3306/{}'.format(
        os.getenv('DB_USER'), os.getenv('DB_PASS'), os.getenv('DB_NAME'))
    app.register_blueprint(routes)
    db.init_app(app)
    return app
