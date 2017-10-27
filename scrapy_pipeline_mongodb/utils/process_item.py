"""
this process_item function should follow the input and output requirements
in the scrapy documents:
https://doc.scrapy.org/en/latest/topics/item-pipeline.html#writing-your-own-item-pipeline
"""
from scrapy import Item
from scrapy import Spider
from twisted.internet.defer import inlineCallbacks


@inlineCallbacks
def process_item(pipeline, item: Item, spider: Spider):
    result = yield pipeline.coll.insert_one(item)
    return item
