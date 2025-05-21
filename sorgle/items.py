import scrapy

class ProfessorItem(scrapy.Item):
    university = scrapy.Field()
    name = scrapy.Field()
    title = scrapy.Field()
    department = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    research_interests = scrapy.Field()
    profile_url = scrapy.Field()
