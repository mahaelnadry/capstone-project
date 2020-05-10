import os
from sqlalchemy import Column, String, Integer, Date, ForeignKey, create_engine, Table
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json
# to read environment variables from heroku
from boto.s3.connection import S3Connection

SQLALCHEMY_ECHO = False
'''
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/castingAgency'
SQLALCHEMY_TRACK_MODIFICATIONS=False
'''

SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ["SQLALCHEMY_TRACK_MODIFICATIONS"]
# SQLALCHEMY_ECHO=os.environ["SQLALCHEMY_ECHO"]

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["SQLALCHEMY_ECHO"] = SQLALCHEMY_ECHO
    db.app = app
    db.init_app(app)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
Association table between Movie and Actor resulted from the many to many relationship between them
'''


class Movie_Actor(db.Model):
    __tablename__ = 'movies_actors'
    movie_id = Column(Integer, ForeignKey('movies.id'), primary_key=True)
    actor_id = Column(Integer, ForeignKey('actors.id'), primary_key=True)


'''
Movie

'''


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    release_date = Column(Date)
    # many to many relationship
    actors = relationship(
        'Actor', secondary='movies_actors', back_populates='movies')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }


'''
Actor

'''


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    # many to many relationship
    movies = relationship(
        'Movie', secondary='movies_actors', back_populates='actors')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }
