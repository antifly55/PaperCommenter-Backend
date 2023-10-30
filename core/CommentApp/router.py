from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import RedirectResponse
from starlette import status

from database import get_db
from pymysql.cursors import Cursor

import core.PaperApp.schema as paper_schema
import core.PaperApp.crud as paper_crud

import core.CommentApp.schema as comment_schema
import core.CommentApp.crud as comment_crud

router = APIRouter(
    prefix="/api/comment",
)

@router.get("/list/{slug}", response_model=comment_schema.CommentList)
def get_comment_list(slug: str, page: int = 0, size: int = 10, db: Cursor = Depends(get_db)):

    db_paper = paper_crud.get_paper_by_slug(db=db, slug=slug)
    if not db_paper:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="paper not found")

    total, comment_list = comment_crud.get_comment_list(db=db, paper_id=db_paper['id'], skip=page*size, limit=size)
    return {
        'total': total,
        'comment_list': comment_list
    }

@router.post("/create", response_model=paper_schema.Paper)
def create_comment(slug: str, content: str, db: Cursor = Depends(get_db)):

    db_paper = paper_crud.get_paper_by_slug(db=db, slug=slug)
    if not db_paper:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="paper not found")
    
    comment_crud.create_comment(db=db, paper_id=db_paper['id'], content=content)

    # redirect
    from core.PaperApp.router import router as paper_router
    url = paper_router.url_path_for('get_paper_detail', paper_id=db_paper['id'])
    return RedirectResponse(url, status_code=303)

@router.put("/update", status_code=status.HTTP_201_CREATED)
def comment_update(comment_uuid: int, content: str, db: Cursor = Depends(get_db)):
    db_comment = comment_crud.get_comment_by_uuid(db=db, comment_uuid=comment_uuid)
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    comment_crud.update_comment(db=db, comment_id=db_comment['id'], content=content)
    
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def comment_delete(comment_uuid: int, db: Cursor = Depends(get_db)):
    db_comment = comment_crud.get_comment_by_uuid(db=db, comment_uuid=comment_uuid)
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    comment_crud.delete_comment(db=db, comment_id=db_comment['id'])

"""
TODO
- access token 검증 기능 추가
- like_comment 기능 구현
- withdraw_like_comment 기능 구현
- 상태 코드 및 API 명세서 정리
"""