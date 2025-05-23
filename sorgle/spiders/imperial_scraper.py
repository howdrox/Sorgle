# sorgle/spiders/uni_scraper.py

import scrapy
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

class ProfessorSpider(scrapy.Spider):
    name = "imperial"
    allowed_domains = ["profiles.imperial.ac.uk"]
    start_url = "https://profiles.imperial.ac.uk/search?by=text&type=user&v=" 

    def start_requests(self):
        # Use Selenium to paginate and collect all profile links
        profile_links = self.collect_all_profile_links()
        print(f"Collected {len(profile_links)} profile links.")
        for link in profile_links:
            yield scrapy.Request(link, callback=self.parse_profile)

    def collect_all_profile_links(self):
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get(self.start_url)

        profile_links = set()

        try:
            while True:
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                anchors = soup.select("div.profileStub__name___lWU19 a")
                for a in anchors:
                    href = a.get("href")
                    if href:
                        full_url = driver.current_url.split("/")[0] + "//" + driver.current_url.split("/")[2] + href
                        profile_links.add(full_url)

                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Move to the next page"]')
                    if not next_button.is_enabled():
                        break
                    next_button.click()
                except NoSuchElementException:
                    break
        finally:
            driver.quit()

        return list(profile_links)

    def parse_profile(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        name_tag = soup.select_one('div.hero__heroDetails___bp7ki h1')
        name = name_tag.get_text(strip=True) if name_tag else None

        title_tag = soup.select_one('p.userHero__position___Zi_A')
        title = title_tag.get_text(strip=True) if title_tag else None

        position_tag = soup.select_one('p.userHero__department___KwMvK')
        position = position_tag.get_text(strip=True) if position_tag else None


        bio_tag = soup.select_one('div.whiteBox__body___nZQwU p')
        bio = bio_tag.get_text(strip=True) if bio_tag else None


        photo_tag = soup.select_one('div.thumbnail__thumbnailContainer___mlIkK thumbnail__hasThumbnail___YiOiO thumbnail__hero___uw6mP img')
        photo_src = photo_tag['src'] if photo_tag else None
        photo_url = response.urljoin(photo_src) if photo_src else None

        yield {
            'university': "Imperial College London",
            'name': " ".join(name.split()) if name else None,
            'title': title.strip() if title else None,
            'url': response.url,
            'position': position.strip() if position else None,
            'bio': bio,
            'photo_url': photo_url.strip() if photo_url else None
        }
