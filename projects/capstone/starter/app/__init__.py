import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Movie, Actor, movies_actors, setup_db, db, db_drop_and_create_all
from auth import AuthError, requires_auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    app.secret_key = os.environ.get("SECRET")

    '''Endpoints:
    GET /actors and /movies
    DELETE /actors/ and /movies/
    POST /actors and /movies and
    PATCH /actors/ and /movies/'''

    @app.route("/actors", methods=["GET"])
    @requires_auth("view:actors")
    def get_actors(jwt):
        try:
            actors = Actor.query.all()
            formatted_actors = [
                actor.format() for actor in actors
            ]
            return jsonify({
                "success": True,
                "actors": formatted_actors
            })
        except:
            abort(404)

    @app.route("/movies", methods=["GET"])
    @requires_auth("view:movies")
    def get_movies(jwt):
        try:
            movies = Movie.query.all()
            formatted_movies = [
                movie.format() for movie in movies
            ]
            return jsonify({
                "success": True,
                "movies": formatted_movies
            })
        except:
            abort(404)

    @app.route("/actors/<actor_id>", methods=["DELETE"])
    @requires_auth("delete:actor")
    def delete_actors(jwt, actor_id):
        try:
            actor = Actor.query.get(actor_id)
            actor.delete()
            return jsonify({
                "success": True,
                "id_deleted": actor_id
            })
        except:
            abort(404)

    @app.route("/movies/<movie_id>", methods=["DELETE"])
    @requires_auth("delete:movie")
    def delete_movies(jwt, movie_id):
        try:
            movie = Movie.query.get(movie_id)
            movie.delete()
            return jsonify({
                "success": True,
                "id_deleted": movie_id
            })
        except:
            abort(404)


    @app.route("/actors", methods=["POST"])
    @requires_auth("add:actor")
    def post_actors(jwt):
        name = request.json.get("name")
        age = request.json.get("age")
        gender = request.json.get("gender")
        movies = request.json.get("movies")

        if not name or not age:
            abort(400)
        try:
            actor  = Actor(
                name=name,
                age=age,
                gender=gender
            )
            if movies is not None:
                movies = Movie.query.filter(Movie.title.in_(movies)).all()
                actor.movies = movies
            actor.insert()
            return jsonify({
                "success": True,
                "actor": actor.format()
            })
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()


    @app.route("/movies", methods=["POST"])
    @requires_auth("add:movie")
    def post_movies(jwt):
        title = request.json.get("title")
        release_date = request.json.get("release_date")
        actors = request.json.get("actors")

        if not title or not release_date:
            abort(400)
        try:
            movie = Movie(
                title=title,
                release_date=release_date
            )
            if actors is not None:
                actors = Actor.query.filter(Actor.name.in_(actors)).all()
                movie.actors = actors
            movie.insert()
            return jsonify({
                "success": True,
                "movie": movie.format()
            })
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.route("/actors/<actor_id>", methods=["PATCH"])
    @requires_auth("modify:actors")
    def patch_actors(jwt, actor_id):
        name = request.json.get("name")
        age = request.json.get("age")
        gender = request.json.get("gender")
        movies = request.json.get("movies")

        try:
            actor = Actor.query.get(actor_id)
        except:
            abort(404)

        if not name or not age:
            abort(400)

        try:
            actor.name = name
            actor.age = age
            actor.gender = gender
            if movies is not None:
                
                movies = Movie.query.filter(Movie.title.in_(movies)).all()
                
                actor.movies = movies
            actor.update()
            return jsonify({
                "success": True,
                "actor": actor.format()
            })
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()


    @app.route("/movies/<movie_id>", methods=["PATCH"])
    @requires_auth("modify:movies")
    def patch_movies(jwt, movie_id):
        title = request.json.get("title")
        release_date = request.json.get("release_date")
        actors = request.json.get("actors")

        try:
            movie = Movie.query.get(movie_id)
        except:
            abort(404)

        if not title or not release_date:
            abort(400)

        try:
            movie.title = title
            movie.release_date = release_date
            if actors is not None:
                actors = Actor.query.filter(Actor.name.in_(actors)).all()
                movie.actors = actors
            movie.update()
            return jsonify({
                "success": True,
                "movie": movie.format()
            })
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    if __name__ == '__main__':
        app.run(debug=True)

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False,
                        "error": 422,
                        "message": "unprocessable"
        }), 422
        
    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
                        "success": False,
                        "error": 404,
                        "message": "resource not found"
        }), 404

    @app.errorhandler(403)
    def unprocessable(error):
        return jsonify({
                        "success": False,
                        "error": 403,
                        "message": "unauthorized access"
        }), 403

    @app.errorhandler(401)
    def unprocessable(error):
        return jsonify({
                        "success": False,
                        "error": 401,
                        "message": "unauthorized access"
        }), 401

    @app.errorhandler(400)
    def unprocessable(error):
        return jsonify({
                        "success": False,
                        "error": 400,
                        "message": "bad request"
        }), 400

    @app.errorhandler(AuthError)
    def unprocessable(error):
        return jsonify({
                        "success": False,
                        "error": 401,
                        "message": "unauthorized access"
        }), 401

    return app

app = create_app()