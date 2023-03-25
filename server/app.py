#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False #this line will indent and separate lines of json to make it easier on your eyes. you don't need to do this if you're using the json beautify extension on google chrome

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

@app.route('/games')
def games():
    games = []
    for g in Game.query.all():
        #title, genre, platform, price
        dict = g.to_dict()
        games.append(dict)

    res = make_response(games, 200, {"Content-Type": "application/json"}) #jsonify serializes (converts from one format to another format aka SQLAlchemy obj to JSON obj) arguments as JSON and returns a flask response object. It takes objects as arguments (lists and dictionaries). It does not take Models! Sometimes you can get away with out jsonifying. However in most cases we will have to jsonify! otherwise you'll hit a TypeError. 
    #__dict__ in Python will represent a dictionary. 
    return res

@app.route('/games/<int:id>') #here we create a dynamic portion of the URL. Then we can access that dynamic portion of the URL by using the dynamic parameter name. Ensure that you ONLY USE UNIQUE ATTRIBUTES IN DYNAMIC URLs
def game(id):
    g = Game.query.filter(Game.id == id).first() #note this returns a model so we have to create a dict of the model
    dict = g.to_dict()
    res = make_response(dict, 200, {"Content-Type" : "application/json"})
    return res

@app.route('/reviews')
def reviews():
    # "score", "comment", "user", "game"
    reviews = []
    for r in Review.query.all():
        dict = r.to_dict()
        reviews.append(dict)

    res = make_response(reviews, 200, {"Content-Type": "application/json"}) #without jsonify, you'll get TypeError: Object of type Game is not JSON serializable. That being said, jsonify() is now run automatically on all dictionaries returned by Flask views!!!
    return res
    


#### DO NOT COMMENT THE BELOW OUT
if __name__ == '__main__':
    app.run(port=5555, debug=True) #look up how to do this from the command line