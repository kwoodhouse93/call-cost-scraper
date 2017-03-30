# coding: utf-8
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CallCostScraper:
    def __init__(self, target_url):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10) # seconds
        self.target_url = target_url

    def load_page(self):
        self.driver.get(self.target_url)

    def lookup_country(self, country):
        input_elem = self.driver.find_element_by_id("countryName")

        input_elem.clear()
        input_elem.send_keys(country)
        input_elem.send_keys(Keys.RETURN)

        wait = WebDriverWait(self.driver, 10)
        paym_elem = wait.until(EC.element_to_be_clickable((By.ID, 'paymonthly')))
        paym_elem.click()

    def find_rate(self):
        price_elem = self.driver.find_element_by_xpath("//*[@id='standardRatesTable']/tbody/tr[1]/td[contains(text(),'Landline')]/following-sibling::td[1]")
        # There is an assumption that prices are between £1.00 and £9.99, or
        # otherwise take the form £0.XX if less than £1.00.
        prog = re.compile(ur"^£[0-9]\.[0-9]{2}$", re.UNICODE)
        if prog.match(price_elem.text) == None:
            print("Error! Value returned was not a price.")
            return None
        return unicode(price_elem.text)

    def get_country_price(self, country):
        self.load_page()
        self.lookup_country(country)
        return self.find_rate()

    pass

TGT_URL = "http://international.o2.co.uk/internationaltariffs/calling_abroad_from_uk"
countries_to_lookup = ['Canada', 'Germany', 'Iceland', 'Pakistan', 'Singapore', 'South Africa']

scraper = CallCostScraper(TGT_URL)

for country in countries_to_lookup:
    price = scraper.get_country_price(country)
    print("Price for " + country + ": " + unicode(price))
