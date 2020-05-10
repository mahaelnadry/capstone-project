# The Casting Agency Backend
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by using the following command

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./capstone-project` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```
## Development environment
export FLASK_ENV=development

To run the server, execute:
```bash
flask run 
```

## Application link
https://casting-agency-proj.herokuapp.com

## Models:
Movies with attributes title and release date
Actors with attributes name, age and gender

## Roles:
## Casting Assistant
Can view actors and movies
## Casting Director
All permissions a Casting Assistant has and…
Add or delete an actor from the database
Modify actors or movies
## Executive Producer
All permissions a Casting Director has and…
Add or delete a movie from the database

## Endpoints:

GET '/movies'
GET '/actors'
POST '/movies'
POST '/actors'
PATCH '/movies/{movie_id}'
PATCH '/actors/{actor_id}'
DELETE '/movies{movie_id}'
DELETE '/actors/{actor_id}'

## GET '/movies'
- Fetches movies that are currently saved in the database
- Request Arguments: Bearer JWT token should be passed in 'Authorization'
- Returns: An array of movies, each movie object has id, release_date and title 
{
  "movies": [
    {
      "id": 1,
      "release_date": "Mon, 03 May 2010 00:00:00 GMT",
      "title": "movie1"
    },
    {
      "id": 4,
      "release_date": "Sat, 04 Jan 2020 00:00:00 GMT",
      "title": "Movie New"
    },
    {
      "id": 5,
      "release_date": "Sat, 04 Jan 2020 00:00:00 GMT",
      "title": "Movie New"
    } 
  ],
  "success": true
}

## GET '/actors'
- Fetches actors that are currently saved in the database
- Request Arguments: Bearer JWT token should be passed in 'Authorization'
- Returns: An array of actors, each actor object has id, gender, age and name. 
{
  "actors": [
    {
      "age": 50,
      "gender": "Male",
      "id": 1,
      "name": "Amr diab"
    },
    {
      "age": 5,
      "gender": "Male",
      "id": 4,
      "name": "New actor"
    }
  ],
  "success": true
}

## POST '/movies'
- Creates a new movie using the passed title and release date
- Request Arguments: Bearer JWT token should be passed in 'Authorization'
- Request body:
{
	"title":"Jungle book",
	"release_date":"2020-01-04"
}
- Returns the id,release_date and title of the created movie and success value
{
  "movie": {
    "id": 24,
    "release_date": "Sat, 04 Jan 2020 00:00:00 GMT",
    "title": "Jungle book"
  },
  "success": true
}

## POST '/actors'
- Creates a new actor using the passed age, gender and name
- Request Arguments: Bearer JWT token should be passed in 'Authorization'
- Request body:
{
	"age":30,
	"gender": "Male",
    "name": "Peter George"
}
- Returns the id, age, name and gender of the created actor and success value
{
  "actor": {
    "age": 30,
    "gender": "Male",
    "id": 18,
    "name": "Peter George"
  },
  "success": true
}

## PATCH '/movies/{movie_id}'
- Patch an already created movie title or release_date or both of them if both of them are passed if this movie exits
- Request Arguments: movie_id (Integer), Bearer JWT token should be passed in 'Authorization'
- Request body:
{
	"title":"Jungle book Part2",
}
- Returns the id,release_date and title of the patched movie and success value
{
  "movie": {
    "id": 24,
    "release_date": "Sat, 04 Jan 2020 00:00:00 GMT",
    "title": "Jungle book Part2"
  },
  "success": true
}

## PATCH '/actors/{actor_id}'
- Patches an already created actor age or gender or name or all of them if all of them are passed in the request body if this actor exists
- Request Arguments: actor_id (Integer), Bearer JWT token should be passed in 'Authorization'
- Request body:
{
	"age":50,
}
- Returns the id, age, name and gender of the patched actor and success value
{
  "actor": {
    "age": 50,
    "gender": "Male",
    "id": 18,
    "name": "Peter George"
  },
  "success": true
}

## DELETE '/movies/{movie_id}'
- Deletes the movie with the given ID if this movie exits
- Request Arguments: movie_id (Integer), Bearer JWT token should be passed in 'Authorization'
- Returns the id of the deleted movie in key called "delete" and success value
{
  "delete": 15,
  "success": true
}

## DELETE '/actors/{actor_id}'
- Deletes the actor with the given ID if this actor exits
- Request Arguments: actor_id (Integer), Bearer JWT token should be passed in 'Authorization'
- Returns the id of the deleted actor in key called "delete" and success value
{
  "delete": 4,
  "success": true
}

## Testing
To run the tests, run
```
dropdb castingAgency
createdb castingAgency
python test_app.py
```
python test_app.py should be run while activating the virtual environment

but the database should be filled first with at least 4 movies and 3 actors in order that the patch and delete tests works fine,
there should be movies of Ids 2,3,4 and there should be actors of Ids 2 and 3
 you can use the postman collection 'casting_agency_postman_collection.postman_collection'   in the 'capstone_project' directory  to fill the database