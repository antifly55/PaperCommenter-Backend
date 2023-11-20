from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import RedirectResponse
from starlette import status

from database import get_db
from pymysql.cursors import Cursor

import core.PaperApp.schema as paper_schema
import core.PaperApp.crud as paper_crud
from core.PaperApp.router import router as paper_router

import core.CommentApp.schema as comment_schema
import core.CommentApp.crud as comment_crud

from core.UserApp.schema import User
from core.UserApp.router import get_current_user


router = APIRouter(
    prefix="/api/comment",
)


@router.get("/list/{slug}", response_model=comment_schema.CommentList)
def get_comment_list(slug: str,
                     page: int = 0,
                     size: int = 10,
                     db: Cursor = Depends(get_db)):

    db_paper = paper_crud.get_paper_by_slug(db=db, slug=slug)
    if not db_paper:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="데이터를 찾을수 없습니다.")

    total, comment_list = comment_crud.get_comment_list(db=db, paper_id=db_paper['id'], skip=page*size, limit=size)
    return {
        'total': total,
        'comment_list': comment_list
    }

@router.post("/create", response_model=paper_schema.Paper)
def create_comment(comment_create: comment_schema.CommentCreate,
                   db: Cursor = Depends(get_db),
                   current_user: User = Depends(get_current_user)):

    db_paper = paper_crud.get_paper_by_slug(db=db, slug=comment_create.slug)
    if not db_paper:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="데이터를 찾을수 없습니다.")
    
    comment_crud.create_comment(db=db, paper_id=db_paper['id'], user_id=current_user['id'],\
                                username=current_user['username'], content=comment_create.content)

    # redirect
    url = paper_router.url_path_for('get_paper_detail', slug=db_paper['slug'])
    return RedirectResponse(url, status_code=status.HTTP_303_SEE_OTHER)

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def update_comment(comment_update: comment_schema.CommentUpdate,
                   db: Cursor = Depends(get_db),
                   current_user: User = Depends(get_current_user)):

    db_comment = comment_crud.get_comment_by_hashed_identifier(db=db, hashed_identifier=comment_update.prev_hashed_identifier)
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    
    elif db_comment['user_id'] != current_user['id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="인가된 사용자가 아닙니다.")
    
    comment_crud.update_comment(db=db, comment_id=db_comment['id'], content=comment_update.new_content)
    
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(prev_hashed_identifier: str,
                   db: Cursor = Depends(get_db),
                   current_user: User = Depends(get_current_user)):

    db_comment = comment_crud.get_comment_by_hashed_identifier(db=db, hashed_identifier=prev_hashed_identifier)
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    
    elif db_comment['user_id'] != current_user['id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="인가된 사용자가 아닙니다.")
    
    comment_crud.delete_comment(db=db, comment_id=db_comment['id'])

@router.post("/like", status_code=status.HTTP_201_CREATED)
def like_comment(hashed_identifier: str,
               db: Cursor = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    
    db_comment = comment_crud.get_comment_by_hashed_identifier(db=db, hashed_identifier=hashed_identifier)
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")

    db_comment_like = comment_crud.get_comment_like(db=db, comment_id=db_comment['id'], user_id=current_user['id'])
    if db_comment_like:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="데이터가 이미 존재합니다.")
    
    comment_crud.like_comment(db=db, comment_id=db_comment['id'], user_id=current_user['id'])

@router.delete("/withdraw-like", status_code=status.HTTP_204_NO_CONTENT)
def withdraw_like_comment(hashed_identifier: str,
               db: Cursor = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    
    db_comment = comment_crud.get_comment_by_hashed_identifier(db=db, hashed_identifier=hashed_identifier)
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")

    db_comment_like = comment_crud.get_comment_like(db=db, comment_id=db_comment['id'], user_id=current_user['id'])
    if not db_comment_like:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    
    comment_crud.withdraw_like_comment(db=db, comment_id=db_comment['id'], user_id=current_user['id'])

"""
TODO
- 상태 코드 및 API 명세서 정리
"""