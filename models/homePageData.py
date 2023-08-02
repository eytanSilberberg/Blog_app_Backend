from pydantic import BaseModel


class HomePageData(BaseModel):
    heading: str
    paragraph: str