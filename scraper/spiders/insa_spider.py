import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import itertools

class InsaSpider(scrapy.Spider):
    name = 'insa'
    allowed_domains = ['insa-lyon.fr']
    # start_urls = []  # Prevent Scrapy from auto-calling with a scrapy.Request
    url = 'https://www.insa-lyon.fr/fr/annuaire_etablissement'

    def start_requests(self):
        for combo in itertools.product('abc', repeat=2): # defghijklmnopqrstuvwxyz
            search_term = ''.join(combo)
            yield SeleniumRequest(
                url=self.url,
                callback=self.parse,
                wait_time=10,
                wait_until=lambda d: d.find_element(By.ID, 'edit-lastname'),
                meta={'search_term': search_term},
                dont_filter=True
            )


    def parse(self, response):
        # Confirm response is from Selenium
        if not hasattr(response, "driver"):
            self.logger.error("Response does not contain a Selenium driver. Check request type.")
            return
        
        driver = response.driver
        search_term = response.meta['search_term']

        # Input the search term into the last-name field
        search_box = driver.find_element(By.ID, 'edit-lastname')
        search_box.clear()
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)

        # Wait for the table of results to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.sticky-enabled'))
        )

        # Parse the rendered HTML
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', class_='sticky-enabled')
        if not table:
            return

        rows = table.find_all('tr')[1:]  # Skip header
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 5:
                continue

            first_name = cols[0].get_text(strip=True)
            last_name = cols[1].get_text(strip=True)

            # Clean up phone numbers
            phone_entries = cols[2].get_text(strip=True, separator='\n').split('\n')
            phones = [p.strip() for p in phone_entries if p.strip() and p.strip() != '-']

            # Clean up departments
            dept_entries = cols[3].get_text(strip=True, separator='\n').split('\n')
            departments = [d.strip() for d in dept_entries if d.strip()]

            # Extract roles
            roles = [a.get_text(strip=True).lower() for a in cols[4].find_all('a')]

            # Filter on teacher or staff roles
            if any(r in ('teacher', 'staff') for r in roles):
                yield {
                    'first_name': first_name,
                    'last_name': last_name,
                    'phone': ';'.join(phones),
                    'department': ';'.join(departments),
                    'role': ';'.join(roles),
                }
