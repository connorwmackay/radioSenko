from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

db = SQLAlchemy()


class User(db.Model):
    def __init__(self, username, email, passwordHash):
        self.username = username
        self.email = email
        self.passwordHash = passwordHash

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    passwordHash = db.Column(db.String(128), nullable=False)


def newUser(user: User):
    db.session.add(user)
    db.session.commit()


class List(db.Model):
    def __init__(self, name: str, uuid: str, user_id: int):
        self.name = name
        self.uuid = uuid
        self.user_id = user_id

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    uuid = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class ListItem(db.Model):
    def __init__(self, name: str, list_id: int):
        self.name = name
        self.list_id = list_id

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)


def new_list(list: List):
    db.session.add(list)
    db.session.commit()


def new_list_item(list_item: ListItem):
    db.session.add(list_item)
    db.session.commit()
