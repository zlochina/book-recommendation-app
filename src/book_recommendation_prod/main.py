from fastapi import FastAPI
from .api import book_user, rating_user
from .services.utils import init_pseudo_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- startup ----
    (app.state.ratings,
     app.state.books,
     app.state.dataset_preprocessed) = init_pseudo_db()
    print("✅ DataFrame db loaded at startup")

    yield

    # ---- shutdown ----
    # (optional) cleanup if needed
    print("👋 Backend shutting down, cleaning up...")

app = FastAPI(title="Book Recommendation API", lifespan=lifespan)

# Include routers
app.include_router(book_user.router, prefix="/books", tags=["Books"])
app.include_router(rating_user.router, prefix="/ratings", tags=["Ratings"])
# TODO: add maintainer api

@app.get("/")
def root():
    return {"message": "Book Recommendation API running"}
