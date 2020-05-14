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


'''
Initialize Database and make api request for all pokemon in Kanto region
write these pokemon and their traits to table
'''

# initialize db
# db = init_db()
# exit(1)

pokemon_list = []

# retrive pokedex based on id '2' for Kanto
# pokedex = pb.pokedex(2)
# print(pokedex.pokemon_entries)

def get_pokemon(entry):
    return {
        "id": entry.entry_number,
        "name": entry.pokemon_species.name
    }

# pokemon_list = list(map(get_pokemon, pokedex.pokemon_entries))
# pokemon_list = [x.get_pokemon() for x in pokedex.pokemon_entries]


app = Flask(__name__)


# @app.cli.command('initdb')
# def initdb_command():
#     init_db()
#     print('Initialized the database.')

# teardown database session
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# currently using this for api/sqlalchemy orm testing
@app.route("/")
def home():

    # TODO: use levenschtien for fuzzy search??

    pokemon_list = []
    objects = []

    # reguest Kanto pokedex
    response = requests.get("https://pokeapi.co/api/v2/pokedex/2/")
    kanto_pokemon = response.json()['pokemon_entries']
    for pokemon in kanto_pokemon:
        # print(pokemon['pokemon_species']['name'])
        pokemon_list.append(pokemon['pokemon_species']['name'])

    # print(len(objects))
    # try:
    #     db_session.bulk_save_objects(objects)
    #     print("saved")
    # except Exception as e:
    #     print(f"could not save {e}")
    # db_session.commit()

    print(f"Length - {len(pokemon_list)}")
    # print(pokemon_list)


    # write json to file
    # with open('kanto_pokemon.txt', 'w') as outfile:
    #     json.dump(response.json()['pokemon_entries'], outfile)

    # TODO: pass results (df) to template that will pull from Results class

    # welcome message
    return render_template('base.html', len = len(pokemon_list), Pokemon = pokemon_list)


# testing another page
@app.route("/index")
def index():

    results = []
    pokemon_list = [{"id": 1, "name": "pikachu", "type": "electric", "shape": "quadruped", "capture rate": "45%"},
                {"id": 2, "name": "Charizard", "type": "flying"},
                {"id": 3, "name": "Squirtle"},
                {"id": 4, "name": "Jigglypuff"}]

    def map_pokemon(pokemon):
        print(f"{pokemon.name} {pokemon.shape}")


    # print(Pokemon_Model.query.all())
    # print(db_session.query(Pokemon_Model.capture_rate).all())
    for pokemon in Pokemon_Model.query.all():
        # print(f"{pokemon.name} {pokemon.capture_rate}")
        # print(pokemon.shape)

        results.append(
            {
                "id": pokemon.id,
                "Name": pokemon.name,
                "Catch Rate": pokemon.capture_rate,
                "Type(s)": pokemon.types,
                "Shape": pokemon.shape,
                "Color": pokemon.color,
                "Description": pokemon.description
            }
        )
    # print(db_session.query.all())
    # for pokemon in Pokemon_Model.query.all():
    #     map_pokemon(pokemon)

    fieldnames = [key for key in results[0].keys()]
    print(fieldnames)
    return render_template('datatable.html', results=results, fieldnames=fieldnames, len=len)

if __name__ == "__main__":
    app.run(debug=True) 



# [df.to_html(classes='data')]
# return render_template('base.html', len = len(pokemon), Pokemon = pokemon)

# table = Results(pokemon_list)
# table.border = True
# return render_template("results.html", table=table)
    
