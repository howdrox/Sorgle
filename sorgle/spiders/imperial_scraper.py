import scrapy
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy import signals
from webdriver_manager.chrome import ChromeDriverManager
import time
from urllib.parse import urljoin

class ProfessorSpider(scrapy.Spider):
    name = "imperial"
    allowed_domains = ["profiles.imperial.ac.uk"]
    start_urls = ["https://profiles.imperial.ac.uk/search?by=text&type=user"]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        # hook spider_closed so we can quit the driver
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)

        # instantiate the headless Chrome driver here
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        spider.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        return spider
    
    def spider_closed(self):
        """Clean up the Selenium driver when the spider finishes."""
        self.logger.info("Closing Selenium driver")
        if hasattr(self, 'driver'):
            self.driver.quit()

    def start_requests(self):
        # Use Selenium to paginate and collect all profile links
        profile_links = self.collect_all_profile_links()
        print(f"Collected {len(profile_links)} profile links.")
        for link in profile_links:
            yield scrapy.Request(link, callback=self.parse_profile)



    def collect_all_profile_links(self):


        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        collection_driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        profile_links = set()

        try:
            collection_driver.get(self.start_urls[0])
            self.logger.info(f"Starting profile collection from: {self.start_urls[0]}")
            
            page_num = 1
            while True:
                self.logger.info(f"Processing page {page_num}")
                time.sleep(3)
                soup = BeautifulSoup(collection_driver.page_source, "html.parser")
                anchors = soup.select("div[class*='profileStub__name'] a")
                page_links_found = 0
                for a in anchors:
                    href = a.get("href")
                    if href:
                        full_url = urljoin(collection_driver.current_url, href)
                        if full_url not in profile_links:
                            profile_links.add(full_url)
                            page_links_found += 1
                self.logger.info(f"Found {page_links_found} new profile links on page {page_num}")


                try:
                    next_button = WebDriverWait(collection_driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Move to the next page"]'))
                    )
                    
                    if not next_button.is_enabled():
                        self.logger.info("Next button is disabled, reached last page")
                        break
                    collection_driver.execute_script("arguments[0].scrollIntoView();", next_button)
                    time.sleep(1)
                    next_button.click()
                    page_num += 1
                    time.sleep(2)
                except Exception as e:
                    break
        except Exception as e:
            self.logger.error(f"Error during profile link collection: {e}")
        finally:
            collection_driver.quit()
        self.logger.info(f"Total unique profile links collected: {len(profile_links)}")

        return list(profile_links)

    def parse_profile(self, response):
        self.driver.get(response.url)
        time.sleep(2)   # short pause so React has a chance to finish rendering



        # self.driver.get(response.url)
        wait = WebDriverWait(self.driver, 10)
        # soup = BeautifulSoup(response.text, 'html.parser')

        # wait until the H1 with id="mainContentProfilePage" appears
        name_el = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#mainContentProfilePage")
            ))
        name = name_el.text.strip()
        # wait for the sidebar “Positions” section to appear
        wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR,
        "li[data-qa='sidebar positionAndDepartment']"
        )))

    # find that <li>
        li = self.driver.find_element(
        By.CSS_SELECTOR,
        "li[data-qa='sidebar positionAndDepartment']"
            )

    # inside it, find the content container
        content = li.find_element(
         By.CSS_SELECTOR,
        'div[class*="iconAndContentRow__content"]'
        )

    # first <div> is the title
        
        title = content.find_element(By.XPATH, "./div[1]").text.strip()

    # second <div> is the department
        department = content.find_element(By.XPATH, "./div[2]").text.strip()
        try:
            bio_header = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'div[class*="whiteBox__body"]'
                )))

            bio = bio_header.text.strip()
        except Exception:
            bio = None

        try:
            img_el = wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'div[class*="thumbnail__thumbnailContainer"] img'
            )))
            img_src = img_el.get_attribute("src")

        except Exception:
            img_src = None

        yield {
            'university': "Imperial College London",
            'name': " ".join(name.split()) if name else None,
            'title': title.strip() if title else None,
            'url': response.url,
            'position': department.strip() if department else None,
            'bio': bio,
            'photo_url': img_src.strip() if img_src else None
        }
