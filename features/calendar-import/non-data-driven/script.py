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
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "utils"))
from rich_unittest import RichTestRunner
from logger import Logger

# Set preferred log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LV = "INFO"
logger = Logger(LOG_LV)

LOGIN_URL = "https://sandbox.moodledemo.net/login/index.php"
FEATURE_URL = "https://sandbox.moodledemo.net/calendar/import.php"
USERNAME = "admin"
PASSWORD = "sandbox"
ICS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "calendar.ics"))


class TestCalendarImport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """setUpClass runs once per script execution.
        This is where you set up the driver and log in if necessary.
        """
        # Set up the driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.implicitly_wait(10)

        cls.driver = driver
        cls.logger = logger

        # Log in
        cls.driver.get(LOGIN_URL)

        username = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")
        login = cls.driver.find_element(By.ID, "loginbtn")

        ActionChains(cls.driver).move_to_element(username).click().send_keys(
            USERNAME
        ).move_to_element(password).click().send_keys(PASSWORD).move_to_element(
            login
        ).click().perform()

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

    # def test_calendar_import(self):
    #    """Simple access test for the calendar import page"""
    #    # Go to the calendar import page
    #    self.driver.get(FEATURE_URL)
    #    # Check that the page is correct
    #    self.assertTrue("Import calendar" in self.driver.page_source)

    # def test_calendar_import_ical(self):
    #    # Go to the calendar import page
    #    self.driver.get(FEATURE_URL)
    #    # Check that the page is correct
    #    self.assertTrue("Import calendar" in self.driver.page_source)

    def test_calendar_valid_field1(self):
        """
        - name: Calendar Import Normal Flow
        - description: Test the calendar import .ics URL functionality with valid fields
        - preconditions: User is logged in
        """

        # Go to the calendar import page
        self.driver.get(FEATURE_URL)

        # Check that the page is correct
        self.assertTrue("Import calendar" in self.driver.page_source)

        # Check that the name field is valid
        calendar_name = self.driver.find_element(By.ID, "id_name")

        ActionChains(self.driver).move_to_element(calendar_name).click().send_keys(
            "Test Calendar"
        ).perform()

        # Check that the field is valid
        calendar_url = self.driver.find_element(By.ID, "id_url")
        calendar_url.send_keys(
            r"""https://www.google.com/calendar/ical/en.usa%23holiday%40group.v.calendar.google.com/public/basic.ics"""
        )

        # Import
        import_button = self.driver.find_element(By.ID, "id_add")
        import_button.click()

        # Check if successfully redirected to the manage calendars page
        self.assertTrue("Import or export calendars" in self.driver.page_source)

    def test_calendar_alt1(self):
        """
        - name: Calendar Import Alternative Flow 1
        - description: Test the calendar import functionality with File Picker
        - preconditions: User is logged in
        """
        wait = WebDriverWait(self.driver, 10)
        # Go to the calendar import page
        self.driver.get(FEATURE_URL)

        # Check that the page is correct
        self.assertTrue("Import calendar" in self.driver.page_source)

        # Check that the name field is valid
        calendar_name = self.driver.find_element(By.ID, "id_name")
        calendar_name.send_keys("Test Calendar Alt 1")

        # Select the file picker option
        selector = Select(self.driver.find_element(By.ID, "id_importfrom"))
        selector.select_by_visible_text("Calendar file (.ics)")
        btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='importfilechoose']"))
        )

        btn.click()

        # click the upload file option driver.findElement(By.xpath("//span[contains(@class,'fp-repo-name') and contains(text(), 'Upload a file')]"))
        btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(), 'Upload a file')]")
            )
        )
        btn.click()

        # wait for 5 seconds for the shitty UI to load
        time.sleep(5)

        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='repo_upload_file']"))
        )
        btn.send_keys(ICS_PATH)

        time.sleep(2)

        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='fp-upload-btn btn-primary btn']")
            )
        )
        btn.click()

        time.sleep(2)

        btn = self.driver.find_element(By.XPATH, "//input[@id='id_add']")
        self.driver.execute_script("arguments[0].click();", btn)

        time.sleep(2)

        # Check if successfully redirected to the manage calendars page: https://sandbox.moodledemo.net/calendar/managesubscriptions.php
        self.assertTrue("Imported calendars" in self.driver.page_source)

    # def test_calendar_invalid_field1(self):
    #    """
    #    - name: Calendar Import Exception Flow 1
    #    - description: Test the calendar import functionality with Invalid URL field
    #    - preconditions: User is logged in
    #    """

    #    # Go to the calendar import page
    #    self.driver.get(FEATURE_URL)

    #    bad_url = "google.com"
    #    name_field = self.driver.find_element(By.ID, "id_name")
    #    url_field = self.driver.find_element(By.ID, "id_url")
    #    submit_btn = self.driver.find_element(By.ID, "id_add")

    #    ActionChains(self.driver).move_to_element(name_field).click().send_keys(
    #        "Test Calendar"
    #    ).move_to_element(url_field).click().send_keys(bad_url).move_to_element(
    #        submit_btn
    #    ).click().perform()

    #    # verify if a error prompt is shown
    #    self.assertTrue("Invalid URL" in self.driver.page_source)

    # def test_calendar_invalid_field2(self):
    #    """
    #    - name: Calendar Import Exception Flow 2
    #    - description: Test the calendar import functionality with Invalid Name field
    #    - preconditions: User is logged in
    #    """

    #    # Go to the calendar import page
    #    self.driver.get(FEATURE_URL)

    #    name_field = self.driver.find_element(By.ID, "id_name")
    #    url_field = self.driver.find_element(By.ID, "id_url")
    #    submit_btn = self.driver.find_element(By.ID, "id_add")

    #    ActionChains(self.driver).move_to_element(name_field).click().send_keys(
    #        "Test Calendar"
    #    ).move_to_element(url_field).click().move_to_element(
    #        submit_btn
    #    ).click().perform()

    #    # verify if a error prompt is shown
    #    self.assertTrue("Invalid URL" in self.driver.page_source)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalendarImport)
    RichTestRunner().run(suite)
