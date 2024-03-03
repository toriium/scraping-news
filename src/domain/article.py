from pydantic import BaseModel


class ArticleDomain(BaseModel):
    id: int = None
    url: str
    title: str
    tags: list[str]
    reading_time: str
    img_path: str
