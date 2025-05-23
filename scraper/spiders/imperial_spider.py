import scrapy
from scrapy_selenium import SeleniumRequest
from ..items import ImperialItem

class ImperialSpider(scrapy.Spider):
    name = "imperial"

    def start_requests(self):
        yield SeleniumRequest(
            url="https://profiles.imperial.ac.uk/d.aanensen",
            callback=self.parse_profile
        )

    def parse_profile(self, response):
        item = ImperialItem()
        item['university'] = "Imperial College London"
        item['name'] = response.css("h1::text").get(default='').strip()
        item['title'] = response.css("p.title::text").get(default='').strip()
        item['department'] = response.css("p.department::text").get(default='').strip()
        item['email'] = response.css("a[href^='mailto:']::attr(href)").re_first(r'mailto:(.*)')
        item['research_interests'] = response.css("ul.research-interests li::text").getall()
        item['profile_url'] = response.url
        yield item
