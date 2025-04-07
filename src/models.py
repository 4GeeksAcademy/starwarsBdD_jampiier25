from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

db = SQLAlchemy()

class FavoriteType(enum.Enum):
    character = "character"
    planet = "planet"
    vehicle = "vehicle"

#(String(120)) para restringirlo a 120 caracteres 
#(String(50)) lo mismo pero para 50 caracteres
#(String(255) the same pero para 255 caracteres
#nullable=False con esto evitamos que queden vacios

class User(db.Model):

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(120))
    last_name: Mapped[str] = mapped_column(String(120))
    subscription_date: Mapped[str] = mapped_column(String(120))

    #relations
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")


#robert nos comento que no debemos devolver el password aqui porque se leak la contraseña 
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }
    
class Character(db.Model):

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[str] = mapped_column(String(50))
    birth_year: Mapped[str] = mapped_column(String(50))
    eye_color: Mapped[str] = mapped_column(String(50))

    #relations
    favorites = relationship("Favorite", back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
        }


class Planet(db.Model):

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(50))
    terrain: Mapped[str] = mapped_column(String(50))
    population: Mapped[str] = mapped_column(String(50))

    #relations
    favorites = relationship("Favorite", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class Vehicle(db.Model):

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    model: Mapped[str] = mapped_column(String(120))
    manufacturer: Mapped[str] = mapped_column(String(120))
    passengers: Mapped[str] = mapped_column(String(50))

    #relations
    favorites = relationship("Favorite", back_populates="vehicle")
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
        }

class Favorite(db.Model):

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    favorite_type: Mapped[FavoriteType] = mapped_column(Enum(FavoriteType), nullable=False)

    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicle.id"), nullable=True)

    user = relationship("User", back_populates="favorites")
    character = relationship("Character", back_populates="favorites")
    planet = relationship("Planet", back_populates="favorites")
    vehicle = relationship("Vehicle", back_populates="favorites")