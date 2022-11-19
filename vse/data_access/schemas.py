from typing import List, Union
from pydantic import BaseModel


class LabelBase(BaseModel):
    label: str


class LabelCreate(LabelBase):
    pass


class Label(LabelBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class ImageBase(BaseModel):
    path: str


class ImageCreate(ImageBase):
    pass


class Image(ImageBase):
    id: int
    labels: List[Label] = []

    class Config:
        orm_mode = True
