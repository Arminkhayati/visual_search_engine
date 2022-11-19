from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import uuid
from .database import Base


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, unique=True, index=True)
    labels = relationship("Label", back_populates="owner")

class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("images.id"))

    owner = relationship("Image", back_populates="labels")