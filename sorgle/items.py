# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ProfessorItem(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    # email = scrapy.Field()
    # office = scrapy.Field()
    # bio = scrapy.Field()
