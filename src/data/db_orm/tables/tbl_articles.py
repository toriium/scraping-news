from sqlalchemy import Column, Date, Integer, String, Text, ARRAY

from src.data.db_orm.tables.base import Base


class TblArticles(Base):
    __tablename__ = 'tbl_articles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(500), nullable=False, unique=True)
    title = Column(String(500), nullable=False)
    tags = Column(ARRAY(String), nullable=False)
    reading_time = Column(String(50), nullable=False)
    img_path = Column(String(500), nullable=False)
