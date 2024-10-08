import time
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class TestViewBusinessDetail(unittest.TestCase):
    """Test Case B2D_002: Test viewing business details functionality."""

    def setUp(self):
        """Setup the browser before each test."""
        options = Options()
        options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(
            'http://localhost:8000/businesses/')
        time.sleep(3)

    def test_view_business_details(self):
        """Test viewing business details after browsing."""
        driver = self.driver

        print("Opening the business browsing page...")

        business_list = driver.find_elements(By.XPATH,
                                             '/html/body/div/div[2]/div/div')
        self.assertGreater(len(business_list), 0, "No businesses found!")
        print(f"Found {len(business_list)} businesses.")

        business_to_view = None
        for business in business_list:
            business_name = business.find_element(By.CLASS_NAME,
                                                  'card-title').text
            if "TechBridge" in business_name:
                business_to_view = business
                break

        self.assertIsNotNone(business_to_view, "TechBridge not found!")
        business_to_view.click()
        time.sleep(3)

        business_name_displayed = driver.find_element(By.XPATH,
                                                      '/html/body/div/div[1]/div[1]/div[2]/div/h1').text
        self.assertEqual(business_name_displayed, "TechBridge",
                         "Displayed business name does not match!")

        business_description_displayed = driver.find_element(By.XPATH,
                                                             '/html/body/div/div[1]/div[1]/div[2]/div/div[1]/p').text
        self.assertTrue(len(business_description_displayed) > 0,
                        "Business description is missing!")

        print(
            "Test Passed: Detailed business information is displayed correctly.")

    def tearDown(self):
        """Close the browser after each test."""
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
