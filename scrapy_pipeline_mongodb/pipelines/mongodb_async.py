import logging
from typing import Dict
from typing import Generator

from bson.codec_options import DEFAULT_CODEC_OPTIONS
from pymongo.errors import OperationFailure
from scrapy.crawler import Crawler
from scrapy.exceptions import NotConfigured
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.utils.misc import load_object
from twisted.internet.defer import inlineCallbacks
from txmongo import filter as txfilter
from txmongo.connection import ConnectionPool

from . import GenericPipeline
from ..settings.default_settings import MONGODB_COLLECTION
from ..settings.default_settings import MONGODB_DATABASE
from ..settings.default_settings import MONGODB_INDEXES
from ..settings.default_settings import MONGODB_PROCESS_ITEM
from ..signals import insert_for_objectid
from ..signals import update_for_objectid
from ..utils.get_mongodb_uri import get_mongodb_uri

logger = logging.getLogger(__name__)


class PipelineMongoDBAsync(GenericPipeline):
    def __init__(self, crawler: Crawler, *args, **kwargs):
        super().__init__(crawler, *args, **kwargs)

        self.uri = get_mongodb_uri(self.settings)
        self.codec_options = DEFAULT_CODEC_OPTIONS.with_options(
            unicode_decode_error_handler='ignore')
        self.cnx = None
        self.db = None
        self.coll = None

    @classmethod
    def from_crawler(cls, crawler: Crawler, *args, **kwargs):
        o = cls(crawler=crawler, *args, **kwargs)
        crawler.signals.connect(o.process_item_insert_one,
                                signal=insert_for_objectid)
        crawler.signals.connect(o.process_item_update_one,
                                signal=update_for_objectid)
        return o

    @inlineCallbacks
    def open_spider(self, spider: Spider):
        self.cnx = ConnectionPool(self.uri, codec_options=self.codec_options)
        self.db = getattr(self.cnx, self.settings[MONGODB_DATABASE])
        self.coll = getattr(self.db, self.settings[MONGODB_COLLECTION])
        self.coll.with_options(codec_options=self.codec_options)

        result = yield self.create_index(spider)
        logger.info('Spider opened: Open the connection to MongoDB: %s',
                    self.uri)

    # TODO: ADD UNIT TEST FOR THIS FUNCTION
    # the api of create_index in txmongo is different with the one in mongomock
    @inlineCallbacks
    def create_index(self, spider: Spider):
        results = []
        for field, _order in self.settings.get(MONGODB_INDEXES, list()):
            try:
                _ = yield self.coll.create_index(txfilter.sort(_order(field)))
                results.append(_)
            except OperationFailure:
                pass
        return results

    @inlineCallbacks
    def close_spider(self, spider: Spider):
        yield self.cnx.disconnect()
        logger.info('Spider closed: Close the connection to MongoDB %s',
                    self.uri)

    @inlineCallbacks
    def process_item(self, item: Item, spider: Spider) -> Generator:
        process_item = load_object(
            self.settings[MONGODB_PROCESS_ITEM]
            if self.settings.get(MONGODB_PROCESS_ITEM)
            else 'scrapy_pipeline_mongodb.utils.process_item.process_item'
        )

        result = yield process_item(self, item, spider)
        return result

    @inlineCallbacks
    def process_item_insert_one(self, item: Item, spider: Spider) -> Generator:
        result = yield self.coll.insert_one(item)
        return result

    @inlineCallbacks
    def process_item_update_one(self, filter_: Dict, update: Dict,
                                upsert: bool, spider: Spider) -> Generator:
        result = yield self.coll.update_one(filter=filter_,
                                           update=update,
                                           upsert=upsert)
        return result
