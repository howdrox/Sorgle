import time
import csv
import itertools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions
from bs4 import BeautifulSoup

options = EdgeOptions()
options.add_argument('--headless')  # Run browser in headless mode
# options.add_argument('--ignore-certificate-errors')  # Suppress SSL errors
# options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Suppress DevTools logs

driver = webdriver.Edge(options=options)

# Prepare the output CSV file
output_file = 'insa_teachers.csv'
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['First Name', 'Last Name', 'Phone', 'Department', 'Role'])

    try:
        # Generate all two-letter combinations from 'aa' to 'zz'
        for combo in itertools.product('abcdefghijklmnopqrstuvwxyz', repeat=2):
            search_term = ''.join(combo)
            print(f"Searching for: {search_term}")


            # Open the INSA Lyon directory page
            driver.get("https://www.insa-lyon.fr/fr/annuaire_etablissement")

            # Locate the input field and enter the search term
            search_field = driver.find_element(By.ID, "edit-lastname")
            search_field.clear()
            search_field.send_keys(search_term)
            search_field.send_keys(Keys.RETURN)

            # Wait for the page to load and display results
            time.sleep(2)  # Adjust sleep time if necessary

            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Find the table containing the results
            table = soup.find('table', class_='sticky-enabled')
            if not table:
                continue  # No results found for this search term

            rows = table.find_all('tr')[1:]  # Skip the header row

            # Extract and write the data
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 5:
                    first_name = cols[0].get_text(strip=True)
                    last_name = cols[1].get_text(strip=True)
                    phone_raw = cols[2].get_text(strip=True, separator='\n').split('\n')
                    phone = [p.strip() for p in phone_raw if p.strip() and p.strip() != '-']
                    department_raw = cols[3].get_text(strip=True, separator='\n').split('\n')
                    department = [dept.strip() for dept in department_raw if dept.strip()]
                    affiliations = [a.get_text(strip=True).lower() for a in cols[4].find_all('a')]

                    # Filter for 'teacher' or 'staff' affiliations
                    # if any(role in ['teacher', 'researcher'] for role in affiliations):
                    writer.writerow([first_name, last_name, ';'.join(phone), ';'.join(department), ';'.join(affiliations)])

    finally:
        # Close the WebDriver
        driver.quit()
