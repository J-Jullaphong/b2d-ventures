import time
import unittest


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from mysite.wsgi import *
from django_otp.plugins.otp_email.models import EmailDevice


class TestLoginProcess(unittest.TestCase):
    """Test Case B2D_007: Test login process for both investors and business owners."""

    def setUp(self):
        """Setup the browser before each test."""
        options = Options()
        options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('http://localhost:8000/')
        self.device = EmailDevice.objects.get(user_id="effb52fe-9db8-455c-8810-a135f0ab6402")
        time.sleep(3)

    def test_login_process(self):
        """Test the login functionality for both investors and business owners."""
        driver = self.driver

        login_button = driver.find_element(By.LINK_TEXT, 'Login')
        self.assertIsNotNone(login_button, "Login button not found!")
        login_button.click()
        time.sleep(2)

        username_input = driver.find_element(By.NAME, 'username')
        self.assertIsNotNone(username_input, "Username input field not found!")
        username_input.send_keys('johndoe@example.com')
        time.sleep(1)

        password_input = driver.find_element(By.NAME, 'password')
        self.assertIsNotNone(password_input, "Password input field not found!")
        password_input.send_keys('Passw0rd!123')
        time.sleep(1)

        submit_button = driver.find_element(By.XPATH,
                                            '/html/body/div/div/form/button')
        self.assertIsNotNone(submit_button, "Submit button not found!")
        submit_button.click()
        time.sleep(3)

        get_otp_button = driver.find_element(By.XPATH,
                                            '/html/body/div/div/form/button')
        self.assertIsNotNone(get_otp_button, "Get OTP button not found!")
        get_otp_button.click()
        time.sleep(5)

        self.device.refresh_from_db()

        otp_token_input = driver.find_element(By.XPATH, '//*[@id="id_otp_token"]')
        self.assertIsNotNone(otp_token_input, "OTP Token input field not found!")
        otp_token_input.send_keys(self.device.token)
        time.sleep(1)

        verify_otp_button = driver.find_element(By.XPATH,
                                             '/html/body/div/div/form/button')
        self.assertIsNotNone(verify_otp_button, "Verify OTP button not found!")
        verify_otp_button.click()
        time.sleep(3)

        user_menu = driver.find_element(By.ID, 'dropdownUser')
        self.assertIsNotNone(user_menu,
                             "User menu not found, login might have failed!")
        self.assertEqual(user_menu.text, 'johndoe@example.com')

        print(
            "Test Passed: User successfully logged in and redirected to the home page.")

    def tearDown(self):
        """Close the browser after each test."""
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
