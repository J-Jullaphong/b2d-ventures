import time
import unittest

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from mysite.wsgi import *
from ..models import Investor


class TestInvestorRegistration(unittest.TestCase):
    """Test Case B2D_005: Test registration process for a new investor."""

    def setUp(self):
        """Setup the browser before each test."""
        options = Options()
        options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('http://localhost:8000/')
        time.sleep(3)

    def test_investor_registration(self):
        """Test the investor registration process."""
        driver = self.driver

        login_button = driver.find_element(By.XPATH,
                                           '//*[@id="navbarContent"]/ul[2]/li/a')
        self.assertIsNotNone(login_button, "Login button not found!")
        login_button.click()
        time.sleep(2)

        sign_up_link = driver.find_element(By.XPATH,
                                           '/html/body/div/div/div/p[2]/a')
        self.assertIsNotNone(sign_up_link, "Sign Up link not found!")
        sign_up_link.click()
        time.sleep(2)

        investor_option = driver.find_element(By.XPATH,
                                              '/html/body/div/div/ul/li[1]/a')
        self.assertIsNotNone(investor_option, "Investor option not found!")
        investor_option.click()
        time.sleep(2)

        driver.find_element(By.NAME, 'first_name').send_keys('FirstName')
        time.sleep(1)
        driver.find_element(By.NAME, 'last_name').send_keys('LastName')
        time.sleep(1)
        driver.find_element(By.NAME, 'email').send_keys('FN@gmail.com')
        time.sleep(1)
        driver.find_element(By.NAME, 'phone_number').send_keys('1234567890')
        time.sleep(1)
        driver.find_element(By.NAME, 'password1').send_keys('@Password123')
        time.sleep(1)
        driver.find_element(By.NAME, 'password2').send_keys('@Password123')
        time.sleep(1)

        financial_statements_input = driver.find_element(By.NAME,
                                                         'financial_statements')
        self.assertIsNotNone(financial_statements_input,
                             "Financial statements upload field not found!")
        financial_statements_input.send_keys(
            f'{os.path.abspath(os.getcwd())}/b2d/end-to-end/Financial_Statement.pdf')
        time.sleep(1)

        iframe = driver.find_element(By.CSS_SELECTOR, "iframe[title='reCAPTCHA']")
        time.sleep(1)

        driver.switch_to.frame(iframe)
        time.sleep(2)

        captcha_checkbox = driver.find_element(By.ID, "recaptcha-anchor")
        captcha_checkbox.click()
        time.sleep(1)

        driver.switch_to.default_content()
        time.sleep(2)

        terms_checkbox = driver.find_element(By.ID, 'termsCheckbox')
        terms_checkbox.click()
        time.sleep(1)

        sign_up_button = driver.find_element(By.XPATH,
                                             '/html/body/div/div/form/button')
        self.assertIsNotNone(sign_up_button, "Sign Up button not found!")
        sign_up_button.click()
        time.sleep(3)

        success_message = driver.find_element(By.XPATH,
                                              '/html/body/div/div/div[1]')
        self.assertIsNotNone(success_message,
                             "Success message not found! Registration might have failed.")

        print(
            "Test Passed: Investor registration completed successfully and is pending admin approval.")

    def tearDown(self):
        """Clear out investor in the database and remove S3 file after each test."""
        test_investor = Investor.objects.last()
        self.clear_investor_details(user_id=test_investor.id)
        self.clear_s3_storage(user_id=test_investor.id)
        self.driver.quit()

    def clear_investor_details(self, user_id):
        """Delete the investor record from the database for the specified user ID."""
        try:
            investor = Investor.objects.get(id=user_id)
            investor.delete()
            print(
                f"Investor record with user ID {user_id} deleted from the database.")
        except Investor.DoesNotExist:
            print(f"No investor found for user ID {user_id}.")

    def clear_s3_storage(self, user_id):
        """Delete the specified investor's financial statement file from S3 storage."""
        s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_S3_REGION_NAME)
        file_key = f'investor_docs/{user_id}.pdf'
        try:
            s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                             Key=file_key)
            print(f"File '{file_key}' deleted from S3 storage.")
        except ClientError as e:
            print(f"Error deleting file from S3: {e}")


if __name__ == '__main__':
    unittest.main()
