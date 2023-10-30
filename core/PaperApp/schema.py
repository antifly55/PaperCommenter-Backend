import datetime

from pydantic import BaseModel

class Paper(BaseModel):
    slug: str
    title: str
    authors: str
    publish_year: int
    publisher: str
    site_url: str
    paper_url: str
    
    create_datetime: datetime.datetime
    modify_datetime: datetime.datetime | None = None

    like_count: int
    comment_count: int

class PaperCreate(BaseModel):
    slug: str
    title: str
    authors: str
    publish_year: int
    publisher: str
    site_url: str
    paper_url: str

class PaperList(BaseModel):
    total: int = 0
    paper_list: list[Paper] = []