from datetime import date

from pydantic import BaseModel


class ArticleDTO(BaseModel):
    id: int
    url: str
    title: str
    tags: list[str]
    reading_time: str
    img_path: str

    class Config:
        from_attributes = True


class CreateArticleDTO(BaseModel):
    url: str
    title: str
    tags: list[str]
    reading_time: str
    img_path: str
