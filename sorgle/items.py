# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ProfessorItem(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    curriculum_link = scrapy.Field()
    unit = scrapy.Field()
    functions = scrapy.Field()
    photo_url = scrapy.Field()

    # email = scrapy.Field()
    # office = scrapy.Field()
    # bio = scrapy.Field()
