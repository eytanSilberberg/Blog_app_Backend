
from fastapi import APIRouter, HTTPException
from models.homePageData import HomePageData
import mysql.connector as mysql
from dotenv import load_dotenv
import os
import MySQLdb

router = APIRouter()

load_dotenv()

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
@router.get("/hpd/", response_model=HomePageData)
def get_homepage_data():
    cursor = db.cursor()
    query = "SELECT heading, paragraph FROM homePageData"
    cursor.execute(query)
    data = cursor.fetchone()
    if data:
        heading, paragraph = data
        return HomePageData(heading=heading, paragraph=paragraph)