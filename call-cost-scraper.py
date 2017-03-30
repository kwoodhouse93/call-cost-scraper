# coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Assuming you want the standard landline rate on a pay monthly contract...

# Steps to find call cost
# 1. Navigate to the link:
#   http://international.o2.co.uk/internationaltariffs/calling_abroad_from_uk
# 2. Using input#countryName...
# 3. Enter the country name and press Enter
# 4. Click a#paymonthly
# 5. Look in table#standardRatesTable for
#    <td>Landline</td><td>*XXXX*</td>

class CallCostScraper:
    def __init__(self, target_url):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10) # seconds
        self.target_url = target_url
        # self.load_page()

    def load_page(self):
        self.driver.get(self.target_url)

    def lookup_country(self, country):
        input_elem = self.driver.find_element_by_id("countryName")
        # TODO: Check if element is the input we're after
        input_elem.clear()
        input_elem.send_keys(country)
        input_elem.send_keys(Keys.RETURN)

        wait = WebDriverWait(self.driver, 10)
        paym_elem = wait.until(EC.element_to_be_clickable((By.ID, 'paymonthly')))
        # paym_elem = self.driver.find_element_by_xpath("//*[@id='paymonthly']")
        paym_elem.click()

    def find_rate(self):
        price_elem = self.driver.find_element_by_xpath("//*[@id='standardRatesTable']/tbody/tr[1]/td[contains(text(),'Landline')]/following-sibling::td[1]")
        # TODO: Check we got a price
        return unicode(price_elem.text)

    def get_country_price(self, country):
        self.load_page()
        self.lookup_country(country)
        return self.find_rate()

    pass

scraper = CallCostScraper("http://international.o2.co.uk/internationaltariffs/calling_abroad_from_uk")
countries_to_lookup = ['Canada', 'Germany', 'Iceland', 'Pakistan', 'Singapore', 'South Africa']

for country in countries_to_lookup:
    price = scraper.get_country_price(country)
    print("Price for " + country + ": " + price)