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

# class List(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', nullable=False))


# class ListItem(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128), nullable=False)
#     list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)
