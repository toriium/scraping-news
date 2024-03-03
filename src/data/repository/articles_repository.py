from sqlalchemy import text

from src.domain.article import ArticleDomain
from src.data.db_orm.query_obj import delete_obj, insert_obj, select_all_obj, update_obj, create_reading_session
from src.data.db_orm.tables.tbl_articles import TblArticles
from src.data.dtos.articles_dto import ArticleDTO
from src.data.errors.sql_error import SQLError


class ArticlesRepository:
    @staticmethod
    def get_all_articles() -> tuple[list[ArticleDTO] | None, SQLError | None]:
        query_result = select_all_obj(obj_table=TblArticles, filter_by={})
        if query_result:
            articles = []
            for article in query_result:
                article = ArticleDTO.from_orm(article)
                articles.append(article)
            return articles, None
        else:
            return None, None

    @staticmethod
    def get_all_article_tags() -> tuple[set[str] | None, SQLError | None]:
        with create_reading_session() as session:
            sql_query = text("""SELECT DISTINCT unnest(tags) AS distinct_values FROM tbl_articles;""")
            query_result = session.execute(sql_query)
        tags = set()
        for tag in query_result:
            tag = tag[0]
            tags.add(tag)

        return tags, None

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

    @classmethod
    def query_number_of_articles_by_tags(cls, articles: list[ArticleDTO] = None) -> dict[str, int]:
        tags, err = cls.get_all_article_tags()
        if not articles:
            articles, err = cls.get_all_articles()

        articles_with_tags = {tag: 0 for tag in tags}
        for tag in tags:
            for article in articles:
                if tag in article.tags:
                    articles_with_tags[tag] += 1

        return articles_with_tags
