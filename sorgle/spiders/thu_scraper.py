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
import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class ProfessorSpider(scrapy.Spider):
    name = "thu_cs1"
    allowed_domains = ["cs.tsinghua.edu.cn"]
    start_urls = ["https://www.cs.tsinghua.edu.cn/csen/Faculty/Full_time_Faculty.htm"]

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        # 1) Loop over each <dl> block
        for dl in soup.find_all("dl"):
            # 2) In each <dl> find the <li> entries under the 'clear' UL
            for li in dl.select("ul.clear > li"):
                # TEASER data from the listing:
                name_tag = li.select_one("div.text h2")
                name = name_tag.get_text(strip=True) if name_tag else ""

                # phone is usually in a <p> starting with + or digit
                phone = ""
                for p in li.select("div.text p"):
                    txt = p.get_text(strip=True)
                    if txt and (txt[0].isdigit() or txt.startswith("+")):
                        phone = txt
                        break

                # email is any <p> containing an "@"
                email = ""
                for p in li.select("div.text p"):
                    if "@" in p.get_text():
                        email = p.get_text(strip=True)
                        break

                # PROFILE LINK
                pic_a = li.select_one("div.pic a[href]")
                if not pic_a:
                    continue
                profile_url = urljoin(response.url, pic_a["href"])

                # Follow that profile page, passing teaser data along in meta
                yield scrapy.Request(
                    profile_url,
                    callback=self.parse_profile,
                    meta={
                        "name": name,
                        "phone": phone,
                        "email": email,
                    },
                )

    def parse_profile(self, response):
        # 1) Recover teaser fields
        name  = response.meta.get("name", "")
        phone = response.meta.get("phone", "")
        email = response.meta.get("email", "")

        # 2) Scrape the rest of the profile with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # # e.g. title inside some div.position
        # title_tag = soup.select_one("div.position")
        # title = title_tag.get_text(strip=True) if title_tag else ""

        # # e.g. unit in the <dt><h4> under people01
        # unit_tag = soup.select_one("div.people01 dt h4")
        # unit = unit_tag.get_text(strip=True) if unit_tag else ""

        # # e.g. optional PDF/CV link
        # cv_a = soup.find("a", href=lambda u: u and u.lower().endswith(".pdf"))
        # curriculum_link = urljoin(response.url, cv_a["href"]) if cv_a else None

        content_div = soup.find("div", class_="v_news_content")
        
        if content_div:
            pieces = []
            # select both section headers and paragraphs
            for el in content_div.find_all(["h4", "p"]):
                # you can choose to keep the heading tags separate or prefix them,
                # here we just collect the stripped text in order
                txt = el.get_text(strip=True)
                if txt:
                    pieces.append(txt.strip())
                    pieces.append(" ")
                      # add a newline after each piece
        img_url = None
        if content_div:
            img_tag = content_div.find("img", class_="img_vsb_content")
            if img_tag and img_tag.get("src"):
                img_url = urljoin(response.url, img_tag["src"])
           
        yield {
            "university": "Tsinghua University",
            "url": response.url,
            "name": name,
            "phone": phone,
            "email": email,
            "bio": pieces if pieces else [],
            "title": "Department of Computer Science and Technology",
            "photo": img_url
        }
