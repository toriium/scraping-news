import requests
from selectolax.lexbor import LexborHTMLParser
from selenium_toolkit import SeleniumToolKit
from turbocrawler import Crawler, CrawlerRequest, CrawlerResponse, ExecutionInfo, ExtractRule
from turbocrawler.engine.control import StopCrawler
import json

from src.application.article.article_error import ArticleError
from src.application.article.article_service import ArticleService
from src.crawlers.request_utils import download_file
from src.crawlers.selenium_manager import get_selenium_webdriver
from src.data.dtos.articles_dto import CreateArticleDTO
from src.settings import IMAGES_PATH


class TimesOfMaltaCrawler(Crawler):
    crawler_name = "TimesOfMaltaCrawler"
    allowed_domains = ['timesofmalta.com']
    regex_extract_rules = [ExtractRule(r'https://timesofmalta.com/page/[0-9]')]
    time_between_requests = 2
    session: requests.Session
    selenium_kit: SeleniumToolKit

    @classmethod
    def start_crawler(cls) -> None:
        cls.session = requests.session()
        cls.selenium_kit = get_selenium_webdriver()

    @classmethod
    def crawler_first_request(cls) -> CrawlerResponse | None:
        url = "https://timesofmalta.com/news/latest"
        response = cls.session.get(url=url)
        selector = LexborHTMLParser(response.text)
        articles_data = selector.css_first('[id="listing-ld"]')
        if not articles_data:
            raise StopCrawler(reason="Unable to find articles tags in the main Page")

        articles_data = articles_data.text()
        articles_data = json.loads(articles_data).get('@graph')

        latest_articles = []
        for article in articles_data:
            keywords = article.get('keywords')
            if keywords:
                keywords = keywords.split(",")

            latest_articles.append({
                "url": article.get('url'),
                "title": article.get('name'),
                "tags": keywords,
            })

        for article in latest_articles:
            req = CrawlerRequest(url=article["url"], kwargs=article)
            cls.crawler_queue.add(req)

        return None

    @classmethod
    def process_request(cls, crawler_request: CrawlerRequest) -> CrawlerResponse:
        url = crawler_request.url
        cls.selenium_kit.goto(url)
        body = cls.selenium_kit.driver.page_source
        return CrawlerResponse(url=url,
                               body=body,
                               status_code=200)

    @classmethod
    def parse(cls, crawler_request: CrawlerRequest, crawler_response: CrawlerResponse) -> None:
        selector = LexborHTMLParser(crawler_response.body)

        # Download main image
        css_main_image = 'img[class="wi-WidgetSubCompType_13-img wi-WidgetImage loaded"]'
        main_image_url = selector.css_first(css_main_image)
        if main_image_url:
            main_image_url = main_image_url.attrs.get('src')
        else:
            cls.logger.info(f"{crawler_request.url} article doesn't have image")
            return
        img_name = main_image_url.split("/")[-1]
        download_file(main_image_url, output_path=IMAGES_PATH, filename=img_name)

        reading_time = selector.css_first('[class="wi-WidgetMeta-readingTime"]>span')
        if reading_time:
            reading_time = reading_time.text().split('read')[0].strip()

        data = {
            "url": crawler_request.kwargs.get('url'),
            "title": crawler_request.kwargs.get('title'),
            "tags": crawler_request.kwargs.get('tags'),
            "reading_time": reading_time,
            "img_path": img_name,
        }
        new_article = CreateArticleDTO(**data)
        _, err = ArticleService.insert_article(new_article)
        if err:
            if err == ArticleError.duplicate_entry:
                cls.logger.info(f"{data['url']} article already saved")
                return
        cls.logger.info(data)

    @classmethod
    def stop_crawler(cls, execution_info: ExecutionInfo) -> None:
        cls.session.close()
        if cls.selenium_kit.webdriver_is_open():
            cls.selenium_kit.driver.quit()
