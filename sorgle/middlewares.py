from scrapy import signals

from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from scrapy.http import HtmlResponse
from selenium import webdriver
import time

class SorgleSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    async def process_start(self, start):
        # Called with an async iterator over the spider start() method or the
        # maching method of an earlier spider middleware.
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class SorgleDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


from scrapy.http import HtmlResponse
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import shutil

class SeleniumMiddleware:
    def __init__(self, driver_path):
        self.driver_path = driver_path

    @classmethod
    def from_crawler(cls, crawler):
        path = shutil.which("msedgedriver")  # Or set manually
        middleware = cls(driver_path=path)
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def _init_driver(self):
        options = EdgeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        service = EdgeService(executable_path=self.driver_path)
        return webdriver.Edge(service=service, options=options)

    def process_request(self, request, spider):
        if not request.meta.get('selenium'):
            return None

        driver = self._init_driver()
        driver.get(request.url)

        # Input the search term
        search_term = request.meta.get('search_term')
        try:
            search_box = driver.find_element(By.ID, "edit-lastname")
            search_box.clear()
            search_box.send_keys(search_term)
            search_box.send_keys(Keys.RETURN)
            time.sleep(2)  # wait for results to load
        except Exception as e:
            spider.logger.warning(f"Selenium error for {search_term}: {e}")

        body = driver.page_source
        driver.quit()

        return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)

    def spider_closed(self):
        pass


