from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from database import get_db
from pymysql.cursors import Cursor

import core.PaperApp.schema as paper_schema
import core.PaperApp.crud as paper_crud

from core.UserApp.schema import User
from core.UserApp.router import get_current_user

router = APIRouter(
    prefix="/api/paper",
)

@router.get("/list", response_model=paper_schema.PaperList)
def get_paper_list(page: int = 0,
                   size: int = 10,
                   db: Cursor = Depends(get_db)):
    total, paper_list = paper_crud.get_paper_list(db=db, skip=page*size, limit=size)
    return {
        'total': total,
        'paper_list': paper_list
    }

@router.get("/detail/{slug}", response_model=paper_schema.Paper)
def get_paper_detail(slug: str,
                     db: Cursor = Depends(get_db)):
    db_paper = paper_crud.get_paper_by_slug(db=db, slug=slug)
    return db_paper

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_paper(paper_create: paper_schema.PaperCreate,
                 db: Cursor = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    paper_crud.create_paper(db=db, paper_create=paper_create, user_id=current_user['id'])

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_paper(slug: str,
                 db: Cursor = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    db_paper = paper_crud.get_paper_by_slug(db=db, slug=slug)
    if (not db_paper) or (db_paper['user_id'] != current_user['id']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    paper_crud.delete_paper(db=db, paper_id=db_paper['id'])

@router.delete("/like", status_code=status.HTTP_201_CREATED)
def like_paper(slug: str,
               db: Cursor = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    db_paper = paper_crud.get_paper_by_slug(db=db, slug=slug)
    if not db_paper:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")

    db_paper_like = paper_crud.get_paper_like(db=db, paper_id=db_paper['id'], user_id=current_user['id'])
    if db_paper_like:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터가 이미 존재합니다.")
    
    paper_crud.like_paper(db=db, paper_id=db_paper['id'], user_id=current_user['id'])

@router.delete("/withdraw-like", status_code=status.HTTP_204_NO_CONTENT)
def withdraw_like_paper(slug: str,
               db: Cursor = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    db_paper = paper_crud.get_paper_by_slug(db=db, slug=slug)
    if not db_paper:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")

    db_paper_like = paper_crud.get_paper_like(db=db, paper_id=db_paper['id'], user_id=current_user['id'])
    if not db_paper_like:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    
    paper_crud.withdraw_like_paper(db=db, paper_id=db_paper['id'], user_id=current_user['id'])

"""
TODO
- create_paper에서 구글 스칼라 기반 파싱 기능 구현
- update_paper 기능 구현
- 상태 코드 및 API 명세서 정리
"""