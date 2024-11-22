import time
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from mysite.wsgi import *
from django_otp.plugins.otp_email.models import EmailDevice


class TestViewPortfolio(unittest.TestCase):
    """Test Case B2D_004: Test viewing the investment portfolio with detailed breakdowns."""

    def setUp(self):
        """Setup the browser and login before each test."""
        options = Options()
        options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('http://localhost:8000/login/')
        self.device = EmailDevice.objects.get(user_id="effb52fe-9db8-455c-8810-a135f0ab6402")
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

        get_otp_button = driver.find_element(By.XPATH,
                                             '/html/body/div/div/form/button')
        self.assertIsNotNone(get_otp_button, "Get OTP button not found!")
        get_otp_button.click()
        time.sleep(5)

        self.device.refresh_from_db()

        otp_token_input = driver.find_element(By.XPATH,
                                              '//*[@id="id_otp_token"]')
        self.assertIsNotNone(otp_token_input,
                             "OTP Token input field not found!")
        otp_token_input.send_keys(self.device.token)
        time.sleep(1)

        verify_otp_button = driver.find_element(By.XPATH,
                                                '/html/body/div/div/form/button')
        self.assertIsNotNone(verify_otp_button, "Verify OTP button not found!")
        verify_otp_button.click()
        time.sleep(3)

    def test_view_investment_portfolio(self):
        """Test viewing the investment portfolio with total investment and pie chart."""
        driver = self.driver

        user_menu = driver.find_element(By.ID, 'dropdownUser')
        user_menu.click()
        time.sleep(1)

        portfolio_link = driver.find_element(By.XPATH,
                                             '//*[@id="navbarContent"]/ul[2]/li/ul/li[2]/a')
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
