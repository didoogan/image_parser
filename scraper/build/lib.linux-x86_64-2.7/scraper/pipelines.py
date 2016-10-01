# -*- coding: utf-8 -*-

from pip.operations import freeze
x = freeze.freeze()
print '\n' * 10
for p in x:
    print p
print '\n' * 10

import redis
import json

from scrapy.exceptions import DropItem


class ScraperPipeline(object):
    def __init__(self):
        self.r = redis.StrictRedis()
        # self.google = {'google': []}
        # self.yandex = {'yandex': []}
        # self.instagram = {'instagram': []}
        self.result = {'google': [], 'yandex': [], 'instagram': []}

    def process_item(self, item, spider):
        item = dict(item)
        src = item.get('google_img', False)
        if src:
            # self.google['google'].append(src)
            self.result['google'].append(src)
            # self.r.publish(spider.query, json.dumps(self.result))
            self.r.hmset(spider.query,
                         {'google': json.dumps(self.result['google']), 'yandex': json.dumps(self.result['yandex']),
                          'instagram': json.dumps(self.result['instagram'])})
            return item

        src = item.get('yandex_img', False)
        if src:
            self.result['yandex'].append(src)
            # self.r.publish(spider.query, json.dumps(self.result))
            self.r.hmset(spider.query,
                         {'google': json.dumps(self.result['google']), 'yandex': json.dumps(self.result['yandex']),
                          'instagram': json.dumps(self.result['instagram'])})
            return item

        src = item.get('instagram_img', False)
        if src:
            self.result['instagram'].append(src)
            # self.r.publish(spider.query, json.dumps(self.result))
            self.r.hmset(spider.query,
                         {'google': json.dumps(self.result['google']), 'yandex': json.dumps(self.result['yandex']),
                          'instagram': json.dumps(self.result['instagram'])})
            return item

        # self.r.publish('chanel', json.dumps(dict(item)))
        # # self.r.publish('chanel', item)
        # print 'fuck'

