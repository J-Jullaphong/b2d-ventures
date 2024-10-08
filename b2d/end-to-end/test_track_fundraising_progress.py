import time
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class TestTrackFundraisingProgress(unittest.TestCase):
    """Test Case B2D_010: Test tracking the progress of a fundraising campaign as a business owner."""

    def setUp(self):
        """Setup the browser and login before each test."""
        options = Options()
        options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('http://localhost:8000/login/')
        time.sleep(3)

        self.login()

    def login(self):
        """Log the user in before testing."""
        driver = self.driver

        username_input = driver.find_element(By.NAME, 'username')
        username_input.clear()
        username_input.send_keys('ceo.john@techbridge.io')
        time.sleep(1)

        password_input = driver.find_element(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys('Tech4Future2024$')
        time.sleep(1)

        login_button = driver.find_element(By.XPATH,
                                           '/html/body/div/div/form/button')
        login_button.click()
        time.sleep(3)

    def test_view_investment_portfolio(self):
        """Test viewing fundraising campaign details as a business owner."""
        driver = self.driver

        user_menu = driver.find_element(By.ID, 'dropdownUser')
        user_menu.click()
        time.sleep(1)

        fundraising_link = driver.find_element(By.XPATH,
                                               '//*[@id="navbarContent"]/ul[2]/li/ul/li[2]/a')
        self.assertIsNotNone(fundraising_link, "Fundraising option not found!")
        fundraising_link.click()
        time.sleep(3)

        fundraising_details = driver.find_element(By.XPATH,
                                                  '/html/body/div/div[2]/div[2]')
        self.assertIsNotNone(fundraising_details,
                             "Fundraising details not found!")

        investment_graph = driver.find_element(By.ID,
                                               'investmentChart')
        self.assertIsNotNone(investment_graph,
                             "Investment history graph not found!")

        individual_investments = driver.find_element(By.XPATH,
                                                     '/html/body/div/div[3]/table')
        self.assertIsNotNone(individual_investments,
                             "Individual investments not found!")

        print(
            "Test Passed: Fundraising details, investment history graph, and individual investments are displayed correctly.")

    def tearDown(self):
        """Close the browser after each test."""
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
