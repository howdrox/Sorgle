import scrapy

class InsaItem(scrapy.Item):
    university = scrapy.Field()
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    phone = scrapy.Field()
    department = scrapy.Field()
    role = scrapy.Field()

class ImperialItem(scrapy.Item):
    university = scrapy.Field()
    name = scrapy.Field()
    title = scrapy.Field()
    department = scrapy.Field()
    email = scrapy.Field()
    research_interests = scrapy.Field()
    profile_url = scrapy.Field()

class KulItem(scrapy.Item):
    university = scrapy.Field()
    name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    curriculum_link = scrapy.Field()
    unit = scrapy.Field()
    functions = scrapy.Field()
    photo_url = scrapy.Field()