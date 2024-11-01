import time
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from mysite.wsgi import *
from django_otp.plugins.otp_email.models import EmailDevice


class TestInvestment(unittest.TestCase):
    """Test Case B2D_003: Test the investment process for a business using QR code for payment."""

    def setUp(self):
        """Setup the browser and login before each test."""
        options = Options()
        options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('http://localhost:8000/login/')
        self.device = EmailDevice.objects.get(user_id=3)
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

        driver.get('http://localhost:8000/business/2/')
        time.sleep(3)

    def test_investment_process(self):
        """Test the investment process for a business using QR code payment."""
        driver = self.driver

        invest_button = driver.find_element(By.XPATH,
                                            '/html/body/div/div[1]/div[1]/div[2]/div/div[3]/a')
        invest_button.click()
        time.sleep(2)

        investment_amount = driver.find_element(By.NAME, 'amount')
        investment_amount.clear()
        investment_amount.send_keys("1000.00")
        time.sleep(1)

        transfer_date = driver.find_element(By.NAME, 'investment_datetime')
        transfer_date.clear()
        transfer_date.send_keys("03/10/2024")
        transfer_date.send_keys(Keys.TAB)
        transfer_date.send_keys("12:30")
        time.sleep(1)

        transaction_slip = driver.find_element(By.NAME, 'transaction_slip')
        transaction_slip.send_keys(
            f'{os.path.abspath(os.getcwd())}/transaction_slip.png')
        time.sleep(1)

        iframe = driver.find_element(By.CSS_SELECTOR, "iframe[title='reCAPTCHA']")
        driver.switch_to.frame(iframe)
        time.sleep(2)

        captcha_checkbox = driver.find_element(By.ID, "recaptcha-anchor")
        captcha_checkbox.click()
        time.sleep(1)

        driver.switch_to.default_content()
        time.sleep(2)

        terms_checkbox = driver.find_element(By.ID, 'agreementCheck')
        terms_checkbox.click()
        time.sleep(1)

        submit_button = driver.find_element(By.XPATH,
                                            '/html/body/div/div/form/div[3]/button')
        submit_button.click()
        time.sleep(3)

        self.assertEqual(self.driver.current_url,
                         'http://localhost:8000/business/2/')

        alert_message = driver.find_element(By.XPATH, '/html/body/div[1]/div')
        self.assertIn(
            'Your investment has been submitted and is pending admin approval.',
            alert_message.text)

        print("Test Passed: Investment successfully submitted.")

    def tearDown(self):
        """Close the browser after each test."""
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
