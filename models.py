### models.py ###

from sqlalchemy import Column, Integer, String
from database import Base


'''
Model representing pokemon attributes

id (unique), name (unique), types, capture_rate, 
shape, color, description, and sprite url

Note: types is a list cast as a string, need to 
find a better way to represent this data
'''
class Pokemon_Model(Base):
    __tablename__ = 'pokedex'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    types = Column(String(50))
    capture_rate = Column(String(50))
    shape = Column(String(50))
    color = Column(String(15))
    description = Column(String(100))
    sprite_url = Column(String(100)) # storing only url for now, may consider full image binary

    def __init__(self, name=None, types=None, capture_rate=None, shape=None, color=None, description=None, sprite_url=None):
        self.name = name
        self.types = types
        self.capture_rate = capture_rate
        self.shape = shape
        self.color = color
        self.description = description
        self.sprite_url = sprite_url

    def __repr__(self):
        return '<Pokemon %r>' % (self.name)