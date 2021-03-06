# -*- coding: utf-8 -*-
import scrapy
import json
import time
import redis

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


from itertools import islice

from itertools import islice

from scraper.items import AppItem


class ImageSpider(scrapy.Spider):

    name = "image"
    results = 10
    google_url_pattern = 'https://www.google.com.ua/search?q={}&biw=5&bih=5&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjy-OyRwKLPAhXJCpoKHVZDDJkQ_AUIBigB'
    yandex_url_pattern = 'https://yandex.ua/images/search?text={}&parent-reqid=1474550983897237-741190681254071648529266-sas1-1783'
    instagram_url_pattern = 'https://www.instagram.com/explore/tags/{}/?__a=1'
    google_url = False
    yandex_url = False
    instagram_url = False

    @classmethod
    def str_to_bool(cls, s):
        if s == 'True':
            return True
        return False

    def __init__(self, question='dog', google=True, yandex=False, instagram=False, **kwargs):
        super(ImageSpider, self).__init__(**kwargs)
        if ImageSpider.str_to_bool(google):
            self.google_url = self.google_url_pattern.format(question)
        if ImageSpider.str_to_bool(yandex):
            self.yandex_url = self.yandex_url_pattern.format(question)
        if ImageSpider.str_to_bool(instagram):
            self.instagram_url = self.instagram_url_pattern.format(question)
        self.query = question
        self.r = redis.StrictRedis()
        # self.r.set('flag', False)

    def start_requests(self):
        if self.google_url:
            yield scrapy.Request(self.google_url, callback=self.google_parser)
        if self.yandex_url:
            yield scrapy.Request(self.yandex_url, callback=self.yandex_parser)
        if self.instagram_url:
            yield scrapy.Request(self.instagram_url, callback=self.instagram_parser)

    def google_parser(self, response):
            google_images = response.xpath('//div[@id="ires"]//img')
            for image in islice(google_images, self.results):
                item = AppItem()
                item['img'] = image.xpath('@src').extract_first()
                item['site'] = 'google'
                yield item

    def yandex_parser(self, response):
        yandex_images = response.xpath('//*[contains(@class, "serp-item_group_search")]').xpath('./@data-bem').extract()
        for image in islice(yandex_images, self.results):
            item = AppItem()
            image = json.loads(image)
            image = image['serp-item']['preview'][0]['url']
            item['img'] = image
            item['site'] = 'yandex'
            yield item

    def instagram_parser(self, response):
        xpath = response.xpath('//p/text()')
        dict = json.loads(xpath.extract_first())
        data = dict['tag']['media']['nodes']
        for url in islice(data, self.results):
            item = AppItem()
            item['img'] = url['thumbnail_src']
            item['site'] = 'instagram'
            yield item

    def parse(self, response):
        pass
















