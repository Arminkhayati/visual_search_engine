from sqlalchemy.orm import Session
from vse.data_access import crud
from collections import defaultdict


class SearchImageLogic:
    def __init__(self, phrase: str):
        self.keywords = [k.strip() for k in phrase.split(",")]

    def process(self, db: Session):
        count_repeated_images = defaultdict(int)
        for k in self.keywords:
            images = crud.get_image_by_label(db, k)
            for image in images:
                count_repeated_images[image.path] += 1
        images = [k for k,_ in sorted(count_repeated_images.items(), key=lambda item: item[1], reverse=True)]
        return images
