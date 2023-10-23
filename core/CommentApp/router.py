from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import RedirectResponse
from starlette import status

import core.PaperApp.schema as paper_schema
import core.PaperApp.crud as paper_crud

import core.CommentApp.schema as comment_schema
import core.CommentApp.crud as comment_crud

router = APIRouter(
    prefix="/api/comment",
)

@router.get("/list/{paper_id}", response_model=comment_schema.CommentList)
def get_comment_list(paper_id: int, page: int = 0, size: int = 10):
    total, comment_list = comment_crud.get_comment_list(paper_id=paper_id, skip=page*size, limit=size)
    return {
        'total': total,
        'comment_list': comment_list
    }

@router.post("/create", response_model=paper_schema.Paper)
def create_comment(paper_id: int, content: str):

    paper = paper_crud.get_paper(paper_id=paper_id)
    if not paper:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="paper not found")
    comment_crud.create_comment(paper_id=paper_id, content=content)

    # redirect
    from core.PaperApp.router import router as paper_router
    url = paper_router.url_path_for('get_paper_detail', paper_id=paper_id)
    return RedirectResponse(url, status_code=303)

@router.put("/update", status_code=status.HTTP_201_CREATED)
def comment_update(comment_id: int, content: str):
    db_comment = comment_crud.get_comment(comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    comment_crud.update_comment(comment_id=comment_id, content=content)
    
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def comment_delete(comment_id: int):
    db_comment = comment_crud.get_comment(comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    comment_crud.delete_comment(comment_id=comment_id)

"""
TODO
- 실제 DB 연동
- access token 검증 기능 추가
- like_comment 기능 구현
- withdraw_like_comment 기능 구현
- 상태 코드 및 API 명세서 정리
"""