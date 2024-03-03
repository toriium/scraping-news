from src.domain.article import ArticleDomain
from src.data.db_orm.query_obj import delete_obj, insert_obj, select_first_obj, update_obj
from src.data.db_orm.tables.tbl_articles import TblArticles
from src.data.dtos.articles_dto import ArticleDTO
from src.data.errors.sql_error import SQLError


class ArticlesRepository:
    @staticmethod
    def get_all_articles(book_id: int) -> tuple[ArticleDTO | None, SQLError | None]:
        query_result = select_first_obj(obj_table=TblArticles, filter_by={"id": book_id})
        if query_result:
            return ArticleDTO.from_orm(query_result), None
        else:
            return None, None

    @staticmethod
    def insert_article(article: ArticleDomain) -> tuple[ArticleDTO | None, SQLError | None]:
        new_article = TblArticles()
        new_article.url = article.url
        new_article.title = article.title
        new_article.tags = article.tags
        new_article.reading_time = article.reading_time
        new_article.img_path = article.img_path

        query_result, error = insert_obj(obj=new_article)
        if error:
            if error == SQLError.duplicate_entry:
                return None, SQLError.duplicate_entry

        if query_result:
            return ArticleDTO.model_validate(query_result), None
        else:
            return None, None
