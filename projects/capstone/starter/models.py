
import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "cast"
database_path = "postgres://{}/{}".format(':5433', database_name)

db = SQLAlchemy()

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

movies_actors = db.Table("movies_actors",
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.id"), primary_key=True),
    db.Column("actor_id", db.Integer, db.ForeignKey("actors.id"), primary_key=True)
)

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all() 

class Movie(db.Model):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(String)
    actors = db.relationship(
        "Actor",
        secondary=movies_actors,
        lazy="subquery",
        backref=db.backref("movies", lazy=True)
    )

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
        actors = db.session.query(movies_actors).join(Movie).join(Actor).filter(Movie.id == self.id).with_entities(Actor.name).all()
        actors_return = []
        for actor in actors:
            actors_return.append(*actor)
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "actors": actors_return
        }

class Actor(db.Model):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        movies = db.session.query(movies_actors).join(Movie).join(Actor).filter(Actor.id == self.id).with_entities(Movie.title).all()
        movies_return = []
        for movie in movies:
            movies_return.append(*movie)
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "movies": movies_return
        }


