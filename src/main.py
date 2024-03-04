from turbocrawler import CrawlerRunner

from src.crawlers.timesofmalta_crawler import TimesOfMaltaCrawler
from src.data.db_orm.migrations import run_migrations
from src.data.repository.articles_repository import ArticlesRepository
from src.settings import REPORTS_PATH
from src.utils.date_utils import now_timestamp_str
from src.utils.email_utils import send_email
from src.utils.sheets_utils import create_sheet


def run_crawler() -> str | None:
    error = None
    try:
        result = CrawlerRunner(crawler=TimesOfMaltaCrawler).run()
        if result['forced_stop']:
            error = result['reason']
    except Exception as e:
        error = str(e)
    return error


def send_report_email(crawler_error: str | None = None):
    subject = "TimesOfMaltaCrawler Report"

    if crawler_error:
        body = f"""
        Report of TimesOfMaltaCrawler
        Date: {now_timestamp_str()}
        The following error happened while executing {crawler_error}
        """
        send_email(subject=subject, body=body)
        return

    articles, _ = ArticlesRepository.get_all_articles()
    number_of_articles_by_tags = ArticlesRepository.query_number_of_articles_by_tags(articles=articles)

    # Creating report sheet report file
    dict_articles = [article.dict() for article in articles]
    filename = f"{now_timestamp_str()}_articles.xlsx"
    sheet_path = create_sheet(data=dict_articles, output_path=REPORTS_PATH, filename=filename)

    body = f"""
    Report of TimesOfMaltaCrawler
    Date: {now_timestamp_str()}
    Articles by Tags: 
    {number_of_articles_by_tags}
    """
    send_email(subject=subject, body=body, attachment_file_paths=[sheet_path])


if __name__ == '__main__':
    run_migrations()
    run_crawler()
    send_report_email()
