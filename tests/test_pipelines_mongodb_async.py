import pprint

import mongomock
from pymongo.results import UpdateResult, InsertOneResult
from scrapy import Field
from scrapy import Item
from scrapy import Spider
from scrapy.utils.test import get_crawler
from twisted.internet import defer
from twisted.trial.unittest import TestCase
from txmongo.filter import ASCENDING
from txmongo.filter import DESCENDING

from scrapy_pipeline_mongodb.pipelines.mongodb_async import PipelineMongoDBAsync
from scrapy_pipeline_mongodb.settings.default_settings import MONGODB_COLLECTION
from scrapy_pipeline_mongodb.settings.default_settings import MONGODB_DATABASE
from scrapy_pipeline_mongodb.settings.default_settings import MONGODB_HOST
from scrapy_pipeline_mongodb.settings.default_settings import MONGODB_INDEXES
from scrapy_pipeline_mongodb.settings.default_settings import MONGODB_OPTIONS_
from scrapy_pipeline_mongodb.settings.default_settings import MONGODB_PASSWORD
from scrapy_pipeline_mongodb.settings.default_settings import MONGODB_PORT
from scrapy_pipeline_mongodb.settings.default_settings import MONGODB_USERNAME

pp = pprint.PrettyPrinter(indent=4)


class ItemTest(Item):
    _id = Field()
    field_0 = Field()
    field_1 = Field()


class TestMongoDBAsync(TestCase):
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

    # TODO: ADD UNIT TEST FOR THIS FUNCTION
    # the api of create_index in txmongo is different with the one in mongomock
    # @defer.inlineCallbacks
    # def test_create_index(self):
    #     pipeline = PipelineMongoDBAsync.from_crawler(crawler=self.crawler)
    #     pipeline._coll = mongomock.MongoClient().db.collection
    #
    #     pp.pprint(dir(pipeline._coll))
    #     result = yield pipeline.create_index(self.spider)
    #     pp.pprint(pipeline._coll.index_information())
    #     self.assertSequenceEqual(self.coll.index_information(),
    #                              pipeline.settings.get(MONGODB_INDEXES))

    @defer.inlineCallbacks
    def test_process_item(self):
        pipeline = PipelineMongoDBAsync.from_crawler(crawler=self.crawler)
        pipeline.coll = mongomock.MongoClient().db.collection

        item = ItemTest({'field_0': 0, 'field_1': 1})

        result = yield pipeline.process_item(item, self.spider)

    @defer.inlineCallbacks
    def test_process_item_insert_one(self):
        pipeline = PipelineMongoDBAsync.from_crawler(crawler=self.crawler)
        pipeline.coll = mongomock.MongoClient().db.collection

        item = ItemTest({'field_0': 0, 'field_1': 1})
        result = yield pipeline.process_item_insert_one(item, self.spider)

        self.assertIsInstance(result, InsertOneResult)

        self.assertDictEqual(
            dict(item),
            dict(pipeline.coll.find_one({'_id': result.inserted_id})))

    @defer.inlineCallbacks
    def test_process_item_update_one(self):
        pipeline = PipelineMongoDBAsync.from_crawler(crawler=self.crawler)
        pipeline.coll = mongomock.MongoClient().db.collection

        item = ItemTest({'field_0': 0, 'field_1': 1})

        result = yield pipeline.process_item_update_one(
            filter_={'field_0': 0},
            update={'$set': item},
            upsert=True,
            spider=self.spider)

        self.assertIsInstance(result, UpdateResult)

        item.update({'_id': result.upserted_id})
        self.assertDictEqual(
            dict(item),
            dict(pipeline.coll.find_one({'_id': result.upserted_id})))
