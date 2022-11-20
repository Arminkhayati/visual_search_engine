from CONFIG import PROCESSED_IMAGES_DIR
from vse.model import detect_image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from vse.data_access import crud
from vse.data_access.database import SessionLocal
import uuid
import shutil
import os
import glob


class NewImageController:
    def __init__(self, path, model):
        self.model = model
        self.path = path

    def process_all(self):
        res = os.listdir(self.path)
        res = [os.path.join(self.path, f) for f in res]
        if not res: return False
        for file_path in res:
            # find objects
            labels = detect_image(self.model, file_path)
            # copy file with new name to processed directory
            _, filename = os.path.split(file_path)
            _, file_extension = os.path.splitext(filename)
            new_filename = str(uuid.uuid4()) + file_extension
            new_file_path = os.path.join(PROCESSED_IMAGES_DIR, new_filename)
            print(new_file_path)
            shutil.move(file_path, new_file_path)
            # write info to database
            db = SessionLocal()
            crud.create_image(db, new_file_path, labels)
            db.close()
        return True


# class NewImageController(FileSystemEventHandler):
#     def __init__(self, model):
#         self.model = model
#
#     def on_created(self, event):
#         file_path = event.src_path.strip()
#         labels = detect_image(self.model, file_path)
#         # copy file with new name to processed directory
#         _, filename = os.path.split(file_path)
#         _, file_extension = os.path.splitext(filename)
#         new_filename = str(uuid.uuid4()) + file_extension
#         new_file_path = os.path.join(PROCESSED_IMAGES_DIR, new_filename)
#         shutil.move(file_path, new_file_path)
#         # write info to database
#         db = SessionLocal()
#         crud.create_image(db, new_file_path, labels)
#         db.close()
