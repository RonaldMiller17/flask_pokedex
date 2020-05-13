# imports
from flask import Flask
import os
import requests
import json


app = Flask(__name__)

@app.route("/")
def home():

    # TODO: use levenschtien for fuzzy search??

    # reguest Kanto pokedex
    response = requests.get("https://pokeapi.co/api/v2/pokedex/2/")
    kanto_pokemon = response.json()['pokemon_entries']
    for pokemon in kanto_pokemon:
        print(pokemon)


    # write json to file
    # with open('kanto_pokemon.txt', 'w') as outfile:
    #     json.dump(response.json()['pokemon_entries'], outfile)

    # welcome message
    return "Welcome to the Pokédex!"


# testing another page
@app.route("/index")
def index():
    return "This is a different page"

if __name__ == "__main__":
    app.run(debug=True) 