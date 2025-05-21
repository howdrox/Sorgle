# sorgle/spiders/uni_scraper.py

import scrapy
import json
from ..items import ProfessorItem


class UniSpider(scrapy.Spider):
    name = 'uni_spider'
    custom_settings = {
        'DOWNLOAD_DELAY': 1.0,         # politeness
        'ROBOTSTXT_OBEY': True,        # obey robots.txt
        # You can also set a more realistic USER_AGENT here:
        'USER_AGENT': 'Mozilla/5.0 (compatible; UniSpider/1.0; +https://yourdomain.example)'
    }

    async def start(self):
        """
        Replaces the deprecated start_requests().
        Scrapy 2.13+ expects this method to be an async iterable.
        """
        # Load your universities list from unis.json
        with open('unis.json', 'r', encoding='utf-8') as f:
            unis = json.load(f)

        for uni_name, homepage in unis.items():
            # Figure out the correct faculty-directory URL for each university
            dir_url = self.get_directory_url(uni_name, homepage)
            if dir_url:
                yield scrapy.Request(
                    url=dir_url,
                    callback=self.parse_directory,
                    meta={'university': uni_name}
                )
            else:
                self.logger.warning(f"No directory URL mapping found for {uni_name}")

    def get_directory_url(self, uni_name, homepage):
        """
        Maps each university key (from unis.json) to its actual faculty-directory page.
        """
        mapping = {
            # MIT’s public faculty directory is on directory.mit.edu
            "Massachusetts Institute of Technology (MIT)": "https://engineering.mit.edu/new-faculty-2024/",
            # Imperial: redirecting into their “Profiles” service automatically
            "Imperial College London": homepage.rstrip('/') + "/people/search?search_faculty=All&search_school=All",
            # Oxford’s “Find an Expert” lives under /people/find-expert
            "University of Oxford": homepage.rstrip('/') + "/people/find-expert",
        }
        return mapping.get(uni_name)

    def parse_directory(self, response):
        uni = response.meta['university']

        # ------------------------------
        # 1) Massachusetts Institute of Technology
        # ------------------------------
        if uni.startswith("Massachusetts Institute of Technology"):
            # directory.mit.edu lists all people alphabetically in <tbody>
            rows = response.css('table.directory-search-results tbody tr')
            for row in rows:
                rel = row.css('td:nth-child(1) a::attr(href)').get()
                if rel:
                    # Full URL is already absolute on directory.mit.edu; you can follow it directly
                    yield response.follow(
                        rel,
                        callback=self.parse_profile,
                        meta={'university': uni}
                    )

        # ------------------------------
        # 2) Imperial College London
        # ------------------------------
        elif uni.startswith("Imperial College London"):
            # Imperial’s “Profiles” service loads via HTML first; each person in <a class="person-result">
            links = response.css('a.person-result::attr(href)').getall()
            for rel in links:
                yield response.follow(
                    rel,
                    callback=self.parse_profile,
                    meta={'university': uni}
                )

        # ------------------------------
        # 3) University of Oxford
        # ------------------------------
        elif uni.startswith("University of Oxford"):
            # Oxford’s “Find an Expert” page: search results in <div class="result">, each <a class="expert-name">
            prof_links = response.css('div.result a.expert-name::attr(href)').getall()
            for rel in prof_links:
                yield response.follow(
                    rel,
                    callback=self.parse_profile,
                    meta={'university': uni}
                )

        else:
            self.logger.warning(f"No parse_directory logic for {uni}")

    def parse_profile(self, response):
        uni = response.meta['university']
        item = ProfessorItem()
        item['university'] = uni
        item['profile_url'] = response.url

        # ------------------------------
        # 1) Massachusetts Institute of Technology
        # ------------------------------
        if uni.startswith("Massachusetts Institute of Technology"):
            # On directory.mit.edu profile pages:
            #   • Name is in <h1> with .page-title
            #   • Title/Role in <div class="field--name-field-sb-person-title">
            #   • Department in <div class="field--name-field-sb-person-department">
            #   • Email is usually obfuscated—look for mailto:
            item['name'] = response.css('h1.page-title::text').get(default='').strip()
            item['title'] = response.css('div.field--name-field-sb-person-title span::text').get(default='').strip()
            item['department'] = response.css('div.field--name-field-sb-person-department span::text').get(default='').strip()
            item['email'] = response.css('a[href^="mailto:"]::text').get(default='').strip()
            # Research interests on MIT profiles often appear in <div class="field--name-field-sb-person-interests">
            interests = response.css('div.field--name-field-sb-person-interests li::text').getall()
            item['research_interests'] = [s.strip() for s in interests if s.strip()]

        # ------------------------------
        # 2) Imperial College London
        # ------------------------------
        elif uni.startswith("Imperial College London"):
            # Imperial “Profiles” pages use:
            #   • <h1 class="profile-name"> for name
            #   • <p class="profile-position"> for title
            #   • <p class="profile-department"> for department
            #   • <a href="mailto:…"> for email
            #   • Research interests in <div class="person-research-interests">
            item['name'] = response.css('h1.profile-name::text').get(default='').strip()
            item['title'] = response.css('p.profile-position::text').get(default='').strip()
            item['department'] = response.css('p.profile-department::text').get(default='').strip()
            item['email'] = response.css('a[href^="mailto:"]::text').get(default='').strip()
            interests = response.css('div.person-research-interests li::text').getall()
            item['research_interests'] = [s.strip() for s in interests if s.strip()]

        # ------------------------------
        # 3) University of Oxford
        # ------------------------------
        elif uni.startswith("University of Oxford"):
            # Oxford “Find an Expert” profile pages:
            #   • <h1 class="expert-name"> for name
            #   • <div class="expert-title"> for title
            #   • <div class="expert-department"> for department
            #   • <a href="mailto:…"> for email
            #   • Research interests in <div class="expert-research-interests">
            item['name'] = response.css('h1.expert-name::text').get(default='').strip()
            item['title'] = response.css('div.expert-title::text').get(default='').strip()
            item['department'] = response.css('div.expert-department::text').get(default='').strip()
            item['email'] = response.css('a[href^="mailto:"]::text').get(default='').strip()
            interests = response.css('div.expert-research-interests ul li::text').getall()
            item['research_interests'] = [s.strip() for s in interests if s.strip()]

        else:
            # Fallback: at least try to grab <h1> as name
            item['name'] = response.css('h1::text').get(default='').strip()
            item['title'] = ''
            item['department'] = ''
            item['email'] = ''
            item['research_interests'] = []

        yield item
