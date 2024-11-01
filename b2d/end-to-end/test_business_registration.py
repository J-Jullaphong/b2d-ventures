import time
import unittest

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from mysite.wsgi import *
from ..models import Business


class TestBusinessRegistration(unittest.TestCase):
    """Test Case B2D_006: Test the registration process for a new business owner."""

    def setUp(self):
        """Setup the browser before each test."""
        options = Options()
        options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('http://localhost:8000/')
        time.sleep(3)

    def test_business_registration(self):
        """Test the business registration process."""
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

        business_option = driver.find_element(By.XPATH,
                                              '/html/body/div/div/ul/li[2]/a')
        self.assertIsNotNone(business_option, "Business option not found!")
        business_option.click()
        time.sleep(2)

        driver.find_element(By.NAME, 'name').send_keys('Company1')
        time.sleep(1)
        driver.find_element(By.NAME, 'email').send_keys('C1@gmail.com')
        time.sleep(1)
        driver.find_element(By.NAME, 'phone_number').send_keys('1234567890')
        time.sleep(1)
        driver.find_element(By.NAME, 'password1').send_keys('@Password123')
        time.sleep(1)
        driver.find_element(By.NAME, 'password2').send_keys('@Password123')
        time.sleep(1)

        self.upload_file(driver, 'business_registration_certificate',
                         'Financial_Statement.pdf')
        self.upload_file(driver, 'tax_identification_number',
                         'Financial_Statement.pdf')
        self.upload_file(driver, 'proof_of_address', 'Financial_Statement.pdf')
        self.upload_file(driver, 'financial_statements',
                         'Financial_Statement.pdf')
        self.upload_file(driver, 'ownership_documents',
                         'Financial_Statement.pdf')
        self.upload_file(driver, 'director_identification',
                         'Financial_Statement.pdf')
        self.upload_file(driver, 'licenses_and_permits',
                         'Financial_Statement.pdf')
        self.upload_file(driver, 'bank_account_details',
                         'Financial_Statement.pdf')

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
            "Test Passed: Business registration completed successfully and is pending admin approval.")

    def upload_file(self, driver, field_name, file_name):
        """Helper function to upload a file to a form field."""
        file_input = driver.find_element(By.NAME, field_name)
        self.assertIsNotNone(file_input,
                             f"{field_name} upload field not found!")
        file_path = os.path.abspath(f'b2d/end-to-end/{file_name}')
        file_input.send_keys(file_path)
        time.sleep(1)

    def tearDown(self):
        """Clear out business in the database and remove S3 file after each test."""
        test_business = Business.objects.last()
        self.clear_business_details(user_id=test_business.id)
        self.clear_s3_storage(user_id=test_business.id)
        self.driver.quit()

    def clear_business_details(self, user_id):
        """Delete the business record from the database for the specified user ID."""
        try:
            business = Business.objects.get(id=user_id)
            business.delete()
            print(
                f"Business record with user ID {user_id} deleted from the database.")
        except Business.DoesNotExist:
            print(f"No business found for user ID {user_id}.")

    def clear_s3_storage(self, user_id):
        """Clear the S3 bucket for the given user ID."""
        s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_S3_REGION_NAME)
        prefix = f'business_docs/{user_id}/'
        try:
            s3.delete_objects(Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                              Delete={
                                  'Objects': [{'Key': obj['Key']} for obj in
                                              s3.list_objects_v2(
                                                  Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                                                  Prefix=prefix).get(
                                                  'Contents', [])]})
        except ClientError:
            print("Specified path does not existed.")

        print(f"All files in {prefix} cleared from S3.")


if __name__ == '__main__':
    unittest.main()
