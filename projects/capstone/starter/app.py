import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import Movie, Actor, movies_actors, setup_db, db,db_drop_and_create_all

# create and configure the app
app = Flask(__name__)
setup_db(app)
migrate = Migrate(app, db)
CORS(app)

app.secret_key = "secretKEY"
# db_drop_and_create_all()

'''Endpoints:
GET /actors and /movies
DELETE /actors/ and /movies/
POST /actors and /movies and
PATCH /actors/ and /movies/'''

@app.route("/actors", methods=["GET"])
def get_actors():
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
def get_movies():
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
def delete_actors(actor_id):
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
def delete_movies(movie_id):
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
def post_actors():
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
def post_movies():
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
def patch_actors(actor_id):
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
def patch_movies(movie_id):
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