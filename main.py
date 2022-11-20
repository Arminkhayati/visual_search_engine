from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from watchdog.observers import Observer
from vse.model import Load_Yolo_model
from vse.controller import NewImageController
from vse.data_access import crud, entities, schemas
from vse.data_access.database import SessionLocal, engine
entities.Base.metadata.create_all(bind=engine)
from CONFIG import IMAGES_DIR
from typing import List
from vse.request_model import SearchRequestModel
from vse.logic import SearchImageLogic

## Load model
yolo = Load_Yolo_model()


app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
async def root():
    return {"message": "Welcome to our visual search engine..."}


# search by list of keywords and order images by most hits of keywords
@app.post("/search/", response_model=List[str])
async def search(search: SearchRequestModel, db: Session = Depends(get_db)):

    sil = SearchImageLogic(search.phrase)
    images = sil.process(db)
    return images

@app.get("/process")
async def process():
    ## Start new image event handler
    file_handler = NewImageController(IMAGES_DIR, yolo)
    result = file_handler.process_all()
    if result:
        return {"message": "done"}
    else:
        return {"message": "nothing to process.."}
