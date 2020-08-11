import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

ASSISTANT=os.environ.get('ASSISTANT')
DIRECTOR=os.environ.get('DIRECTOR')
PRODUCER=os.environ.get('PRODUCER')

os.system("dropdb {}".format("cast_test"))
os.system("createdb {}".format("cast_test"))

class CastTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "cast_test"
        self.database_path = "postgresql://{}/{}".format(":5433", self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_actor = {
            "name": "New Actor",
            "age": 59,
            "gender": "Male",
            "movies": []
        }

        self.another_actor = {
            "name": "Another Actor",
            "age": 20,
            "gender": "Female",
            "movies": []
        }

        self.new_movie = {
            "title": "New Movie",
            "release_date": "2020-5-15",
            "actors": []
        }

        self.another_movie = {
            "title": "Another Movie",
            "release_date": "2035-5-15",
            "actors": []
        }

        self.empty_actor = {
            "name": "",
            "age": 59,
            "gender": "Male",
            "movies": []
        }

        self.empty_movie = {
            "title": "",
            "release_date": "2020-5-15",
            "actors": []
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    '''
    TESTS for Actor
    '''
    # Test post actor
    def test_post_actor(self):
        res = self.client().post(
            "/actors",
            json=self.new_actor,
            headers={
                "Authorization": "Bearer {}".format(DIRECTOR)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        return data.get("actor")

    # Test get actors
    def test_get_actors(self):
        res = self.client().get(
            "/actors",
            headers={
                "Authorization": "Bearer {}".format(ASSISTANT)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # Test patch actor
    def test_patch_actors(self):
        actor = self.test_post_actor()

        res = self.client().patch(
            "/actors/{}".format(actor["id"]),
            json=self.another_actor,
            headers={
                "Authorization": "Bearer {}".format(DIRECTOR)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        updated_actor = data.get("actor")
        updated_actor.pop("id")
        self.assertEqual(updated_actor, self.another_actor)
    
    # Test delete actor
    def test_delete_actor(self):
        actor = self.test_post_actor()

        res = self.client().delete(
            "/actors/{}".format(actor["id"]),
            headers={
                "Authorization": "Bearer {}".format(DIRECTOR)
            }
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(int(data.get("id_deleted")), actor["id"])
    
    '''
    TESTS for Movie
    '''
    # Test post movie
    def test_post_movie(self):
        res = self.client().post(
            "/movies",
            json=self.new_movie,
            headers={
                "Authorization": "Bearer {}".format(PRODUCER)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        return data.get("movie")

    # Test get movies
    def test_get_movies(self):
        res = self.client().get(
            "/movies",
            headers={
                "Authorization": "Bearer {}".format(PRODUCER)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)


    # Test patch movie
    def test_patch_movie(self):
        movie = self.test_post_movie()

        res = self.client().patch(
            "/movies/{}".format(movie["id"]),
            json=self.another_movie,
            headers={
                "Authorization": "Bearer {}".format(PRODUCER)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    
    # Test delete movie
    def test_delete_movie(self):
        movie = self.test_post_movie()

        res = self.client().delete(
            "/movies/{}".format(movie["id"]),
            headers={
                "Authorization": "Bearer {}".format(PRODUCER)
            }
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(int(data.get("id_deleted")), movie["id"])

    '''
    TESTS error for actors
    '''
    # Test error for post actor
    def test_400_post_actor(self):
        res = self.client().post(
            "/actors",
            json=self.empty_actor,
            headers={
                "Authorization": "Bearer {}".format(DIRECTOR)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)

    # Test error for get actor
    def test_401_public_get_actor(self):
        res = self.client().get("/actors")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    # Test error for patch actor
    def test_400_patch_actor(self):
        actor = self.test_post_actor()
        res = self.client().patch(
            "/actors/{}".format(actor["id"]),
            json=self.empty_actor,
            headers={
                "Authorization": "Bearer {}".format(DIRECTOR)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)

    # Test error for delete actor
    def test_404_delete_actor(self):
        res = self.client().delete(
            "/actors/1000",
            headers={
                "Authorization": "Bearer {}".format(DIRECTOR)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    '''
    TESTS error for movies
    '''
    # Test error for post movie
    def test_400_post_movie(self):
        res = self.client().post(
            "/movies",
            json=self.empty_movie,
            headers={
                "Authorization": "Bearer {}".format(PRODUCER)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)

    # Test error for get movies
    def test_401_public_get_movie(self):
        res = self.client().get("/movies")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    # Test error for patch movie
    def test_400_patch_movie(self):
        movie = self.test_post_movie()
        res = self.client().patch(
            "/movies/{}".format(movie["id"]),
            json=self.empty_movie,
            headers={
                "Authorization": "Bearer {}".format(DIRECTOR)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
    
    # Test error for delete movie
    def test_404_delete_movie(self):
        res = self.client().delete(
            "/movies/1000",
            headers={
                "Authorization": "Bearer {}".format(PRODUCER)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    '''
    TESTS of RBAC for each role
    '''
    # Test authorized for ASSISTANT - can get actors
    def test_authorized_assistant(self):
        res = self.client().get(
            "/actors",
            headers={
                "Authorization": "Bearer {}".format(ASSISTANT)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # Test unauthorized for ASSISTANT - can't post an actor
    def test_unauthorized_assistant(self):
        res = self.client().post(
            "/actors",
            json=self.new_actor,
            headers={
                "Authorization": "Bearer {}".format(ASSISTANT)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    # Test authorized for DIRECTOR - can post an actor
    def test_authorized_director(self):
        res = self.client().post(
            "/actors",
            json=self.new_actor,
            headers={
                "Authorization": "Bearer {}".format(DIRECTOR)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # Test unauthorized for DIRECTOR - can't post a movie
    def test_unauthorized_director(self):
        res = self.client().post(
            "/movies",
            json=self.new_movie,
            headers={
                "Authorization": "Bearer {}".format(DIRECTOR)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    # Test authorized for PRODUCER - can post a movie
    def test_authorized_producer_post_movie(self):
        res = self.client().post(
            "/movies",
            json=self.new_movie,
            headers={
                "Authorization": "Bearer {}".format(PRODUCER)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # Test authorized for PRODUCER - can delete a movie
    def test_authorized_producer_delete_movie(self):
        movie = self.test_post_movie()

        res = self.client().delete(
            "/movies/{}".format(movie["id"]),
            headers={
                "Authorization": "Bearer {}".format(PRODUCER)
            }
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()