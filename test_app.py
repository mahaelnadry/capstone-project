
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import  setup_db, Movie, Actor, Movie_Actor, SQLALCHEMY_DATABASE_URI


castingAssistantToken = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFueFlGTERkN0wwMkFBRWpXeDNPVyJ9.eyJpc3MiOiJodHRwczovL2Rldi11bzF4dTM4eS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTgyNzU4OTQ0ODI2NDE3MjM0NjIiLCJhdWQiOlsiY2FzdGluZ19hZ2VuY3kiLCJodHRwczovL2Rldi11bzF4dTM4eS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTg5MDU4MTEzLCJleHAiOjE1ODkxNDQ1MTMsImF6cCI6Ijh2UVc3OWtVNXZFM0JKcHJvM2JYZlE0eWQ0Vng1NW9iIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.N68AyitjCQ7tgCj4Dr5GCxu3zp6p0IHQKrph3g2_htOgXcSeKphmL7dd1L0xNHhVuBxjk9Fc0nOzJujukuWE18lZY_uAZWUklN-ie5HSj8EF3Oum6Lpmz5gHrltTKQkVn5zUToZ64Q362-qu4C4bo6Obt86ui55dKXRWxJN7AFLRM6VNIrUd9Fqwfs8extpwE9igT0JWeN5hYEM0Prn9QetdTGIjpK7-of1CFbANBBJozVmfnPRLEFCjZI5nr_XPF3KWZr0cOUpehlei11N1o2cT9gxuN9DreFagZhs6jHgk1e-BWXlnYB6pJS_Z4neZyS0UligWiUgRlIPDCOl4kQ"
castingDirectorToken = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFueFlGTERkN0wwMkFBRWpXeDNPVyJ9.eyJpc3MiOiJodHRwczovL2Rldi11bzF4dTM4eS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTgyNzU4OTQ0ODI2NDE3MjM0NjIiLCJhdWQiOlsiY2FzdGluZ19hZ2VuY3kiLCJodHRwczovL2Rldi11bzF4dTM4eS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTg5MDU3OTk0LCJleHAiOjE1ODkxNDQzOTQsImF6cCI6Ijh2UVc3OWtVNXZFM0JKcHJvM2JYZlE0eWQ0Vng1NW9iIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.ElHt4Ugz35bWZgTPbMh21d1wtkFuUw0ln_Zj1Id_afNrXOaDYfJF_tkTdZCmbvdOMuPXdAio3VXWXIRqG31qt-5lpdWivlhvy8wmGMWd0dLTGfKZXD9VCGPKtUV57hc1uV9Ob2GZoe5RMlMeU0AcPKXFNA4On--Cb22iVqhMiIhcVUYVGlwJI6cQLOT14PSeAs5kJDTqEqo1QhOE1Th7BV7rId0DsNdwHMXj_PV7GFpdY5VusO7gYg_6zz6aDbtJTqmWaS_M28Jl2J9_DewRHzeiDxuwhXWCt8mtDlF1cC9kcaoaElGQBN7OEZf2vo31oBJZ4lpysy9ybA478ht-fw"
ExecutiveProducerToken = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFueFlGTERkN0wwMkFBRWpXeDNPVyJ9.eyJpc3MiOiJodHRwczovL2Rldi11bzF4dTM4eS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTgyNzU4OTQ0ODI2NDE3MjM0NjIiLCJhdWQiOlsiY2FzdGluZ19hZ2VuY3kiLCJodHRwczovL2Rldi11bzF4dTM4eS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTg5MDU4MjEyLCJleHAiOjE1ODkxNDQ2MTIsImF6cCI6Ijh2UVc3OWtVNXZFM0JKcHJvM2JYZlE0eWQ0Vng1NW9iIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.BD2HH5PVjZEaKd00cXKmwWMDdeNra0AaAd4bQEH68Cx1kJ-mEin4SQXRcJ-vheqdMcIB2iAXh2ykn91rfMgLB8exFuG1NInSvWODiyoKABEkEQ3nGJ-KfJtTgj61TXh8J-EhSxhkKzhcjEUZsUG4JHqrtNiQkl16uEqs-d-XgwX_4PkMlc-MxCpgCSL3Zf7gBfhAIQFg8laGhObVgRljTyr8fd2g-tg7oPFQIVf65_joxgdUz0bUg8eZKswG-IOgST8TKAkIVbEICaFMsU9ZdZPig3cqGxLD8EHRpjnzejcnqkfXK02eTSPGS9bk-H_wm59LuksErJKn8FubGGNSpA"

castingAssistantToken = "Bearer "+castingAssistantToken
castingDirectorToken = "Bearer "+castingDirectorToken
ExecutiveProducerToken = "Bearer "+ExecutiveProducerToken

class CastingAgencyTestCase(unittest.TestCase):
    
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    def test_get_movies(self):
        auth_header = {
        'Authorization': ExecutiveProducerToken
        }
        res=self.client().get('/movies', headers=auth_header)
        self.assertEqual(res.status_code,200)    
    def test_get_actors(self):
        auth_header = {
        'Authorization': ExecutiveProducerToken
        }
        res=self.client().get('/actors', headers=auth_header)
        self.assertEqual(res.status_code,200)    
    
    def test_add_movies_valid(self):
        auth_header = {
        'Authorization': ExecutiveProducerToken
        }
        res=self.client().post('/movies',json={
            "title":"Movie New",
	        "release_date":"2020-01-04"
        }, headers=auth_header)
        self.assertEqual(res.status_code,200)
       
        ##this test is invalid as the items passed in the json are wrong  
    def test_add_movies_invalid(self):
        auth_header = {
        'Authorization': ExecutiveProducerToken
        }
        res=self.client().post('/movies',json={
            "titlekkkkkk":"Movie Newfffffff",
	        "release_date":"2020-01-04"
        }, headers=auth_header)
        self.assertEqual(res.status_code,422)  
    
    def test_update_movies_valid(self):
        auth_header = {
        'Authorization': ExecutiveProducerToken
        }
        res=self.client().patch('/movies/2',json={
            "title":"The big mobie",
	        "release_date":"2020-06-04"
        }, headers=auth_header)
        self.assertEqual(res.status_code,200)
     
    ##this test is invalid as movie id 100 is not in the database
    def test_update_movies_invalid(self):
        auth_header = {
        'Authorization': ExecutiveProducerToken
        }
        res=self.client().patch('/movies/100',json={
            "title":"The big mobie",
	        "release_date":"2020-06-04"
        }, headers=auth_header)
        self.assertEqual(res.status_code,404)
    ##this test is valid if there is a movie id=3 in the database
    def test_delete_movies_valid(self):
        auth_header = {
        'Authorization': ExecutiveProducerToken
        }
        res=self.client().delete('/movies/3', headers=auth_header)
        self.assertEqual(res.status_code,200)  

    ##this test is invalid as movie id 100 is not in the database
    def test_delete_movies_invalid(self):
        auth_header = {
        'Authorization': ExecutiveProducerToken
        }
        res=self.client().delete('/movies/100', headers=auth_header)
        self.assertEqual(res.status_code,404)   
    
    def test_add_actors_valid(self):
        auth_header = {
        'Authorization': ExecutiveProducerToken
        }
        res=self.client().post('/actors',json={
           	"age":5,
	        "gender": "Male",
            "name": "New actor"
        }, headers=auth_header)
        self.assertEqual(res.status_code,200)

    ##this test is invalid as the items passed in the json are wrong  
    def test_add_actors_invalid(self):
        auth_header = {
        'Authorization': ExecutiveProducerToken
        }
        res=self.client().post('/actors',json={
           	"age":5,
	        "gender": "Male",
            "nameeeeeee": "New actor"
        }, headers=auth_header)
        self.assertEqual(res.status_code,422)

    def test_update_actors_valid(self):
        auth_header = {
        'Authorization': ExecutiveProducerToken
        }
        res=self.client().patch('/actors/2',json={
           	"age":20,
        }, headers=auth_header)
        self.assertEqual(res.status_code,200)

    ##this test is invalid as actor id 100 is not in the database
    def test_update_actors_invalid(self):
        auth_header = {
        'Authorization': ExecutiveProducerToken
        }
        res=self.client().patch('/actors/100',json={
           	"age":20,
        }, headers=auth_header)
        self.assertEqual(res.status_code,404)

    ##this test is valid if there is a actor id=3 in the database
    def test_delete_actors_valid(self):
        auth_header = {
        'Authorization': ExecutiveProducerToken
        }
        res=self.client().delete('/actors/3', headers=auth_header)
        self.assertEqual(res.status_code,200)

    ##this test is invalid as actor id 100 is not in the database
    def test_delete_actors_invalid(self):
        auth_header = {
        'Authorization': ExecutiveProducerToken
        }
        res=self.client().delete('/actors/100', headers=auth_header)
        self.assertEqual(res.status_code,404)


    ##Casting Assistant role testing
    def test_get_movies_castingAssistant(self):
        auth_header = {
        'Authorization': castingAssistantToken
        }
        res=self.client().get('/movies', headers=auth_header)
        self.assertEqual(res.status_code,200)      

    def test_update_actors_castingAssistant(self):
        auth_header = {
        'Authorization': castingAssistantToken
        }
        res=self.client().patch('/actors/2',json={
           	"age":20,
        }, headers=auth_header)
        self.assertEqual(res.status_code,401)

    ##Casting Director role testing
  
    def test_update_actors_castingDirector(self):
        auth_header = {
        'Authorization': castingDirectorToken
        }
        res=self.client().patch('/actors/2',json={
           	"age":50,
        }, headers=auth_header)
        self.assertEqual(res.status_code,200) 

    def test_add_movies_castingDirector(self):
        auth_header = {
        'Authorization': castingDirectorToken
        }
        res=self.client().post('/movies',json={
            "title":"Movie New",
	        "release_date":"2020-01-04"
        }, headers=auth_header)
        self.assertEqual(res.status_code,401)       

    ##Executive Producer role testing
    
    ##this test is valid if there is a movie id=3 in the database
    def test_delete_movies_ExecutiveProducer(self):
        auth_header = {
        'Authorization': ExecutiveProducerToken
        }
        res=self.client().delete('/movies/4', headers=auth_header)
        self.assertEqual(res.status_code,200)  

    def test_add_movies_ExecutiveProducer(self):
        auth_header = {
        'Authorization': ExecutiveProducerToken
        }
        res=self.client().post('/movies',json={
            "title":"Movie New",
	        "release_date":"2020-01-04"
        }, headers=auth_header)
        self.assertEqual(res.status_code,200)
     
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()        