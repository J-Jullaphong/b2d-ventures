import time
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class TestAdminApproveFundraising(unittest.TestCase):
    """Test Case B2D_013: Test approving fundraising requests as an admin."""

    def setUp(self):
        """Setup the browser before each test."""
        options = Options()
        options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('http://localhost:8000/admin/login/')
        time.sleep(2)

        driver = self.driver
        driver.find_element(By.NAME, 'username').send_keys('b2d-ventures-admin')
        driver.find_element(By.NAME, 'password').send_keys('@AdminPassword123')
        driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(2)

    def test_approve_fundraising_request(self):
        """Test approving a pending fundraising request as admin."""
        driver = self.driver

        driver.find_element(By.LINK_TEXT, 'Fundraising Campaigns').click()
        time.sleep(2)

        fundraising_request = driver.find_element(By.XPATH,
                                                  '//*[@id="result_list"]/tbody/tr[1]/th/a')
        fundraising_request.click()
        time.sleep(2)

        status_dropdown = driver.find_element(By.ID, 'id_fundraising_status')
        status_dropdown.click()
        time.sleep(1)

        approve_option = driver.find_element(By.XPATH,
                                             '//select[@id="id_fundraising_status"]/option[@value="approve"]')
        approve_option.click()
        time.sleep(1)

        save_button = driver.find_element(By.NAME, '_save')
        save_button.click()
        time.sleep(2)

        success_message = driver.find_element(By.CSS_SELECTOR, 'li.success')
        self.assertIsNotNone(success_message,
                             "Success message not found! Approval might have failed.")

        print(
            "Test Passed: The admin successfully approved the fundraising request.")

    def tearDown(self):
        """Tear down the browser session after each test."""
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
