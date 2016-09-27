# -*- coding: utf-8 -*-

import redis
import json

from scrapy.exceptions import DropItem


class ScraperPipeline(object):
    def __init__(self):
        self.redis = redis.StrictRedis()

    def process_item(self, item, spider):
        # self.redis.lpush('items', item)
        # raise DropItem("{} has been saved".format(item))
        key = spider.query
        self.redis.sadd(key, json.dumps(dict(item)))
        return item
