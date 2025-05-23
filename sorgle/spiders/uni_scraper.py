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
        profs = ["polin", "rijmen", "vander"]  # later: loop a–z, or whatever
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        letters = letters + profs
        urls = []
        for letter in letters:
            new = scrape_lname_links(
                url="https://www.kuleuven.be/wieiswie/en/person/search",
                query=letter,
                search_selector=(By.ID, "personinput"),
                lname_links_selector=(By.CSS_SELECTOR, "a.lname"),
                headless=True
            )
            urls.extend(new)
            # profile_url = "https://www.kuleuven.be/wieiswie/en/person/00005695"  #These are for single url testing
            # yield scrapy.Request(profile_url, callback=self.parse_profile)       #For single url testing
        print("EVERYTHING LOADED: ", len(urls))
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
            'university': "KU Leuven",
            'name': " ".join(name.split()),
            'title': title.strip(),
            'url': response.url,
            'curriculum_link': curriculum_link.strip() if curriculum_link else 'None',
            'unit': unit,
            'functions': functions,
            'photo_url': photo_url.strip() if photo_url else 'None'
        }
