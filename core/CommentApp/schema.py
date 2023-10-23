import datetime

from pydantic import BaseModel

class Comment(BaseModel):
    id: int
    content: str

    create_datetime: datetime.datetime
    modify_datetime: datetime.datetime | None = None

class CommentList(BaseModel):
    total: int = 0
    comment_list: list[Comment] = []