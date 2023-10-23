from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

router = APIRouter(
    prefix="/api/paper",
)

@router.get("/hello")
def hello():
    return {"message": "Hello World!"}