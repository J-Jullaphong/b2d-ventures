import time
import unittest
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

from mysite.wsgi import *
from ..models import Business
from django_otp.plugins.otp_email.models import EmailDevice


class TestBusinessDetails(unittest.TestCase):
    """Test Case B2D_008: Test the process of adding business details as a business owner."""

    def setUp(self):
        """Setup the browser and login before each test."""
        options = Options()
        options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('http://localhost:8000/login/')
        self.device = EmailDevice.objects.get(user_id='1711e45a-9af8-4740-ab4d-75dc1b437b57')
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
        password_input.send_keys('Hb!47xGk9$Hb!47xGk9$')
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

    def test_add_business_details(self):
        """Test adding business details as a business owner."""
        driver = self.driver

        user_menu = driver.find_element(By.ID, 'dropdownUser')
        user_menu.click()
        time.sleep(1)

        profile_link = driver.find_element(By.XPATH,
                                           '//*[@id="navbarContent"]/ul[2]/li/ul/li[1]/a')
        profile_link.click()
        time.sleep(3)

        business_name = driver.find_element(By.NAME, 'businessName')
        business_name.clear()
        business_name.send_keys('HealthBiz')
        time.sleep(1)

        business_description = driver.find_element(By.NAME,
                                                   'businessDescription')
        business_description.clear()
        business_description.send_keys('Provide Health')
        time.sleep(1)

        category_dropdown = driver.find_element(By.XPATH, '/html/body/div/form/div[1]/div[3]/div/div[2]/span/span[1]/span/span/input')
        category_dropdown.send_keys('Healthcare')
        category_dropdown.send_keys(Keys.RETURN)
        time.sleep(1)

        business_photos = driver.find_element(By.NAME, 'photo1')
        business_photos.send_keys(
            f'{os.path.abspath(os.getcwd())}/b2d/end-to-end/transaction_slip.png')
        time.sleep(1)

        youtube_url = driver.find_element(By.NAME, 'videoEmbed')
        youtube_url.clear()
        youtube_url.send_keys('https://youtu.be/dQw4w9WgXcQ?feature=shared')
        time.sleep(1)

        pitch_problem = driver.find_element(By.XPATH,
                                            '//*[@id="pitchingSection"]/div[2]/div[1]/div[2]/input')
        pitch_problem.clear()
        pitch_problem.send_keys('Problem')
        time.sleep(1)

        pitch_problem_detail = driver.find_element(By.XPATH,
                                                   '//*[@id="pitchingSection"]/div[2]/div[2]/div[2]/textarea')
        pitch_problem_detail.clear()
        pitch_problem_detail.send_keys('This is the problem.')
        time.sleep(1)

        add_pitch_button = driver.find_element(By.ID, 'addPitch')
        add_pitch_button.click()
        time.sleep(1)

        pitch_solution = driver.find_element(By.XPATH,
                                             '//*[@id="pitchingSection"]/div[3]/div[1]/div[2]/input')
        pitch_solution.clear()
        pitch_solution.send_keys('Solution')
        time.sleep(1)

        pitch_solution_detail = driver.find_element(By.XPATH,
                                                    '//*[@id="pitchingSection"]/div[3]/div[2]/div[2]/textarea')
        pitch_solution_detail.clear()
        pitch_solution_detail.send_keys('This is the solution.')
        time.sleep(1)

        team_member_name = driver.find_element(By.XPATH,
                                               '//*[@id="teamSection"]/div[2]/div[1]/div[2]/input')
        team_member_name.clear()
        team_member_name.send_keys('John')
        time.sleep(1)

        team_member_role = driver.find_element(By.XPATH,
                                               '//*[@id="teamSection"]/div[2]/div[2]/div[2]/input')
        team_member_role.clear()
        team_member_role.send_keys('CEO')
        time.sleep(1)

        team_member_photo = driver.find_element(By.XPATH,
                                                '//*[@id="teamSection"]/div[2]/div[3]/div[2]/input')
        team_member_photo.send_keys(
            f'{os.path.abspath(os.getcwd())}/b2d/end-to-end/transaction_slip.png')
        time.sleep(1)

        terms_checkbox = driver.find_element(By.XPATH, '//*[@id="agreement"]')
        terms_checkbox.click()
        time.sleep(1)

        save_button = driver.find_element(By.ID, 'submitButton')
        save_button.click()
        time.sleep(3)

        self.verify_business_details()

        print(
            "Test Passed: Business details successfully submitted and saved.")

    def verify_business_details(self):
        """Verify that the business details are correctly displayed after submission."""
        driver = self.driver

        business_name_displayed = driver.find_element(By.NAME,
                                                      'businessName').get_attribute(
            'value')
        self.assertEqual(business_name_displayed, 'HealthBiz',
                         "Business name does not match!")

        business_description_displayed = driver.find_element(By.NAME,
                                                             'businessDescription').get_attribute(
            'value')
        self.assertEqual(business_description_displayed, 'Provide Health',
                         "Business description does not match!")

        selected_category = Select(
            driver.find_element(By.ID, 'category')).first_selected_option.text
        self.assertEqual(selected_category, 'Healthcare',
                         "Category does not match!")

        youtube_url_displayed = driver.find_element(By.NAME,
                                                    'videoEmbed').get_attribute(
            'value')
        self.assertEqual(youtube_url_displayed,
                         'https://youtu.be/dQw4w9WgXcQ?feature=shared',
                         "YouTube URL does not match!")

        pitch_problem_displayed = driver.find_element(By.NAME,
                                                      'topic_0').get_attribute(
            'value')
        self.assertEqual(pitch_problem_displayed, 'Problem',
                         "Pitch problem does not match!")

        pitch_problem_detail_displayed = driver.find_element(By.NAME,
                                                             'details_0').text
        self.assertEqual(pitch_problem_detail_displayed,
                         'This is the problem.',
                         "Pitch problem detail does not match!")

        pitch_solution_displayed = driver.find_element(By.NAME,
                                                       'topic_1').get_attribute(
            'value')
        self.assertEqual(pitch_solution_displayed, 'Solution',
                         "Pitch solution does not match!")

        pitch_solution_detail_displayed = driver.find_element(By.NAME,
                                                              'details_1').text
        self.assertEqual(pitch_solution_detail_displayed,
                         'This is the solution.',
                         "Pitch solution detail does not match!")

        team_member_name_displayed = driver.find_element(By.NAME,
                                                         'memberName_0').get_attribute(
            'value')
        self.assertEqual(team_member_name_displayed, 'John',
                         "Team member name does not match!")

        team_member_role_displayed = driver.find_element(By.NAME,
                                                         'workAs_0').get_attribute(
            'value')
        self.assertEqual(team_member_role_displayed, 'CEO',
                         "Team member role does not match!")

    def tearDown(self):
        """Clear out business details in the database and remove S3 files after each test."""
        self.clear_business_details(user_id='1711e45a-9af8-4740-ab4d-75dc1b437b57')
        self.clear_s3_storage(user_id='1711e45a-9af8-4740-ab4d-75dc1b437b57')
        self.driver.quit()

    def clear_business_details(self, user_id):
        """Clear business details (description and category) in the database."""
        try:
            business = Business.objects.get(id=user_id)
            business.description = ''
            business_category = business.category.first()
            business.category.remove(business_category)
            business.save()
            print(
                f"Business details for user {user_id} cleared from the database.")
        except Business.DoesNotExist:
            print(f"No business found for user {user_id}.")

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
