# imports
from flask import Flask, render_template, request
import os
import requests
import json
import pandas as pd
from database import db_session
from database import init_db
from models import Pokemon_Model
import pokebase as pb
import csv


'''
Initialize Database and make api request for all pokemon in Kanto region
write these pokemon and their traits to table

TODO: implement alembic migrations
'''

# initialize db
# db = init_db()
# exit(1)

app = Flask(__name__, static_folder='static')

# @app.cli.command('initdb')
# def initdb_command():
#     init_db()
#     print('Initialized the database.')


# teardown database session
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# testing another page
@app.route("/", methods=["GET","POST"])
def home():
    if request.method == 'GET':

        results = [] # list to store dictionaries of poke-data from sqlalchemy
        images = [] # list to store image urls

        # print(db_session.query(Pokemon_Model.capture_rate).all())

        # iterate over pokemon model instances in database
        for pokemon in Pokemon_Model.query.all():

            images.append(pokemon.sprite_url) # append images url to image list
            # print(pokemon.sprite_url)

            # append dict with headers and data to list
            results.append(
                {
                    "id": pokemon.id,
                    "Name": pokemon.name,
                    "Catch Rate": f"{pokemon.capture_rate}%",
                    "Type(s)": pokemon.types,
                    "Shape": pokemon.shape,
                    "Color": pokemon.color,
                    "Description": pokemon.description
                }
            )

        fieldnames = [key for key in results[0].keys()] # list comprehesion for field keys from dict
        # print(fieldnames)

        # render template with data, headers, and images
        return render_template('base.html', results=results, fieldnames=fieldnames, images=images, len=len)
    elif request.method == 'POST':
        return render_template(results=None, fieldnames=None, images=None, len=len)

if __name__ == "__main__":
    app.run(debug=True) 

    
