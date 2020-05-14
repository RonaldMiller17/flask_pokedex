from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pokebase as pb
from flask import Flask

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
        for desc in pokemon.species.flavor_text_entries:
            if desc.language.name == 'en':
                description = desc.flavor_text
                # print(desc.flavor_text)
                break
        type_list = []
        for types in pokemon.types:
            type_list.append(types.type.name)
        db_session.add(Pokemon_Model( # create pokemon model, fill data, and commit to db
            name = pokemon.name,
            types = str(type_list),
            capture_rate = pokemon.species.capture_rate,
            shape = pokemon.species.shape.name,
            color = pokemon.species.color.name,
            description = description
            ))
    db_session.commit()
