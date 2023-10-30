from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from database import get_db
from pymysql.cursors import Cursor

import core.PaperApp.schema as paper_schema
import core.PaperApp.crud as paper_crud

router = APIRouter(
    prefix="/api/paper",
)

@router.get("/list", response_model=paper_schema.PaperList)
def get_paper_list(page: int = 0, size: int = 10, db: Cursor = Depends(get_db)):
    total, paper_list = paper_crud.get_paper_list(db=db, skip=page*size, limit=size)
    return {
        'total': total,
        'paper_list': paper_list
    }

@router.get("/detail/{paper_id}", response_model=paper_schema.Paper)
def get_paper_detail(paper_id: int, db: Cursor = Depends(get_db)):
    paper = paper_crud.get_paper(db=db, paper_id=paper_id)
    return paper

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_paper(paper_create: paper_schema.PaperCreate, db: Cursor = Depends(get_db)):
    paper_crud.create_paper(db=db, paper_create=paper_create)

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_paper(paper_id: int, db: Cursor = Depends(get_db)):
    db_paper = paper_crud.get_paper(db=db, paper_id=paper_id)
    if not db_paper:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    paper_crud.delete_paper(db=db, paper_id=paper_id)

"""
TODO
- access token 검증 기능 추가
- create_paper에서 구글 스칼라 기반 파싱 기능 구현
- update_paper 기능 구현
- like_paper 기능 구현
- withdraw_like_paper 기능 구현
- 상태 코드 및 API 명세서 정리
"""