from fastapi import FastAPI
from .api import book_user, rating_user

app = FastAPI(title="Book Recommendation API")

# Include routers
app.include_router(book_user.router, prefix="/books", tags=["Books"])
app.include_router(rating_user.router, prefix="/ratings", tags=["Ratings"])
# TODO: add maintainer api

@app.get("/")
def root():
    return {"message": "Book Recommendation API running"}
