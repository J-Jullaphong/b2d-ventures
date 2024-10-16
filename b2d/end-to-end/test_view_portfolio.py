import time
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class TestViewPortfolio(unittest.TestCase):
    """Test Case B2D_004: Test viewing the investment portfolio with detailed breakdowns."""

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
        username_input.send_keys('johndoe@example.com')
        time.sleep(1)

        password_input = driver.find_element(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys('Passw0rd!123')
        time.sleep(1)

        login_button = driver.find_element(By.XPATH,
                                           '/html/body/div/div/form/button')
        login_button.click()
        time.sleep(3)

    def test_view_investment_portfolio(self):
        """Test viewing the investment portfolio with total investment and pie chart."""
        driver = self.driver

        user_menu = driver.find_element(By.ID, 'dropdownUser')
        user_menu.click()
        time.sleep(1)

        portfolio_link = driver.find_element(By.XPATH,
                                             '//*[@id="navbarContent"]/ul[2]/li/ul/li[1]/a')
        self.assertIsNotNone(portfolio_link, "Portfolio option not found!")
        portfolio_link.click()
        time.sleep(3)

        investment_summary = driver.find_element(By.XPATH,
                                                 '/html/body/div/div[2]/div[1]/table')
        self.assertIsNotNone(investment_summary,
                             "Investment summary not found!")

        pie_chart = driver.find_element(By.ID, 'investmentPieChart')
        self.assertIsNotNone(pie_chart, "Pie chart not found!")

        total_investment = driver.find_element(By.XPATH,
                                               '/html/body/div/div[2]/div[1]/div/h2/span')
        self.assertTrue(total_investment.text.strip().startswith("$"),
                        "Total investment amount is missing or incorrect!")

        print(
            "Test Passed: Portfolio summary and pie chart are displayed correctly.")

    def tearDown(self):
        """Close the browser after each test."""
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
