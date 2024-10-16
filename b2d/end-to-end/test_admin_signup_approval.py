import time
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class TestAdminApproveSignup(unittest.TestCase):
    """Test Case B2D_011: Test approving sign-up requests as an admin."""

    def setUp(self):
        """Setup the browser before each test."""
        options = Options()
        options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('http://localhost:8000/admin/login/')
        time.sleep(2)

        driver = self.driver
        driver.find_element(By.NAME, 'username').send_keys('admin')
        driver.find_element(By.NAME, 'password').send_keys('1234')
        driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(2)

    def test_approve_signup_request(self):
        """Test approving a pending signup request as admin."""
        driver = self.driver

        driver.find_element(By.LINK_TEXT, 'Businesses').click()
        time.sleep(2)

        signup_request = driver.find_element(By.XPATH, '//*[@id="result_list"]/tbody/tr[1]/th/a')
        signup_request.click()
        time.sleep(2)

        active_checkbox = driver.find_element(By.NAME, 'is_active')
        if not active_checkbox.is_selected():
            active_checkbox.click()
        time.sleep(1)

        save_button = driver.find_element(By.NAME, '_save')
        save_button.click()
        time.sleep(2)

        success_message = driver.find_element(By.CSS_SELECTOR, 'li.success')
        self.assertIsNotNone(success_message, "Success message not found! Approval might have failed.")

        print("Test Passed: The admin successfully approved the sign-up request.")

    def tearDown(self):
        """Tear down the browser session after each test."""
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
