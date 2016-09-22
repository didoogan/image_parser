# -*- coding: utf-8 -*-
import scrapy
import json

from itertools import islice

# from itertools import islice

from scraper.items import AppItem


class ImageSpider(scrapy.Spider):

    name = "image"
    results = 10
    google_url_pattern = "https://www.google.com.ua/search?q={}&biw=5&bih=5&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjy-OyRwKLPAhXJCpoKHVZDDJkQ_AUIBigB"
    yandex_url_pattern = 'https://yandex.ua/images/search?text={}&parent-reqid=1474550983897237-741190681254071648529266-sas1-1783'

    # start_urls = [
    #     # self.google_url.format(question),
    #     'https://www.google.com.ua/search?q=animal&biw=5&bih=5&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjy-OyRwKLPAhXJCpoKHVZDDJkQ_AUIBigB',
    # ]

    # def __init__(self, question=u'сиськи'.encode('utf-8'), google=True, yandex=False, instagram=False):
    #     super(ImageSpider, self).__init__()
    #     if google:
    #         self.start_urls.append(self.google_url.format(question))
    #     if yandex:
    #         self.start_urls.append(self.yandex_url.format(question))

    def __init__(self, question=u'сиськи'.encode('utf-8'), google=True, yandex=True, instagram=False):
        super(ImageSpider, self).__init__()
        if google:
            self.google_url = self.google_url_pattern.format(question)
        if yandex:
            self.yandex_url = self.yandex_url_pattern.format(question)

    def start_requests(self):
        if self.google_url:
            yield scrapy.Request(self.google_url, callback=self.google_parser)
        if self.yandex_url:
            yield scrapy.Request(self.yandex_url, callback=self.yandex_parser)

    def google_parser(self, response):
            # questions = response.xpath('//div[@class="question-summary"]')
            google_images = response.xpath('//div[@id="ires"]//img')
            for image in islice(google_images, self.results):
                item = AppItem()
                item['google_img'] = image.xpath('@src').extract_first()
                yield item

    def yandex_parser(self, response):
                # yandex_images = response.xpath('//a[@class="serp-item__link"]')
                yandex_images = response.xpath('//*[contains(@class, "serp-item_group_search")]').xpath('./@data-bem').extract()
                for image in islice(yandex_images, self.results):
                    item = AppItem()
                    image = json.loads(image)
                    image = image['serp-item']['preview'][0]['url']
                    item['yandex_img'] = image
                    yield item












