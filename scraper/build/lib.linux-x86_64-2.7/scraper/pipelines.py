# -*- coding: utf-8 -*-


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
        self.result[item['site']].append(item['img'])
        return item

    def close_spider(self, spider):
        self.r.hmset(spider.query, {k: json.dumps(v) for k, v in self.result.iteritems() if v})
        self.r.expire(spider.query, 3600)
        # old_result = self.r.hgetall(spider.query)
        # for k,v in self.result.iteritems():
        #     data = old_result.get(k, False)
        #     if data:
        #         self.result[k] = old_result[k]
        # self.r.hmset(spider.query, {k: json.dumps(v) for k, v in self.result.iteritems() if v})


        self.r.publish('flag', True)
        # item = dict(item)
        # self.result[item['site']].append(item['src'])
        # src = item.get('google_img', False)
        # if src:
        #     # self.google['google'].append(src)
        #     self.result['google'].append(src)
        #     # self.r.publish(spider.query, json.dumps(self.result))
        #     self.r.hmset(spider.query,
        #                  {'google': json.dumps(self.result['google']), 'yandex': json.dumps(self.result['yandex']),
        #                   'instagram': json.dumps(self.result['instagram'])})
        #     self.r.expire(spider.query, 3600)
        #     return item
        #
        # src = item.get('yandex_img', False)
        # if src:
        #     self.result['yandex'].append(src)
        #     # self.r.publish(spider.query, json.dumps(self.result))
        #     self.r.hmset(spider.query,
        #                  {'google': json.dumps(self.result['google']), 'yandex': json.dumps(self.result['yandex']),
        #                   'instagram': json.dumps(self.result['instagram'])})
        #     self.r.expire(spider.query, 3600)
        #     return item
        #
        # src = item.get('instagram_img', False)
        # if src:
        #     self.result['instagram'].append(src)
        #     # self.r.publish(spider.query, json.dumps(self.result))
        #     self.r.hmset(spider.query,
        #                  {'google': json.dumps(self.result['google']), 'yandex': json.dumps(self.result['yandex']),
        #                   'instagram': json.dumps(self.result['instagram'])})
        #     self.r.expire(spider.query, 3600)
        #     return item

        # self.r.publish('chanel', json.dumps(dict(item)))
        # # self.r.publish('chanel', item)
        # print 'fuck'

