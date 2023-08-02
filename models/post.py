from pydantic import BaseModel

class Post(BaseModel):
    id: str
    title: str
    description: str
    image: str

class PostToSave(BaseModel):
    title: str
    description: str
    image: str