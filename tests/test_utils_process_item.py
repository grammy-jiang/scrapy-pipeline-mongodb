import pprint

import mongomock
from scrapy import Field
from scrapy import Item
from scrapy import Spider
from scrapy.utils.test import get_crawler
from twisted.internet import defer
from twisted.trial.unittest import TestCase

from scrapy_pipeline_mongodb.pipelines.mongodb_async import PipelineMongoDBAsync
from scrapy_pipeline_mongodb.settings.default_settings import MONGODB_COLLECTION
from scrapy_pipeline_mongodb.settings.default_settings import MONGODB_DATABASE
from scrapy_pipeline_mongodb.settings.default_settings import MONGODB_HOST
from scrapy_pipeline_mongodb.settings.default_settings import MONGODB_OPTIONS_
from scrapy_pipeline_mongodb.settings.default_settings import MONGODB_PASSWORD
from scrapy_pipeline_mongodb.settings.default_settings import MONGODB_PORT
from scrapy_pipeline_mongodb.settings.default_settings import MONGODB_USERNAME
from scrapy_pipeline_mongodb.utils.process_item import process_item

pp = pprint.PrettyPrinter(indent=4)


class ItemTest(Item):
    _id = Field()
    field_0 = Field()
    field_1 = Field()


class ProcessItemTest(TestCase):
    settings_dict = {
        MONGODB_COLLECTION: 'test_mongodb_async',
        MONGODB_DATABASE: 'test_mongodb_async',
        MONGODB_HOST: 'localhost',
        # MONGODB_INDEXES: (('field_0', ASCENDING),
        #                   (('field_0', 'field_1'), ASCENDING),
        #                   (('field_0', ASCENDING), ('field_0', DESCENDING))),
        MONGODB_OPTIONS_: '',
        MONGODB_PASSWORD: '',
        MONGODB_PORT: 27017,
        MONGODB_USERNAME: '',
    }

    def setUp(self):
        self.crawler = get_crawler(Spider, self.settings_dict)
        self.spider = self.crawler._create_spider('foo')

    @defer.inlineCallbacks
    def test_process_item(self):
        pipeline = PipelineMongoDBAsync.from_crawler(crawler=self.crawler)
        pipeline.coll = mongomock.MongoClient().db.collection

        item = ItemTest({'field_0': 0, 'field_1': 1})

        result = yield process_item(pipeline, item, self.spider)

        self.assertEqual(result.__dict__, item.__dict__)
