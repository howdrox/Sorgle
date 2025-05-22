# sorgle/spiders/uni_scraper.py

import scrapy
import json
from sorgle.items import ProfessorItem
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_lname_links(url, query,
                      search_selector=(By.CSS_SELECTOR, "input.search-input"),
                      lname_links_selector=(By.CSS_SELECTOR, "a.lname"),
                      driver_path=None,
                      headless=False):
    """
    Navigate to `url`, input `query` into the search field,
    wait for all <a class="lname"> elements to appear,
    and return their hrefs.

    Args:
        url (str): The website URL.
        query (str): Search term to input.
        search_selector (tuple): Locator for the search input.
        lname_links_selector (tuple): Locator for <a class="lname"> links.
        driver_path (str, optional): Path to the WebDriver executable.
        headless (bool): Whether to run browser headlessly.

    Returns:
        List[str]: HREF attributes of all <a class="lname"> links.
    """
    # Configure Chrome options
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')

    # Launch browser
    driver = webdriver.Chrome(executable_path=driver_path, options=options) if driver_path else webdriver.Chrome(options=options)
    driver.get(url)

    try:
        # Find and fill search input
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(search_selector)
        )
        search_input.clear()
        search_input.send_keys(query)
        search_input.send_keys(Keys.ENTER)

        # Wait for the lname links to load
        lname_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(lname_links_selector)
        )

        # Extract hrefs only from <a class="lname">
        urls = [el.get_attribute('href') for el in lname_elements]
        return urls

    finally:
        driver.quit()


class ProfessorSpider(scrapy.Spider):
    
    name = "professor"
    allowed_domains = ["kuleuven.be"]
    def start_requests(self):
        # get the links for “a” once, up front
        letters = ["polin"]  # later: loop a–z, or whatever
        for letter in letters:
            urls = scrape_lname_links(
                url="https://www.kuleuven.be/wieiswie/en/person/search",
                query="polin",
                search_selector=(By.ID, "personinput"),
                lname_links_selector=(By.CSS_SELECTOR, "a.lname"),
                headless=True
            )
            # profile_url = "https://www.kuleuven.be/wieiswie/en/person/00005695"  #These are for single url testing
            # yield scrapy.Request(profile_url, callback=self.parse_profile)       #For single url testing
            for profile_url in urls:
                yield scrapy.Request(profile_url, callback=self.parse_profile)
    
    

    def parse_profile(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        name_tag = soup.select_one('div.Person-box h2')
        name = name_tag.get_text(strip=True) if name_tag else None
        title_tag = soup.select_one('div.address p')
        title = title_tag.get_text(strip=True) if title_tag else None
        curriculum_div = soup.select_one('#about_me a[href*="orcid.org"]')
        curriculum_link = curriculum_div['href'] if curriculum_div else None
        unit = []
        for li in soup.select('div.unit ul.list-styled li'):
        # get_text joins all text inside li (including <a>)
            full_text = li.get_text(" ", strip=True)
            if full_text:
                unit.append(full_text)
        functions = []
        for li in soup.select('div.functions ul.list-styled li'):
        # get_text joins all text inside li (including <a>)
            full_text = li.get_text(" ", strip=True)
            if full_text:
                functions.append(full_text)
        photo_tag = soup.select_one('img.photo.image-left')
        photo_src = photo_tag['src'] if photo_tag else None
        photo_url = response.urljoin(photo_src) if photo_src else None
       



        yield {
            'name': name.strip(),
            'title': title.strip(),
            'url': response.url,
            'curriculum_link': curriculum_link.strip() if curriculum_link else 'None',
            'unit': unit,
            'functions': functions,
            'photo_url': photo_url.strip() if photo_url else 'None'
        }
# class ProfessorSpider(scrapy.Spider):
#     name = 'professor'
#     start_urls = [
#         'https://www.kuleuven.be/wieiswie/en/person/00005695'  # Replace with actual URL
#     ]

#     def parse(self, response):
#         response = response.replace(encoding='utf-8')
#         print("RESPONSE ENCODING:", repr(response.encoding))
#         print("CONTENT-TYPE HEADER:", response.headers.get('Content-Type'))

#         item = ProfessorItem()
        
#         # Example selectors - adjust based on actual page structure
#         item['name'] = response.css('div.Person-box h2::text').get()
#         # item['title'] = response.css('div.address p b::text').get()
#         # item['email'] = response.xpath('//a[contains(@href, "mailto:")]/text()').get()
#         # item['office'] = response.css('div.office::text').get()
#         # item['bio'] = ' '.join(response.css('div.bio ::text').getall())
        
#         yield item
# class UniSpider(scrapy.Spider):
#     name = 'uni_spider'
#     custom_settings = {
#         'DOWNLOAD_DELAY': 1.0,         # politeness
#         'ROBOTSTXT_OBEY': True,        # obey robots.txt
#         # You can also set a more realistic USER_AGENT here:
#         'USER_AGENT': 'Mozilla/5.0 (compatible; UniSpider/1.0; +https://yourdomain.example)'
#     }

#     async def start(self):
#         """
#         Replaces the deprecated start_requests().
#         Scrapy 2.13+ expects this method to be an async iterable.
#         """
#         # Load your universities list from unis.json
#         with open('unis.json', 'r', encoding='utf-8') as f:
#             unis = json.load(f)

#         for uni_name, dir_url in unis.items():
#             if dir_url:
#                 yield scrapy.Request(
#                     url=dir_url,
#                     callback=self.parse_directory,
#                     meta={'university': uni_name}
#                 )
#             else:
#                 self.logger.warning(f"No directory URL mapping found for {uni_name}")

#     def parse_directory(self, response):
#         uni = response.meta['university']

#         # # ------------------------------
#         # # 1) Massachusetts Institute of Technology
#         # # ------------------------------
#         # if uni.startswith("Massachusetts Institute of Technology"):
#         #     # directory.mit.edu lists all people alphabetically in <tbody>
#         #     rows = response.css('table.directory-search-results tbody tr')
#         #     for row in rows:
#         #         rel = row.css('td:nth-child(1) a::attr(href)').get()
#         #         if rel:
#         #             # Full URL is already absolute on directory.mit.edu; you can follow it directly
#         #             yield response.follow(
#         #                 rel,
#         #                 callback=self.parse_profile,
#         #                 meta={'university': uni}
#         #             )

#         # ------------------------------
#         # 2) Imperial College London
#         # ------------------------------
#         if uni.startswith("Imperial College London"):
#             # Imperial’s “Profiles” service loads via HTML first; each person in <a class="person-result">
#             links = response.css('a[href*="profiles.imperial.ac.uk"]::attr(href)').getall()
#             for link in links:
#                 yield response.follow(
#                     link,
#                     callback=self.parse_profile,
#                     meta={'university': uni}
#                 )

#         # ------------------------------
#         # 3) University of Oxford
#         # ------------------------------
#         elif uni.startswith("University of Oxford"):
#             # Oxford’s “Find an Expert” page: search results in <div class="result">, each <a class="expert-name">
#             prof_links = response.css('div.result a.expert-name::attr(href)').getall()
#             for link in prof_links:
#                 yield response.follow(
#                     link,
#                     callback=self.parse_profile,
#                     meta={'university': uni}
#                 )

#         else:
#             self.logger.warning(f"No parse_directory logic for {uni}")

#     def parse_profile(self, response):
#         uni = response.meta['university']
#         item = ProfessorItem()
#         item['university'] = uni
#         item['profile_url'] = response.url

#         # ------------------------------
#         # 1) Massachusetts Institute of Technology
#         # ------------------------------
#         if uni.startswith("Massachusetts Institute of Technology"):
#             # On directory.mit.edu profile pages:
#             #   • Name is in <h1> with .page-title
#             #   • Title/Role in <div class="field--name-field-sb-person-title">
#             #   • Department in <div class="field--name-field-sb-person-department">
#             #   • Email is usually obfuscated—look for mailto:
#             item['name'] = response.css('h1.page-title::text').get(default='').strip()
#             item['title'] = response.css('div.field--name-field-sb-person-title span::text').get(default='').strip()
#             item['department'] = response.css('div.field--name-field-sb-person-department span::text').get(default='').strip()
#             item['email'] = response.css('a[href^="mailto:"]::text').get(default='').strip()
#             # Research interests on MIT profiles often appear in <div class="field--name-field-sb-person-interests">
#             interests = response.css('div.field--name-field-sb-person-interests li::text').getall()
#             item['research_interests'] = [s.strip() for s in interests if s.strip()]

#         # ------------------------------
#         # 2) Imperial College London
#         # ------------------------------
#         elif uni.startswith("Imperial College London"):
#             item['name'] = response.css('h1.hero__header___xfv2U::text').get(default='').strip()
#             item['title'] = response.css('p.hero__title___qQUiv::text').get(default='').strip()
#             item['department'] = response.css('p.userHero__department___KwMvK::text').get(default='').strip()
#             item['email'] = response.css('a[href^="mailto:"]::text').get(default='').strip()
#             interests = response.css('div.person-research-interests li::text').getall()
#             item['research_interests'] = [s.strip() for s in interests if s.strip()]

#         # ------------------------------
#         # 3) University of Oxford
#         # ------------------------------
#         elif uni.startswith("University of Oxford"):
#             # Oxford “Find an Expert” profile pages:
#             #   • <h1 class="expert-name"> for name
#             #   • <div class="expert-title"> for title
#             #   • <div class="expert-department"> for department
#             #   • <a href="mailto:…"> for email
#             #   • Research interests in <div class="expert-research-interests">
#             item['name'] = response.css('h1.expert-name::text').get(default='').strip()
#             item['title'] = response.css('div.expert-title::text').get(default='').strip()
#             item['department'] = response.css('div.expert-department::text').get(default='').strip()
#             item['email'] = response.css('a[href^="mailto:"]::text').get(default='').strip()
#             interests = response.css('div.expert-research-interests ul li::text').getall()
#             item['research_interests'] = [s.strip() for s in interests if s.strip()]

#         else:
#             # Fallback: at least try to grab <h1> as name
#             item['name'] = response.css('h1::text').get(default='').strip()
#             item['title'] = ''
#             item['department'] = ''
#             item['email'] = ''
#             item['research_interests'] = []

#         yield item
