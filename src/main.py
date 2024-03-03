from src.crawlers.timesofmalta_crawler import TimesOfMaltaCrawler
from src.settings import REPORTS_PATH
from turbocrawler import CrawlerRunner
from turbocrawler.engine.data_types.crawler_runner_config import CrawlerRunnerConfig
from turbocrawler.queues.crawled_queue import MemoryCrawledQueue
from turbocrawler.queues.crawler_queues import FIFOMemoryCrawlerQueue

from src.data.db_orm.migrations import run_migrations
from src.data.repository.articles_repository import ArticlesRepository
from src.utils.date_utils import now_timestamp_str
from src.utils.email_utils import send_email
from src.utils.sheets_utils import create_sheet


def run_crawler():
    config = CrawlerRunnerConfig(crawler_queue=FIFOMemoryCrawlerQueue,
                                 crawler_queue_params=None,
                                 crawled_queue=MemoryCrawledQueue,
                                 crawled_queue_params=dict(save_crawled_queue=True, load_crawled_queue=False),
                                 plugins=None, qtd_parse=2)
    result = CrawlerRunner(crawler=TimesOfMaltaCrawler, config=config).run()
    if result['forced_stop']:
        raise ValueError(result['reason'])


def send_report_email():
    articles, _ = ArticlesRepository.get_all_articles()
    number_of_articles_by_tags = ArticlesRepository.query_number_of_articles_by_tags(articles=articles)

    # Creating report sheet report file
    dict_articles = [article.dict() for article in articles]
    filename = f"{now_timestamp_str()}_articles.xlsx"
    sheet_path = create_sheet(data=dict_articles, output_path=REPORTS_PATH, filename=filename)

    subject = "test mail"
    body = f"""
    Report of TimesOfMaltaCrawler
    Date: {now_timestamp_str()}
    Articles by Tags: {number_of_articles_by_tags}
    """
    send_email(subject=subject, body=body, attachment_file_paths=[sheet_path])


if __name__ == '__main__':
    run_migrations()
    # run_crawler()
    send_report_email()
