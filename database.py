from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pokebase as pb
from flask import Flask
import requests
import os

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
    there seems to be a lot of complexity in this in terms of ball type,
    hp, etc. For now, I will use the ratio catch_rate/255.
    '''
    pokedex = pb.pokedex(2) # get pokedex data for kanto - '2'
    for entry in pokedex.pokemon_entries:
        pokemon = pb.pokemon(entry.entry_number) # get pokemon data based on pokedex entry api
        print(f"{entry.entry_number} {pokemon.name}")

        for desc in pokemon.species.flavor_text_entries: # iterate over descriptions and find english translation
            if desc.language.name == 'en':
                description = desc.flavor_text
                break

        type_list = []
        for types in pokemon.types:
            type_list.append(types.type.name)

        # TODO: check if file already exists
        img_data = requests.get(pokemon.sprites.front_default).content
        base_path = os.getcwd() + '/static/images/'
        filename = f'pokemon_{entry.entry_number}.jpg'
        # print(base_path + filename)
        with open(base_path + filename, 'wb') as handler:
            handler.write(img_data)

        db_session.add(Pokemon_Model( # create pokemon model, fill data, and commit to db
            name = pokemon.name,
            types = str(type_list),
            capture_rate = round((pokemon.species.capture_rate / 255) * 100),
            shape = pokemon.species.shape.name,
            color = pokemon.species.color.name,
            description = description,
            sprite_url = filename # get image url for sprite using 'front_default'
            ))
    db_session.commit()
