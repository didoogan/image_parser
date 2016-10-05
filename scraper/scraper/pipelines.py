# -*- coding: utf-8 -*-


import redis
import json

from scrapy.exceptions import DropItem


class ScraperPipeline(object):
    def __init__(self):
        self.r = redis.StrictRedis()
        self.result = {'google': [], 'yandex': [], 'instagram': []}

    def process_item(self, item, spider):
        self.result[item['site']].append(item['img'])
        return item

    def close_spider(self, spider):
        self.r.hmset(spider.query, {k: json.dumps(v) for k, v in self.result.iteritems() if v})
        self.r.expire(spider.query, 3600)
        flag = spider.query
        self.r.publish(spider.query, True)
