import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from webdriver_manager.chrome import ChromeDriverManager

from rich.panel import Panel
from rich import print

import unittest
import sys
import os
import csv

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "utils"))
from rich_unittest import RichTestRunner
from logger import Logger


# Set preferred log level: DEBUG, INFO, WARNING, ERROR, CRITICAL

LOG_LV = "INFO"
logger = Logger(LOG_LV)

# Open the page
LOGIN_URL = "https://sandbox.moodledemo.net/login/index.php"
FEATURE_URL = "https://sandbox.moodledemo.net/admin/settings.php?section=taskprocessing"
USERNAME = "admin"
PASSWORD = "sandbox"
DATA_PATH = os.path.join(os.path.dirname(__file__), "data.csv")


# END OF TEMPLATE -- CREATE YOUR OWN CLASS
class TestDrive(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """setUpClass runs once per class.
        This is where you set up the driver and log in
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

    def setUp(self):
        """setUp runs before each test case run.
        This is where you set up any data needed for the tests.
        """
        time.sleep(2)

        # iterate through the data
        # self.test_data = next(self.test_data_reader)
        # self.username = self.test_data[0]
        # self.password = self.test_data[1]

    def fill_in_form_keepAlive(self, value, unit="minutes"):
        """Fill in the form for keep alive.
        - Text field id=id_s__cron_keepalivev
        - Selector id=id_s__cron_keepaliveu
        """

        # Get the text field
        keepAlive = self.driver.find_element(By.ID, "id_s__cron_keepalivev")
        keepAlive.clear()
        keepAlive.send_keys(value)

        # Get the selector
        keepAliveUnit = Select(self.driver.find_element(By.ID, "id_s__cron_keepaliveu"))
        keepAliveUnit.select_by_visible_text(unit)

    def fill_in_form_scheduledConcurrencyLimit(self, value):
        """Fill in the form for scheduled concurrency limit.
        - id=id_s__task_scheduled_concurrency_limit
        """

        # Get the text field
        concurrencyLimit = self.driver.find_element(
            By.ID, "id_s__task_scheduled_concurrency_limit"
        )
        concurrencyLimit.clear()
        concurrencyLimit.send_keys(value)

    def fill_in_form_scheduledTaskLifetime(self, value, unit="minutes"):
        """Fill in the form for scheduled task lifetime.
        - Text field id=id_s__task_scheduled_max_runtimev
        - Selector id=id_s__task_scheduled_max_runtimeu
        """

        # Get the text field
        taskLifetime = self.driver.find_element(
            By.ID, "id_s__task_scheduled_max_runtimev"
        )
        taskLifetime.clear()
        taskLifetime.send_keys(value)

        # Get the selector
        taskLifetimeUnit = Select(
            self.driver.find_element(By.ID, "id_s__task_scheduled_max_runtimeu")
        )
        taskLifetimeUnit.select_by_visible_text(unit)

    def fill_in_form_scheduledAdhocConcurrencyLimit(self, value):
        """Fill in the form for scheduled adhoc concurrency limit.
        - id=id_s__task_adhoc_concurrency_limit
        """

        # Get the text field
        concurrencyLimit = self.driver.find_element(
            By.ID, "id_s__task_adhoc_concurrency_limit"
        )
        concurrencyLimit.clear()
        concurrencyLimit.send_keys(value)

    def fill_in_form_scheduledAdhocTaskLifetime(self, value, unit="minutes"):
        """Fill in the form for scheduled adhoc task lifetime.
        - Text field id=id_s__task_adhoc_max_runtimev
        - Selector id=id_s__task_adhoc_max_runtimeu
        """

        # Get the text field
        taskLifetime = self.driver.find_element(By.ID, "id_s__task_adhoc_max_runtimev")
        taskLifetime.clear()
        taskLifetime.send_keys(value)

        # Get the selector
        taskLifetimeUnit = Select(
            self.driver.find_element(By.ID, "id_s__task_adhoc_max_runtimeu")
        )
        taskLifetimeUnit.select_by_visible_text(unit)

    def submit_form(self):
        """Submit the form.
        - xpath=//button[contains(.,'Save changes')]
        """
        btn = self.driver.find_element(By.XPATH, "//button[contains(.,'Save changes')]")
        self.driver.execute_script("arguments[0].click();", btn)

    # TEST CASES
    def test_drive(self):
        with open(DATA_PATH, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                # cron_keepalive,task_scheduled_concurrency_limit,task_scheduled_max_runtime,task_adhoc_concurrency_limit,task_adhoc_max_runtime
                self.logger.log(
                    f"Testing: {row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}", "info"
                )
                self.cron_keepalive = row[0]
                self.task_scheduled_concurrency_limit = row[1]
                self.task_scheduled_max_runtime = row[2]
                self.task_adhoc_concurrency_limit = row[3]
                self.task_adhoc_max_runtime = row[4]
                self.expected = row[5]

                self.driver.get(FEATURE_URL)

                # Fill in the form
                #self.fill_in_form_keepAlive(self.cron_keepalive, "seconds")
                self.fill_in_form_scheduledConcurrencyLimit(
                    self.task_scheduled_concurrency_limit
                )
                self.fill_in_form_scheduledTaskLifetime(
                    self.task_scheduled_max_runtime, "seconds"
                )
                self.fill_in_form_scheduledAdhocConcurrencyLimit(
                    self.task_adhoc_concurrency_limit
                )
                self.fill_in_form_scheduledAdhocTaskLifetime(
                    self.task_adhoc_max_runtime, "seconds"
                )

                # Submit the form
                self.submit_form()

                # Check if the result is as expected
                xpath_successfully_changed = """//div[contains(@class, "alert-success") and contains(text(), "Changes saved")]"""
                xpath_error = """//div[contains(@class, "alert-danger")]"""

                try:
                    self.driver.find_element(By.XPATH, xpath_successfully_changed)
                    self.result = "success"
                except NoSuchElementException:
                    try:
                        self.driver.find_element(By.XPATH, xpath_error)
                        self.result = "failure"
                    except NoSuchElementException:
                        self.result = "Unknown"

                try:
                    self.assertEqual(self.result, self.expected)
                    self.logger.log(
                        f"Test passed: Got: {self.result}, Expected: {self.expected}", "info"
                    )
                except AssertionError:
                    self.logger.log(
                        f"Test failed: Got: {self.result}, Expected: {self.expected}", "error"
                    )
                finally:
                    continue


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDrive)
    RichTestRunner().run(suite)
