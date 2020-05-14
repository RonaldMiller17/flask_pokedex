### models.py ###

from sqlalchemy import Column, Integer, String
from database import Base


# pokemon model
class Pokemon_Model(Base):
    __tablename__ = 'pokedex'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    types = Column(String(50))
    capture_rate = Column(String(50))
    shape = Column(String(50))
    color = Column(String(15))
    description = Column(String(100))

    def __init__(self, name=None, types=None, capture_rate=None, shape=None, color=None, description=None):
        self.name = name
        self.types = types
        self.capture_rate = capture_rate
        self.shape = shape
        self.color = color
        self.description = description



    def __repr__(self):
        return '<Pokemon %r>' % (self.name)