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
    
    # import
    from models import Pokemon_Model

    Base.metadata.create_all(bind=engine)

    # get pokemon data
    pokedex = pb.pokedex(2)
    for entry in pokedex.pokemon_entries:
        pokemon = pb.pokemon(entry.entry_number)
        # print(entry)
        print(f"{pokemon.name} {pokemon.species.shape.name}")
        db_session.add(Pokemon_Model(
            name = pokemon.name,
            types = str(pokemon.types),
            capture_rate = pokemon.species.capture_rate,
            shape = pokemon.species.shape.name
            ))
    db_session.commit()
