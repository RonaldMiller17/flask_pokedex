# imports
from flask import Flask, render_template
from flask_table import Table, Col
import os
import requests
import json
import pandas as pd


app = Flask(__name__)

@app.route("/")
def home():

    # TODO: use levenschtien for fuzzy search??

    pokemon_list = []

    # reguest Kanto pokedex
    response = requests.get("https://pokeapi.co/api/v2/pokedex/2/")
    kanto_pokemon = response.json()['pokemon_entries']
    for pokemon in kanto_pokemon:
        # print(pokemon['pokemon_species']['name'])
        pokemon_list.append(pokemon['pokemon_species']['name'])

    print(f"Length - {len(pokemon_list)}")
    print(pokemon_list)


    # write json to file
    # with open('kanto_pokemon.txt', 'w') as outfile:
    #     json.dump(response.json()['pokemon_entries'], outfile)

    # TODO: pass results (df) to template that will pull from Results class

    # welcome message
    return render_template('base.html', len = len(pokemon_list), Pokemon = pokemon_list)


# testing another page
@app.route("/index")
def index():
    # making list of pokemons 
    pokemon =["Pikachu", "Charizard", "Squirtle", "Jigglypuff",  
           "Bulbasaur", "Gengar", "Charmander", "Mew", "Lugia", "Gyarados"] 

    return render_template('base.html', len = len(pokemon), Pokemon = pokemon)


if __name__ == "__main__":
    app.run(debug=True) 