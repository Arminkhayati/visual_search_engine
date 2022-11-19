from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from watchdog.observers import Observer
from vse.model import Load_Yolo_model
from vse.controller.data_controller import NewImageController
from vse.data_access import crud, entities, schemas
from vse.data_access.database import SessionLocal, engine
entities.Base.metadata.create_all(bind=engine)
from CONFIG import IMAGES_DIR
from typing import List

# Load model
yolo = Load_Yolo_model()
# Start new image event handler
file_handler = NewImageController(IMAGES_DIR, yolo)
# event_handler = NewImageController(yolo)
# observer = Observer()
# observer.schedule(event_handler, IMAGES_DIR, recursive=True)
# observer.start()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# db = SessionLocal()
# print(crud.get_image_by_label(db, "person")[0].name)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# search by list of keywords and order by most hits of keywords
@app.get("/search/{name}", response_model=List[schemas.Image])
async def search(name: str, db: Session = Depends(get_db)):
    images = crud.get_image_by_label(db, name)
    return images


@app.get("/process")
async def process():
    result = file_handler.process_all()
    if result:
        return {"message": "done"}
    else:
        return {"message": "nothing to process.."}
