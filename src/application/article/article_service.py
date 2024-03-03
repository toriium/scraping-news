
from src.application.article.article_error import ArticleError
from src.domain.article import ArticleDomain
from src.data.errors.sql_error import SQLError
from src.data.repository.articles_repository import ArticlesRepository
from src.data.dtos.articles_dto import CreateArticleDTO, ArticleDTO


class ArticleService:
    @staticmethod
    def find_book_by_id(book_id: int) -> tuple[ArticleDomain | None, ArticleError | None]:
        found_book, error = ArticlesRepository.get_all_articles(book_id=book_id)

        if not found_book:
            return None, None

        return ArticleDomain(**found_book.dict()), None

    @staticmethod
    def insert_article(data: CreateArticleDTO) -> tuple[ArticleDomain | None, ArticleError | None]:
        new_article = ArticleDomain(**data.dict())

        new_article, error = ArticlesRepository.insert_article(article=new_article)
        if error:
            if error == SQLError.duplicate_entry:
                return None, ArticleError.duplicate_entry

        return ArticleDomain(**new_article.dict()), None
