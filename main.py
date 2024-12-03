from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import articles_crud
import models
import schemas
from database import engine, SessionLocal

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# Création des tables
models.Base.metadata.create_all(bind=engine)

# Dépendance pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/articles/", response_model=schemas.ArticleResponse)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    return articles_crud.create_article(db, article)

@app.get("/articles/{article_id}", response_model=schemas.ArticleResponse)
def read_article(article_id: int, db: Session = Depends(get_db)):
    db_article = articles_crud.get_article(db, article_id)
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

@app.get("/articles/", response_model=list[schemas.ArticleResponse])
def read_articles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return articles_crud.get_articles(db, skip=skip, limit=limit)

@app.delete("/articles/{article_id}", response_model=schemas.ArticleResponse)
def delete_article(article_id: int, db: Session = Depends(get_db)):
    db_article = articles_crud.delete_article(db, article_id)
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article
