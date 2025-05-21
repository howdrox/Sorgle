import scrapy
from sorgle.items import ProfessorItem

class ProfessorSpider(scrapy.Spider):
    name = 'professor'
    start_urls = [
        'https://www.kuleuven.be/wieiswie/en/person/00005695'  # Replace with actual URL
    ]

    def parse(self, response):
        item = ProfessorItem()
        
        # Example selectors - adjust based on actual page structure
        item['name'] = response.css('h1.name::text').get()
        item['title'] = response.css('div.title::text').get()
        item['email'] = response.xpath('//a[contains(@href, "mailto:")]/text()').get()
        item['office'] = response.css('div.office::text').get()
        item['bio'] = ' '.join(response.css('div.bio ::text').getall())
        
        yield item