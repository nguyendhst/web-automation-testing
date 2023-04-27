# Test script for the calendar import functionality

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

from rich.panel import Panel
from rich import print

import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "utils"))
from rich_unittest import RichTestRunner


# Set up the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(10)

# Open the page
LOGIN_URL = "https://sandbox.moodledemo.net/login/index.php"
FEATURE_URL = "https://sandbox.moodledemo.net/calendar/import.php"
USERNAME = "admin"
PASSWORD = "sandbox"
ICS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "calendar.ics"))

driver.get(LOGIN_URL)

# Log in
username = driver.find_element(By.ID, "username")
username.send_keys(USERNAME)

password = driver.find_element(By.ID, "password")
password.send_keys(PASSWORD)

login = driver.find_element(By.ID, "loginbtn")
login.click()

# if login failed, exit

if "Available courses" not in driver.page_source:
    driver.quit()
    LOGIN_ERR = Panel(
        f"""
    Login failed. Please check your credentials and try again.
    - username: {USERNAME}
    - password: {PASSWORD}
    """,
        title="Login Error",
        title_align="left",
        expand=True,
        style="red",
    )
    print(LOGIN_ERR)
    sys.exit(1)


class TestCalendarImport(unittest.TestCase):
    def test_calendar_import(self):
        """Simple access test for the calendar import page"""
        # Go to the calendar import page
        driver.get(FEATURE_URL)
        # Check that the page is correct
        self.assertTrue("Import calendar" in driver.page_source)

    def test_calendar_import_ical(self):
        # Go to the calendar import page
        driver.get(FEATURE_URL)
        # Check that the page is correct
        self.assertTrue("Import caledar" in driver.page_source)

    def test_calendar_valid_field1(self):
        """
        - name: Calendar Import Normal Flow
        - description: Test the calendar import .ics URL functionality with valid fields
        - preconditions: User is logged in
        """

        # Go to the calendar import page
        driver.get(FEATURE_URL)

        # Check that the page is correct
        self.assertTrue("Import calendar" in driver.page_source)

        # Check that the name field is valid
        calendar_name = driver.find_element(By.ID, "id_name")

        ActionChains(driver).move_to_element(calendar_name).click().send_keys(
            "Test Calendar"
        ).perform()

        # Check that the field is valid
        calendar_url = driver.find_element(By.ID, "id_url")
        calendar_url.send_keys(
            r"""https://www.google.com/calendar/ical/en.usa%23holiday%40group.v.calendar.google.com/public/basic.ics"""
        )

        # Import
        import_button = driver.find_element(By.ID, "id_add")
        import_button.click()

        # Check if successfully redirected to the manage calendars page
        self.assertTrue("Import or export calendars" in driver.page_source)

    def test_calendar_invalid_file(self):
        """
        - name: Calendar Import Alternative Flow 1
        - description: Test the calendar import functionality with File Picker
        - preconditions: User is logged in
        """

        # Go to the calendar import page
        driver.get(FEATURE_URL)

        # Check that the page is correct
        self.assertTrue("Import calendar" in driver.page_source)

        # Check that the name field is valid
        calendar_name = driver.find_element(By.ID, "id_name")
        calendar_name.send_keys("Test Calendar")

        # Select the file picker option
        selector = Select(driver.find_element(By.ID, "id_importfrom"))
        selector.select_by_index(1)

        ## Confirm that the file picker is visible
        # file_picker = driver.find_element(By.ID, "filepicker-wrapper")
        # self.assertTrue(file_picker.is_displayed())

        # Click the file upload button name="importfilechoose"
        file_picker_button = driver.find_element(By.NAME, "importfilechoose")
        file_picker_button.click()

        # Click the file upload option fp-repo-6447ad08ccd7e-3
        file_picker_option = driver.find_element(By.ID, "fp-repo-6447ad08ccd7e-3")
        file_picker_option.click()

        # get the input type="file"
        file_input = driver.find_element(By.XPATH, "//input[@type='file']")
        file_input.send_keys(ICS_PATH)

        # Import
        import_button = driver.find_element(By.ID, "id_add")
        import_button.click()

        # Check if successfully redirected to the manage calendars page
        self.assertTrue("Import or export calendars" in driver.page_source)

    def test_calendar_invalid_field1(self):
        """
        - name: Calendar Import Exception Flow 1
        - description: Test the calendar import functionality with Invalid URL field
        - preconditions: User is logged in
        """

        # Go to the calendar import page
        driver.get(FEATURE_URL)

        bad_url = "google.com"
        name_field = driver.find_element(By.ID, "id_name")
        url_field = driver.find_element(By.ID, "id_url")
        submit_btn = driver.find_element(By.ID, "id_add")

        ActionChains(driver).move_to_element(name_field).click().send_keys(
            "Test Calendar"
        ).move_to_element(url_field).click().send_keys(bad_url).move_to_element(
            submit_btn
        ).click().perform()

        # verify if a error prompt is shown
        self.assertTrue("Invalid URL" in driver.page_source)

    def test_calendar_invalid_field2(self):
        """
        - name: Calendar Import Exception Flow 2
        - description: Test the calendar import functionality with Invalid Name field
        - preconditions: User is logged in
        """

        # Go to the calendar import page
        driver.get(FEATURE_URL)

        name_field = driver.find_element(By.ID, "id_name")
        url_field = driver.find_element(By.ID, "id_url")
        submit_btn = driver.find_element(By.ID, "id_add")

        ActionChains(driver).move_to_element(name_field).click().send_keys(
            "Test Calendar"
        ).move_to_element(url_field).click().move_to_element(
            submit_btn
        ).click().perform()

        # verify if a error prompt is shown
        self.assertTrue("Invalid URL" in driver.page_source)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalendarImport)
    RichTestRunner().run(suite)
