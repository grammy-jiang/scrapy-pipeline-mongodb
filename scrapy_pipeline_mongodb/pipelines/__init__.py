from abc import ABCMeta
from abc import abstractclassmethod
from abc import abstractmethod

from scrapy.crawler import Crawler
from scrapy.item import Item
from scrapy.spiders import Spider


class GenericPipeline(metaclass=ABCMeta):
    def __init__(self, crawler: Crawler, *args, **kwargs):
        self.crawler = crawler
        self.settings = crawler.settings
        self.__dict__.update(kwargs)

    @abstractclassmethod
    def from_crawler(cls, crawler: Crawler, *args, **kwargs):
        pass

    @abstractmethod
    def open_spider(self, spider: Spider):
        pass

    @abstractmethod
    def close_spider(self, spider: Spider):
        pass

    @abstractmethod
    def process_item(self, item: Item, spider: Spider) -> Item:
        return item
