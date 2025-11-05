from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy import text
from sqlmodel import Session, SQLModel, select

from .database import engine, get_session
from .models import Post  

# Crea tablas de SQLModel (requiere que models esté importado)
SQLModel.metadata.create_all(engine)

app = FastAPI()

class PostIn(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

@app.get("/sqlalchemy-health", status_code=status.HTTP_200_OK)
def get_sqlalchemy_health(db: Session = Depends(get_session)):
    db.execute(text("SELECT 1"))
    return {"status": "ok"}

# Conexión psycopg2 (bloqueante hasta que conecte)
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",       # <-- igual que en database.py
            user="postgres",
            password="postgres",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as e:
        print("Database connection failed!", e)
        time.sleep(2)

@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts(db: Session = Depends(get_session)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.exec(select(Post)).all()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: PostIn, db: Session = Depends(get_session)):
    # cursor.execute(
    #     "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_a_post(id: int, db: Session = Depends(get_session)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    # post = cursor.fetchone()
    post = db.get(models.Post, id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {id} was not found")
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    deleted = cursor.fetchone()
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Post {id} was not found")
    conn.commit()
    return {}

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    cursor.execute(
        "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
        (post.title, post.content, post.published, id),
    )
    updated = cursor.fetchone()
    if not updated:
        raise HTTPException(status_code=404, detail=f"Post {id} was not found")
    conn.commit()
    return {"data": updated}
