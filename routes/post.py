# app/routes/posts.py

from fastapi import APIRouter, HTTPException
from typing import List
from models.post import Post, PostToSave
import mysql.connector as mysql
import uuid
import datetime

router = APIRouter()

from dotenv import load_dotenv
load_dotenv()
import os
import MySQLdb

db = MySQLdb.connect(
  host= os.getenv("HOST"),
  user=os.getenv("USERNAME"),
  passwd= os.getenv("PASSWORD"),
  db= os.getenv("DATABASE"),
  autocommit = True,
  ssl_mode = "VERIFY_IDENTITY",
  ssl      = {
    "ca": "/etc/ssl/cert.pem"
  }
)


class Response:
    def __init__(self, res: str, data: List[Post], timeStamp: float):
        self.res = res
        self.data = data
        self.timeStamp = timeStamp


@router.post("/posts/", response_model=Post)
async def create_post(post: PostToSave):
    cursor = db.cursor()
    id = str(uuid.uuid4())
    query = "INSERT INTO posts (id, title, description, image) VALUES (%s, %s, %s, %s)"
    values = ( id,post.title, post.description, post.image)
    cursor.execute(query, values)
    db.commit()
    new_post = Post(id=id, title=post.title, description=post.description, image=post.image)
    return new_post

@router.get("/posts/{post_id}", response_model=Post)
def read_post(post_id: str):
    cursor = db.cursor()
    query = "SELECT id, title, description, image FROM posts WHERE id = %s"
    cursor.execute(query, (post_id,))
    result = cursor.fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return Post(id=result[0], title=result[1], description=result[2], image=result[3])




@router.put("/posts/{post_id}", response_model=Post)
def update_post(post_id: str, post: Post):
    cursor = db.cursor()
    query = "UPDATE posts SET title = %s, description = %s, image = %s WHERE id = %s"
    values = (post.title, post.description, post.image, post_id)
    cursor.execute(query, values)
    db.commit()
    return post

@router.delete("/posts/{post_id}")
def delete_post(post_id: str):
    cursor = db.cursor()
    query = "DELETE FROM posts WHERE id = %s"
    cursor.execute(query, (post_id,))
    db.commit()
    return {"message": "Post deleted successfully"}

@router.get("/posts/")
def get_all_posts():
    cursor = db.cursor()
    query = "SELECT id, title, description, image FROM posts"
    cursor.execute(query)
    results = cursor.fetchall()

    posts = []
    for result in results:
        post = Post(id=result[0], title=result[1], description=result[2], image=result[3])
        posts.append(post)

    response_data = Response(res="ok", data=posts, timeStamp=datetime.datetime.now().timestamp())
    return response_data

