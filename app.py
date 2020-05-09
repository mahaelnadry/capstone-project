import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db_drop_and_create_all, setup_db, Movie, Actor, Movie_Actor
from auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  ##uncomment the following line to initialize the datbase
  ## THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
  #db_drop_and_create_all()
  cors=CORS(app,resources={r"/api/*":{"origins":"*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods','GET,PATCH,POST,DELETE,OPTIONS')
    return response
   
  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(self):
    movies = Movie.query.all()
    if len(movies) == 0:
      abort(404)
    try:  
        formatted_movies = []
        for movie in movies:
            formatted_movies.append(movie.format())
        return jsonify({
            'success': True,
            'movies': formatted_movies
            })
    except Exception as e:
        print("Exception is ", e)
        abort(400)
  
  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(self):
    actors = Actor.query.all()
    print(actors)
    if len(actors) == 0:
      abort(404)
    try:
        formatted_actors = []
        for actor in actors:
            formatted_actors.append(actor.format())
        return jsonify({
            'success': True,
            'actors': formatted_actors
            })
    except Exception as e:
        print("Exception is ", e)
        abort(400)

  @app.route('/actors' , methods=['POST'])
  @requires_auth('post:actors')
  def add_actor(self):
  #def add_actor():  
    try:
      data = request.get_json()
      actor=Actor(name=data['name'],age=data['age'],gender=data['gender'])
      actor.insert()
      return jsonify({
        'success':True,
        'actor':actor.format()
      })
    except Exception as e:
      print("exception is ",e)
      abort(422)

  @app.route('/movies' , methods=['POST'])
  @requires_auth('post:movies')
  def add_movie(self):  
    try:
      data = request.get_json()
      movie=Movie(title=data['title'],release_date=data['release_date'])
      movie.insert()
      return jsonify({
        'success':True,
        'movie':movie.format()
      })
    except Exception as e:
      print("exception is ",e)
      abort(422)


  @app.route('/actors/<int:actor_id>' , methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(self,actor_id):  
    data = request.get_json()
    actor=Actor.query.filter(Actor.id == actor_id).one_or_none()
    #actor=Actor(name=data['name'],age=data['age'],gender=data['gender'])
    if actor is None:
      abort(404) ##the abort outside try works right
    try:
      for key in data.keys():
        if key=='name':
          actor.name = data[key]
        elif key =='age':
          actor.age = data[key]
        elif key =='gender':
          actor.gender = data[key]        
      actor.update()
      return jsonify({
        'success':True,
        'actor':actor.format()
      })
    except Exception as e:
      print("exception is ",e)
      abort(404)
  
  @app.route('/movies/<int:movie_id>' , methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(self,movie_id):  
    data = request.get_json()
    movie=Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
      abort(404) ##the abort outside try works right
    try:
      for key in data.keys():
        if key=='title':
          movie.title = data[key]
        elif key =='release_date':
          movie.release_date = data[key]       
      movie.update()
      return jsonify({
        'success':True,
        'movie':movie.format()
      })
    except Exception as e:
      print("exception is ",e)
      abort(404)

  @app.route('/actors/<int:actor_id>' , methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(self,actor_id):
      actor=Actor.query.get(actor_id)
      if actor is None:
        abort(404) ##the abort outside try works right
      try:  
          actor.delete()
          return jsonify({
          'success':True,
          'delete':actor_id
          })
      except Exception as e:
          #print("exception",e)
          abort(404)

  @app.route('/movies/<int:movie_id>' , methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(self,movie_id):
      movie=Movie.query.get(movie_id)
      if movie is None:
        abort(404)  ##the abort outside try works right
      try:  
          movie.delete()
          return jsonify({
          'success':True,
          'delete':movie_id
          })
      except Exception as e:
          #print("exception",e)
          abort(404)        
  ## Error Handling

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
        'success': False, 
        'error': 422,
        'message': "unprocessable"
        }), 422

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
        'success':False,
        'error':404,
        'message':"ٌResource Not found"
      }), 404

  @app.errorhandler(400)
  def bad_request(error):
        return jsonify({
          'success':False,
          'error':400,
          'message':"Bad Request"
      }), 400 

  @app.errorhandler(AuthError)
  def auth_error(Error):
        return jsonify({
          'success':False,
          'error':Error.status_code,
          'message':Error.error['code'],
          'description':Error.error['description']
      }),401  ##401 is the status code returned
 
  
  return app

APP = create_app()

if __name__ == '__main__':
    ##APP.run() ##default port
   APP.run(host='0.0.0.0', port=8080, debug=True)