# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GbtItem(scrapy.Item):
    # define the fields for your item here like:
    game_time = scrapy.Field()
    game_name = scrapy.Field()
    game_BT_URL = scrapy.Field()
