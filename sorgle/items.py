# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ProfessorItem(scrapy.Item):
    university = scrapy.Field()
    name = scrapy.Field()
    title = scrapy.Field()
    department = scrapy.Field()
    email = scrapy.Field()
    research_interests = scrapy.Field()
    profile_url = scrapy.Field()
