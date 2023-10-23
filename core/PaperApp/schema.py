import datetime

from pydantic import BaseModel

class Paper(BaseModel):
    id: int

    title: str
    abstract: str
    year: int
    publisher: str
    url: str
    
    create_datetime: datetime.datetime
    modify_datetime: datetime.datetime | None = None

class PaperCreate(BaseModel):
    title: str
    abstract: str
    year: int
    publisher: str
    url: str
    content: str

class PaperDetail(Paper):
    content: str

class PaperList(BaseModel):
    total: int = 0
    paper_list: list[Paper] = []