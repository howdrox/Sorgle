import scrapy


class ImperialSpider(scrapy.Spider):
    name = "imperial_spider"
    allowed_domains = ["imperial.ac.uk"]
    start_urls = [
        "https://www.imperial.ac.uk/business-school/faculty-research/faculty/people/"
    ]

    def parse(self, response):
        # Extract profile links
        profile_links = response.css(
            "a[href*='profiles.imperial.ac.uk/']::attr(href)"
        ).getall()
        for link in profile_links:
            yield response.follow(link, callback=self.parse_profile)

    def parse_profile(self, response):
        # Extract name
        name = response.css("h1.hero__header___xfv2U::text").get()
        # Extract title
        title = response.css("p.hero__title___qQUiv::text").get()
        # Extract position
        position = response.css("p.userHero__position___Zi__A::text").get()
        # Extract department
        department = response.css("p.userHero__department___KwMvK::text").get()
        # Extract fields of research
        fields = response.css(
            "div.whiteBox__body___nZQwU ul[aria-label='Fields of Research'] li span::text"
        ).getall()

        yield {
            "name": name.strip() if name else None,
            "title": title.strip() if title else None,
            "position": position.strip() if position else None,
            "department": department.strip() if department else None,
            "fields_of_research": [field.strip() for field in fields if field.strip()],
            "profile_url": response.url,
        }
