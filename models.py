import os
from sqlalchemy import Column, String, Integer,Date, ForeignKey, create_engine, Table
#from sqlalchemy import *
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json
import config



db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
  app.config["SQLALCHEMY_DATABASE_URI"] =config.SQLALCHEMY_DATABASE_URI
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
  app.config["SQLALCHEMY_ECHO"]=config.SQLALCHEMY_ECHO
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

  
# association table
#movies_actors = db.Table('movies_actors', Base.metadata,
#Column('movie_id', db.ForeignKey('movies.id'), primary_key=True),
#Column('actor_id', db.ForeignKey('actors.id'), primary_key=True))   
'''
Association table between Movie and Actor resulted from the many to many relationship between them
'''
class Movie_Actor(db.Model):
  __tablename__ = 'movies_actors'
  movie_id = Column(Integer,ForeignKey('movies.id'), primary_key=True)
  actor_id=Column(Integer,ForeignKey('actors.id'), primary_key=True)

'''
Movie

'''
class Movie(db.Model):  
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  release_date=Column(Date)
  #many to many relationship
  actors = relationship('Actor', secondary='movies_actors', back_populates='movies')

  #answer = Column(String)
  #category = Column(String)
  #difficulty = Column(Integer)

  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date

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

  id = Column(Integer, primary_key=True)
  name = Column(String)
  age = Column(Integer)
  gender = Column(String)
  #many to many relationship
  movies = relationship('Movie', secondary='movies_actors', back_populates='actors')



  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender
    }

 