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


# Example usage
if __name__ == "__main__":
    found = scrape_lname_links(
        url="https://www.kuleuven.be/wieiswie/en/person/search",
        query="A",
        search_selector=(By.ID, "personinput"),  # adjust as needed
        lname_links_selector=(By.CSS_SELECTOR, "a.lname"),
        driver_path=None,
        headless=True
    )
    print("Person links:")
    for link in found:
        print(link)