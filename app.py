import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import db_drop_and_create_all, setup_db, Movie, Actor, Movie_Actor

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  db_drop_and_create_all()
  '''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
  return app

APP = create_app()

if __name__ == '__main__':
    APP.run() ##default port
   ## APP.run(host='0.0.0.0', port=8080, debug=True)