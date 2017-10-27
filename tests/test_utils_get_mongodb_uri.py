from collections import OrderedDict
from unittest import TestCase
from urllib.parse import urlparse

from scrapy import Spider
from scrapy.utils.test import get_crawler

from scrapy_pipeline_mongodb.settings.default_settings import MONGODB_COLLECTION
from scrapy_pipeline_mongodb.settings.default_settings import MONGODB_DATABASE
from scrapy_pipeline_mongodb.settings.default_settings import MONGODB_HOST
from scrapy_pipeline_mongodb.settings.default_settings import MONGODB_PASSWORD
from scrapy_pipeline_mongodb.settings.default_settings import MONGODB_PORT
from scrapy_pipeline_mongodb.settings.default_settings import MONGODB_USERNAME
from scrapy_pipeline_mongodb.utils.get_mongodb_uri import get_mongodb_uri

MONGODB_OPTIONS_authMechanism = 'MONGODB_OPTIONS_authMechanism'
MONGODB_OPTIONS_maxPoolSize = 'MONGODB_OPTIONS_maxPoolSize'


class GetMongoDBURITest(TestCase):
    settings_dict = {
        MONGODB_COLLECTION: 'test_mongodb_async',
        MONGODB_DATABASE: 'test_mongodb_async',
        MONGODB_HOST: 'localhost',
        # MONGODB_INDEXES: (('field_0', ASCENDING),
        #                   (('field_0', 'field_1'), ASCENDING),
        #                   (('field_0', ASCENDING), ('field_0', DESCENDING))),
        MONGODB_OPTIONS_authMechanism: 'SCRAM-SHA-1',
        MONGODB_OPTIONS_maxPoolSize: 100,
        MONGODB_PASSWORD: 'password',
        MONGODB_PORT: 27017,
        MONGODB_USERNAME: 'username',
    }

    def setUp(self):
        self.crawler = get_crawler(Spider, self.settings_dict)
        self.settings = self.crawler.settings

    def test_get_mongodb_uri(self):
        uri = urlparse(get_mongodb_uri(self.settings))

        self.assertDictEqual(
            uri._replace(query=dict(map(lambda x: x.split('='),
                                        uri.query.split('&'))))._asdict(),
            OrderedDict([
                ('scheme', 'mongodb'),
                ('netloc', '{username}:{password}@{host}:{port}'.format(
                    username=self.settings_dict[MONGODB_USERNAME],
                    password=self.settings_dict[MONGODB_PASSWORD],
                    host=self.settings_dict[MONGODB_HOST],
                    port=self.settings_dict[MONGODB_PORT])),
                ('path', '/{database}'.format(
                    database=self.settings_dict[MONGODB_DATABASE])),
                ('params', ''),
                ('query',
                 {'maxpoolsize': str(
                     self.settings_dict[MONGODB_OPTIONS_maxPoolSize]),
                     'authmechanism': self.settings_dict[
                         MONGODB_OPTIONS_authMechanism]}),
                ('fragment', '')])
        )
