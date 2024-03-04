
from src.application.article.article_error import ArticleError
from src.data.dtos.articles_dto import CreateArticleDTO
from src.data.errors.sql_error import SQLError
from src.data.repository.articles_repository import ArticlesRepository
from src.domain.article import ArticleDomain


class ArticleService:
    @staticmethod
    def insert_article(data: CreateArticleDTO) -> tuple[ArticleDomain | None, ArticleError | None]:
        new_article = ArticleDomain(**data.dict())

        new_article, error = ArticlesRepository.insert_article(article=new_article)
        if error:
            if error == SQLError.duplicate_entry:
                return None, ArticleError.duplicate_entry

        return ArticleDomain(**new_article.dict()), None
