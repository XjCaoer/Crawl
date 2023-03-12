# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    author = scrapy.Field()
    name = scrapy.Field()
    sex = scrapy.Field()
    addr = scrapy.Field()
    email = scrapy.Field()
    description = scrapy.Field()

class MeishiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    src = scrapy.Field()