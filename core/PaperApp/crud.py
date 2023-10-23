from datetime import datetime

from core.PaperApp.schema import PaperCreate

from sqlalchemy.orm import Session

PAPERS = [
    {
        'id': 1,
        'user_id': 1,
        'title': 'fit a spread',
        'abstract': 'estimator',
        'year': 2009,
        'publisher': 'IEEE INFOCOM',
        'url': 'http://3.141592',
        'content': "asdfjok;ln",
        'create_datetime': datetime.now(),
        'modify_datetime': datetime.now()
    },
    {
        'id': 2,
        'user_id': 1,
        'title': 'fit a spread',
        'abstract': 'estimator',
        'year': 2009,
        'publisher': 'IEEE INFOCOM',
        'url': 'http://3.141592',
        'content': "asdfjok;ln",
        'create_datetime': datetime.now(),
        'modify_datetime': datetime.now()
    },
    {
        'id': 3,
        'user_id': 1,
        'title': 'fit a spread',
        'abstract': 'estimator',
        'year': 2009,
        'publisher': 'IEEE INFOCOM',
        'url': 'http://3.141592',
        'content': "asdfjok;ln",
        'create_datetime': datetime.now(),
        'modify_datetime': datetime.now()
    },
]

def get_paper_list(skip: int = 0, limit: int = 10):
    _paper_list = PAPERS
    total = len(PAPERS)
    paper_list = _paper_list[skip : skip + limit]
    return total, paper_list

def get_paper(paper_id: int):
    for paper in PAPERS:
        if paper['id']==paper_id:
            return paper

def create_paper(paper_create: PaperCreate):
    PAPERS.append({
        'id': 3,
        'user_id': 1,
        'title': 'fit a spread',
        'abstract': 'estimator',
        'year': 2009,
        'publisher': 'IEEE INFOCOM',
        'url': 'http://3.141592',
        'content': "asdfjok;ln",
        'create_datetime': datetime.now(),
        'modify_datetime': datetime.now()
    })

def delete_paper(paper_id: int):
    for idx in range(len(PAPERS)):
        if PAPERS[idx]['id']==paper_id:
            PAPERS.pop(idx)
            break