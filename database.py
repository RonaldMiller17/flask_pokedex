from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pokebase as pb
from flask import Flask
import requests

engine = create_engine('sqlite:///pokedex.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    
    from models import Pokemon_Model

    Base.metadata.create_all(bind=engine)

    '''
    Creates table data from api requests to pokebase wrapper
    TODO: find faster way to iterate, for loop is ugly
    TODO: need to figure out how to convert catch rate to percentage, depends on # of pokemon caught
    '''
    pokedex = pb.pokedex(2) # get pokedex data for kanto - '2'
    for entry in pokedex.pokemon_entries:
        pokemon = pb.pokemon(entry.entry_number) # get pokemon data based on pokedex entry api
        print(pokemon.name)

        for desc in pokemon.species.flavor_text_entries: # iterate over descriptions and find english translation
            if desc.language.name == 'en':
                description = desc.flavor_text
                break

        type_list = []
        for types in pokemon.types:
            type_list.append(types.type.name)

        # download sprite url - this didnt work too well
        # sprite = pb.SpriteResource('pokemon', entry.entry_number)
        # print(pokemon.sprites.front_default)

        img_data = requests.get(pokemon.sprites.front_default).content
        base_path = "/Users/aurora_secondary/python_projects/flask_pokedex/static/images/"
        filename = f'pokemon_{entry.entry_number}.jpg'
        # TODO: check if file already exists
        print(base_path + filename)
        with open(base_path + filename, 'wb') as handler:
            handler.write(img_data)

        db_session.add(Pokemon_Model( # create pokemon model, fill data, and commit to db
            name = pokemon.name,
            types = str(type_list),
            capture_rate = pokemon.species.capture_rate,
            shape = pokemon.species.shape.name,
            color = pokemon.species.color.name,
            description = description,
            sprite_url = filename # get image url for sprite using 'front_default'
            ))
    db_session.commit()
