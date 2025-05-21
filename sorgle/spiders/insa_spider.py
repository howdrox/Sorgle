import scrapy
import itertools
from bs4 import BeautifulSoup

class InsaSpider(scrapy.Spider):
    name = 'insa'
    allowed_domains = ['insa-lyon.fr']
    start_urls = ['https://www.insa-lyon.fr/fr/annuaire_etablissement']

    def start_requests(self):
        for combo in itertools.product('abcdefghijklmnopqrstuvwxyz', repeat=2):
            search_term = ''.join(combo)
            yield scrapy.Request(
                url=self.start_urls[0],
                callback=self.parse,
                meta={'selenium': True, 'search_term': search_term}
            )

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='sticky-enabled')
        if not table:
            return

        rows = table.find_all('tr')[1:]  # Skip header
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 5:
                first_name = cols[0].get_text(strip=True)
                last_name = cols[1].get_text(strip=True)
                phone_raw = cols[2].get_text(strip=True, separator='\n').split('\n')
                phone = [p.strip() for p in phone_raw if p.strip() and p.strip() != '-']
                department_raw = cols[3].get_text(strip=True, separator='\n').split('\n')
                department = [dept.strip() for dept in department_raw if dept.strip()]
                role = [a.get_text(strip=True).lower() for a in cols[4].find_all('a')]

                if any(r in ['teacher', 'staff'] for r in role):
                    yield {
                        'first_name': first_name,
                        'last_name': last_name,
                        'phone': ';'.join(phone),
                        'department': ';'.join(department),
                        'role': ';'.join(role)
                    }
