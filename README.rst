=======================
Scrapy-Pipeline-MongoDB
=======================

.. image:: https://img.shields.io/pypi/v/scrapy-pipeline-mongodb.svg
   :target: https://pypi.python.org/pypi/scrapy-pipeline-mongodb
   :alt: PyPI Version

.. image:: https://img.shields.io/travis/grammy-jiang/scrapy-pipeline-mongodb/master.svg
   :target: http://travis-ci.org/grammy-jiang/scrapy-pipeline-mongodb
   :alt: Build Status

.. image:: https://img.shields.io/badge/wheel-yes-brightgreen.svg
   :target: https://pypi.python.org/pypi/scrapy-pipeline-mongodb
   :alt: Wheel Status

.. image:: https://img.shields.io/codecov/c/github/grammy-jiang/scrapy-pipeline-mongodb/master.svg
   :target: http://codecov.io/github/grammy-jiang/scrapy-pipeline-mongodb?branch=master
   :alt: Coverage report

Overview
========

Scrapy is a great framework for web crawling. This package provides two
pipelines to save items into MongoDB in a async or sync way. And also provide a
a highly customized way to interact with MongoDB in a async or sync way.

* Save an item and get Object ID from this pipeline

* Update an item and get Object ID from this pipeline

Requirements
============

* Txmongo, a async MongoDB driver with Twisted

* Not support Python 2.7

* Tests on Python 3.5, but it should work on other version higher then Python
  3.3

* Tests on Linux, but it's a pure python module, it should work on other
  platforms with official python and Twisted supported, e.g. Windows, Mac OSX,
  BSD

Installation
============

The quick way::

    pip install scrapy-pipeline-mongodb

Or put this middleware just beside the scrapy project.

Documentation
=============

Block Inspector in spider middleware, in ``settings.py``, for example::

    from txmongo.filter import ASCENDING
    from txmongo.filter import DESCENDING

    # -----------------------------------------------------------------------------
    # PIPELINE MONGODB ASYNC
    # -----------------------------------------------------------------------------

    ITEM_PIPELINES.update({
        'scrapy_pipeline_mongodb.pipelines.mongodb_async.PipelineMongoDBAsync': 500,
    })

    MONGODB_USERNAME = 'user'
    MONGODB_PASSWORD = 'password'
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    MONGODB_DATABASE = 'test_mongodb_async_db'
    MONGODB_COLLECTION = 'test_mongodb_async_coll'

    # MONGODB_OPTIONS_ = 'MONGODB_OPTIONS_'

    MONGODB_INDEXES = [('field_0', ASCENDING, {'unique': True}),
                       (('field_0', 'field_1'), ASCENDING, {}),
                       (('field_0', ASCENDING, {}), ('field_0', DESCENDING, {}))]

    MONGODB_PROCESS_ITEM = 'scrapy_pipeline_mongodb.utils.process_item.process_item'


Settings Reference
==================

MONGODB_USERNAME
----------------

A string of the username of the database.

MONGODB_PASSWORD
----------------

A string of the password of the database.

MONGODB_HOST
------------

A string of the ip address or the domain of the database.

MONGODB_PORT
------------

A int of the port of the database.

MONGODB_DATABASE
----------------

A string of the name of the database.

MONGODB_COLLECTION
------------------

A list of the indexes to create on the collection.

MONGODB_OPTIONS_*
-----------------

Options can be attached when the pipeline start to connect to MongoBD.

If any options are needed, the name of the option can be with the prefix
`MONGODB_OPTIONS_`, the pipeline will parse it.

For example:

+---------------+-------------------------------+
| option name   | in `settings.py`              |
+---------------+-------------------------------+
| authMechanism | MONGODB_OPTIONS_authMechanism |
+---------------+-------------------------------+


For more options, please refer to the page:

`Connection String URI Format — MongoDB Manual 3.4`_

.. _`Connection String URI Format — MongoDB Manual 3.4`: https://docs.mongodb.com/manual/reference/connection-string/#connections-standard-connection-string-format

MONGODB_INDEXES
---------------

A list of the indexes defined in this setting will be created when the spider is
open.

If the index has already existed, there will be no warning or error raised.

MONGODB_PROCESS_ITEM
--------------------

To highly customize to interact with MongoDB, this pipeline provide a setting to
define the function `process_item`. And with this package, there is one default
function: just call the method `insert_one` of the collection to save the item
into MongoDB, then return the item.

If a customize is provided to replace the default one, please note the behavior
should follow the requirement which is clearly written in the scrapy documents:

`Item Pipeline — Scrapy 1.4.0 documentation`_

.. _`Item Pipeline — Scrapy 1.4.0 documentation`: https://doc.scrapy.org/en/latest/topics/item-pipeline.html#writing-your-own-item-pipelin

Build-in Functions For Processing Item
======================================

scrapy_pipeline_mongodb.utils.process_item.process_item
-------------------------------------------------------

This is a build-in function to call the method `insert_one` of the collection,
and return the item.

To use this function, in `settings.py`::

    MONGODB_PROCESS_ITEM = 'scrapy_pipeline_mongodb.utils.process_item.process_item'

NOTE
====

The drivers may have different api for the same operation, this pipeline adopts
txmongo as the async driver for MongoDB, please read the relative documents to
make sure the customized functions can run fluently in this pipeline.

TODO
====
* Add a unit test for the index created function

* Add a sync pipeline
