# -*- coding: utf-8 -*-
import scrapy

from itertools import islice

# from itertools import islice

from scraper.items import AppItem


class ImageSpider(scrapy.Spider):

    name = "image"
    results = 10
    google_url = "https://www.google.com.ua/search?q={}&biw=5&bih=5&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjy-OyRwKLPAhXJCpoKHVZDDJkQ_AUIBigB"

    # start_urls = [
    #     # self.google_url.format(question),
    #     'https://www.google.com.ua/search?q=animal&biw=5&bih=5&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjy-OyRwKLPAhXJCpoKHVZDDJkQ_AUIBigB',
    # ]

    def __init__(self, question=u'сиськи'.encode('utf-8'), google=True, yandex=False, instagram=False):
        super(ImageSpider, self).__init__()
        # self.question = question
        if google:
            self.start_urls.append(self.google_url.format(question))

    def parse(self, response):
        # questions = response.xpath('//div[@class="question-summary"]')
        images = response.xpath('//div[@id="ires"]//img')
        for image in islice(images, self.results):
            item = AppItem()
            item['google_img'] = images.xpath('@src').extract_first()
            yield item











