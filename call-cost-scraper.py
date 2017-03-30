from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Assuming you want the standard rate

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
        self.target_url = target_url
        self.load_page()
    
    def load_page(self):
        self.driver.get(self.target_url)
    
    def input_country(self, country):
        pass
        
    def find_rate(self):
        pass
    
    def get_country_price(self, country):
        self.input_country(country)
        self.find_rate()
    
    pass

scraper = CallCostScraper("http://international.o2.co.uk/internationaltariffs/calling_abroad_from_uk")
scraper.get_country_price("Canada")
