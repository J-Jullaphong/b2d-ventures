import time
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class TestBusinessBrowsing(unittest.TestCase):
    """Test Case B2D_001: Test business browsing and search functionality"""

    def setUp(self):
        """Setup the browser before each test."""
        options = Options()
        options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('http://localhost:8000/')
        time.sleep(3)

    def test_business_browsing_and_search(self):
        """Test business browsing, search, category filter, and sort functionality."""
        driver = self.driver
        search_term = 'bridge'

        search_bar = driver.find_element(By.CLASS_NAME, 'search-input')
        search_bar.send_keys(search_term)
        search_bar.send_keys(Keys.RETURN)
        time.sleep(2)

        sort_dropdown = Select(driver.find_element(By.NAME, 'sort'))
        sort_dropdown.select_by_visible_text('Most Investors')
        time.sleep(2)

        category_dropdown = Select(driver.find_element(By.NAME, 'category'))
        category_dropdown.select_by_visible_text('Technology')
        time.sleep(2)

        search_results = driver.find_elements(By.XPATH,
                                              '/html/body/div/div[2]/div/div')
        self.assertGreater(len(search_results), 0,
                           "No businesses found after search and filters.")

        for result in search_results:
            business_name = result.text
            self.assertIn(search_term.lower(), business_name.lower(),
                          f"Search result '{business_name}' does not match search term '{search_term}'.")

        print(
            "Test Passed: Business listings are displayed correctly based on search and filter criteria.")

    def tearDown(self):
        """Close the browser after each test."""
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
