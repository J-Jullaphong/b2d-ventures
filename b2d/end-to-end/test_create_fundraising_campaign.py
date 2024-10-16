import time
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from mysite.wsgi import *
from ..models import Business, FundRaising


class TestFundraisingCampaignCreation(unittest.TestCase):
    """Test Case B2D_009: Test creating a fundraising campaign as a business owner."""

    def setUp(self):
        """Setup the browser and login before each test."""
        options = Options()
        options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('http://localhost:8000/login/')
        time.sleep(3)

        self.login()

    def login(self):
        """Log the business owner in before testing."""
        driver = self.driver

        username_input = driver.find_element(By.NAME, 'username')
        username_input.clear()
        username_input.send_keys('info@healthbiz.com')
        time.sleep(1)

        password_input = driver.find_element(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys('Hb!47xGk9$')
        time.sleep(1)

        login_button = driver.find_element(By.XPATH,
                                           '/html/body/div/div/form/button')
        login_button.click()
        time.sleep(3)

    def test_create_fundraising_campaign(self):
        """Test the process of creating a fundraising campaign."""
        driver = self.driver

        user_menu = driver.find_element(By.ID, 'dropdownUser')
        user_menu.click()
        time.sleep(1)

        fundraising_link = driver.find_element(By.XPATH,
                                               '//*[@id="navbarContent"]/ul[2]/li/ul/li[2]/a')
        self.assertIsNotNone(fundraising_link, "Fundraising option not found!")
        fundraising_link.click()
        time.sleep(3)

        goal_input = driver.find_element(By.NAME, 'goal_amount')
        self.assertIsNotNone(goal_input, "Goal amount input field not found!")
        goal_input.send_keys('500000')
        time.sleep(1)

        publish_date_input = driver.find_element(By.NAME, 'publish_date')
        self.assertIsNotNone(publish_date_input,
                             "Publish date input field not found!")
        publish_date_input.send_keys('10/10/2024')
        time.sleep(1)

        deadline_date_input = driver.find_element(By.NAME, 'deadline_date')
        self.assertIsNotNone(deadline_date_input,
                             "Deadline date input field not found!")
        deadline_date_input.send_keys('31/12/2024')
        time.sleep(1)

        min_investment_input = driver.find_element(By.NAME,
                                                   'minimum_investment')
        self.assertIsNotNone(min_investment_input,
                             "Minimum investment input field not found!")
        min_investment_input.send_keys('10000')
        time.sleep(1)

        shares_input = driver.find_element(By.NAME, 'shares_percentage')
        self.assertIsNotNone(shares_input,
                             "Shares percentage input field not found!")
        shares_input.send_keys('10')
        time.sleep(1)

        create_button = driver.find_element(By.XPATH,
                                            '/html/body/div/form/div[2]/button')
        self.assertIsNotNone(create_button,
                             "Create Fundraising button not found!")
        create_button.click()
        time.sleep(3)

        success_message = driver.find_element(By.XPATH,
                                              '/html/body/div/div/div')
        self.assertIsNotNone(success_message,
                             "Success message not found! Fundraising creation might have failed.")

        print(
            "Test Passed: Fundraising campaign successfully created and pending admin approval.")

    def tearDown(self):
        """Close the browser and clear fundraising campaign after each test."""
        self.clear_fundraising_campaign(user_id=8)
        self.driver.quit()

    def clear_fundraising_campaign(self, user_id):
        """Clear fundraising campaign in the database."""
        try:
            business = Business.objects.get(id=user_id)
            fundraising = FundRaising.objects.filter(business=business)
            fundraising.delete()
            print(
                f"Fundraising campaign for user {user_id} cleared from the database.")
        except Business.DoesNotExist:
            print(f"No business found for user {user_id}.")


if __name__ == '__main__':
    unittest.main()
