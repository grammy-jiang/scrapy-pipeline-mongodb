import logging
from typing import Generator

from pymongo import MongoClient
from pymongo.errors import OperationFailure
from scrapy.crawler import Crawler
from scrapy.item import Item
from scrapy.spiders import Spider
from txmongo import filter as txfilter

from . import GenericPipeline
from ..settings.default_settings import MONGODB_COLLECTION
from ..settings.default_settings import MONGODB_DATABASE
from ..settings.default_settings import MONGODB_INDEXES
from ..signals import insert_for_objectid
from ..signals import update_for_objectid
from ..utils.get_mongodb_uri import get_mongodb_uri

logger = logging.getLogger(__name__)


class PipelineMongoDB(GenericPipeline):
    def __init__(self, crawler: Crawler, *args, **kwargs):
        super().__init__(crawler, *args, **kwargs)
        self._uri = get_mongodb_uri(self.settings)
        self._cnx = MongoClient(self._uri)
        self._db = self._cnx.get_database(self.settings[MONGODB_DATABASE])
        self._coll = self._db.get_collection(self.settings[MONGODB_COLLECTION])

    @classmethod
    def from_crawler(cls, crawler: Crawler, *args, **kwargs):
        o = cls(crawler=crawler, *args, **kwargs)
        crawler.signals.connect(o.insert, signal=insert_for_objectid)
        crawler.signals.connect(o.update, signal=update_for_objectid)
        return o

    def open_spider(self, spider: Spider):
        for index in self.settings.get(MONGODB_INDEXES, list()):
            try:
                self._coll.create_index(
                    txfilter.sort(txfilter.ASCENDING(index)))
            except OperationFailure:
                pass
        logger.info('Spider opened: Open the connection to MongoDB: %s',
                    self._uri)

    def close_spider(self, spider: Spider):
        self._cnx.disconnect()
        logger.info('Spider closed: Close the connection to MongoDB %s',
                    self._uri)

    def process_item(self, item: Item, spider: Spider) -> Generator:
        return self._coll.insert_one(item)

    def insert(self, item: Item, spider: Spider) -> Generator:
        return self._coll.process_item_insert_one(item)

    def update(self, item: Item, spider: Spider) -> Generator:
        return self._coll.process_item_update_one(item)
