# -*- coding: utf-8 -*-
import scrapy
import json
import time
import redis

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


from itertools import islice

# from itertools import islice

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

    def __init__(self, question='dog', google=False, yandex=False, instagram=False, **kwargs):

        # for detecting the end of spiders work
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        if google:
            self.google_url = self.google_url_pattern.format(question)
        if yandex:
            self.yandex_url = self.yandex_url_pattern.format(question)
        if instagram:
            self.instagram_url = self.instagram_url_pattern.format(question)
        self.query = question
        self.r = redis.StrictRedis()
        self.r.set('flag', False)


    def start_requests(self):
        if self.google_url:
            yield scrapy.Request(self.google_url, callback=self.google_parser)
        if self.yandex_url:
            yield scrapy.Request(self.yandex_url, callback=self.yandex_parser)
        if self.instagram_url:
            yield scrapy.Request(self.instagram_url, callback=self.instagram_parser)

    def google_parser(self, response):
            # questions = response.xpath('//div[@class="question-summary"]')
            google_images = response.xpath('//div[@id="ires"]//img')
            for image in islice(google_images, self.results):
                item = AppItem()
                item['google_img'] = image.xpath('@src').extract_first()
                yield item

    def yandex_parser(self, response):
        yandex_images = response.xpath('//*[contains(@class, "serp-item_group_search")]').xpath('./@data-bem').extract_first()
        for image in islice(yandex_images, self.results):
            time.sleep(1)
            item = AppItem()
            image = json.loads(image)
            image = image['serp-item']['preview'][0]['url']
            item['yandex_img'] = image
            yield item

    def instagram_parser(self, response):
        xpath = response.xpath('//p/text()')
        dict = json.loads(xpath.extract_first())
        data = dict['tag']['media']['nodes']
        for url in islice(data, self.results):
            item = AppItem()
            item['instagram_img'] = url['thumbnail_src']
            yield item

    def spider_closed(self, spider):
        if spider is not self:
            return
        # name = '{}_signal'.format(self.query)
        self.r.set('flag', True)
        self.r.expire(name, 3600)

    def parse(self, response):
        pass
















