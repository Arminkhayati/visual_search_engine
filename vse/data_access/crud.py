from sqlalchemy.orm import Session
from . import entities, schemas
from typing import List, Union


def create_image(db: Session, image_path, labels):
    labels = [entities.Label(label=label) for label in labels]
    image = entities.Image(path=image_path, labels=labels)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image

def get_image_by_label(db: Session, label):
    return db.query(entities.Image).join(entities.Label)\
            .filter(entities.Label.label == label).all()
    # return entities.Image.query.join(entities.Label)\
    #     .filter(entities.Label.label == label).all()