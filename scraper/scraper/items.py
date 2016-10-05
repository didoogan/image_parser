# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppItem(scrapy.Item):
    query = scrapy.Field()
    site = scrapy.Field()
    img = scrapy.Field()
    # google_img = scrapy.Field()
    # yandex_img = scrapy.Field()
    # instagram_img = scrapy.Field()

