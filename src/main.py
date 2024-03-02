from src.crawlers.timesofmalta_crawler import TimesOfMaltaCrawler

from turbocrawler import CrawlerRunner
from turbocrawler.engine.data_types.crawler_runner_config import CrawlerRunnerConfig
from turbocrawler.queues.crawled_queue import MemoryCrawledQueue
from turbocrawler.queues.crawler_queues import FIFOMemoryCrawlerQueue

if __name__ == '__main__':
    config = CrawlerRunnerConfig(crawler_queue=FIFOMemoryCrawlerQueue,
                                 crawler_queue_params=None,
                                 crawled_queue=MemoryCrawledQueue,
                                 crawled_queue_params=dict(save_crawled_queue=True, load_crawled_queue=False),
                                 plugins=None, qtd_parse=2)
    result = CrawlerRunner(crawler=TimesOfMaltaCrawler, config=config).run()
    print(result)
