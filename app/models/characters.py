# SQLAlchemy
from sqlalchemy import Column, String, Integer

# import
from app.core.database import Base

"""
"id": 1,
"name": "Jon Snow",
"house": "Stark",
"animal": "Direwolf",
"symbol": "Wolf",
"nickname": "King in the North",
"role": "King",
"age": 25,
"death": null,
"strength": "Physically strong"""

class Character(Base):
    __tablename__ = "characters"

    character_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=True)
    house = Column(String, nullable=True)
    animal = Column(String, nullable=True)
    symbol = Column(String, nullable=True)
    nickname = Column(String, nullable=True)
    role = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    death = Column(String, nullable=True)
    strength = Column(String, nullable=True)

    def __repr__(self):
        return f"character_id=(self.character_id), name=(self.name)"
