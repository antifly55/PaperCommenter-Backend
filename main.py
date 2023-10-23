from fastapi import FastAPI

from core.PaperApp import router as paper_router
# from core.CommentApp import router as comment_router
# from core.UserApp import router as user_router

app = FastAPI()

app.include_router(paper_router.router)
# app.include_router(comment_router.router)
# app.include_router(user_router.router)