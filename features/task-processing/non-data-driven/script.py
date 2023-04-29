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
FEATURE_URL = "https://sandbox.moodledemo.net/admin/settings.php?section=taskprocessing"
USERNAME = "admin"
PASSWORD = "sandbox"


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

    def setUp(self):
        """setUp runs before every test case.
        This is where you set up any data needed for the tests.
        """
        self.driver.get(FEATURE_URL)
        time.sleep(1)

    def checkCron(self, on=True):
        """checkCron checks if cron is enabled or disabled.
        - id=id_s__cron_enabled
        """
        self.driver.get(FEATURE_URL)
        cron = self.driver.find_element(By.ID, "id_s__cron_enabled")
        if on:
            if not cron.is_selected():
                cron.click()
        else:
            if cron.is_selected():
                cron.click()

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

    def test_normal_flow(self):
        """Test normal flow.
        1. Enable cron
        2. Set keep alive to 5 minutes
        3. Set scheduled concurrency limit to 5
        4. Set scheduled task lifetime to 5 minutes
        5. Set scheduled adhoc concurrency limit to 5
        6. Set scheduled adhoc task lifetime to 5 minutes
        7. Save changes
        8. Check if changes are saved
        """
        self.logger.log("Test normal flow", "info")
        self.checkCron()
        self.fill_in_form_keepAlive(5)
        self.fill_in_form_scheduledConcurrencyLimit(5)
        self.fill_in_form_scheduledTaskLifetime(5)
        self.fill_in_form_scheduledAdhocConcurrencyLimit(5)
        self.fill_in_form_scheduledAdhocTaskLifetime(5)
        self.submit_form()

        time.sleep(1)

        xpath_expected = """//div[contains(@class, "alert-success") and contains(text(), "Changes saved")]"""
        xpath_failed = """//div[contains(@class, "alert-danger")]"""

        try:
            success = self.driver.find_element(By.XPATH, xpath_expected)
        except Exception:
            
            try:
                failed = self.driver.find_element(By.XPATH, xpath_failed)
            except Exception:
                self.assertTrue(False, "No alert found")
            else:
                if failed:
                    self.fail("Changes not saved")

        self.assertTrue(success)

    def test_invalid_keepAlive1(self):
        """Test invalid keep alive field.
        1. Enable cron
        2. Set keep alive to -1 minutes
        3. All other fields are valid
        4. Save changes
        5. Check if changes are saved
        """

        self.logger.log("Test invalid keep alive field", "info")
        self.checkCron()
        self.fill_in_form_keepAlive(-1)
        self.fill_in_form_scheduledConcurrencyLimit(5)
        self.fill_in_form_scheduledTaskLifetime(5)
        self.fill_in_form_scheduledAdhocConcurrencyLimit(5)
        self.fill_in_form_scheduledAdhocTaskLifetime(5)
        self.submit_form()

        time.sleep(1)

        xpath = """//div[contains(@class, "alert-danger") and contains(text(), "Some settings were not changed due to an error")]"""
        xpath_failed = """//div[contains(@class, "alert-success") and contains(text(), "Changes saved")]"""

        try:
            success = self.driver.find_element(By.XPATH, xpath)
        except Exception:
            try:
                failed = self.driver.find_element(By.XPATH, xpath_failed)
            except Exception:
                failed = None

            if failed:
                success = False

            else:
                self.fail("No error message displayed")

        self.assertTrue(success)

    def test_invalid_keepAlive2(self):
        """Test invalid keep alive field.
        1. Enable cron
        2. Set keep alive to non-numeric value
        3. All other fields are valid
        4. Save changes
        5. Check if changes are saved
        """

        self.logger.log("Test invalid keep alive field", "info")
        self.checkCron()
        self.fill_in_form_keepAlive("abc")
        self.fill_in_form_scheduledConcurrencyLimit(5)
        self.fill_in_form_scheduledTaskLifetime(5)
        self.fill_in_form_scheduledAdhocConcurrencyLimit(5)
        self.fill_in_form_scheduledAdhocTaskLifetime(5)
        self.submit_form()

        time.sleep(1)

        xpath = """//div[contains(@class, "alert-danger") and contains(text(), "Some settings were not changed due to an error.")]"""

        xpath_failed = """//div[contains(@class, "alert-success") and contains(text(), "Changes saved")]"""

        try:
            success = self.driver.find_element(By.XPATH, xpath)
        except Exception:
            try:
                failed = self.driver.find_element(By.XPATH, xpath_failed)
            except Exception:
                failed = None

            if failed:
                success = False

            else:
                self.fail("No error message displayed")

        self.assertTrue(success)

    def test_invalid_scheduledConcurrencyLimit1(self):
        """Test invalid scheduled concurrency limit field.
        1. Enable cron
        2. Set scheduled concurrency limit to -1
        3. All other fields are valid
        4. Save changes
        5. Check if changes are saved
        """

        self.logger.log("Test invalid scheduled concurrency limit field", "info")
        self.checkCron()
        self.fill_in_form_keepAlive(5)
        self.fill_in_form_scheduledConcurrencyLimit(-1)
        self.fill_in_form_scheduledTaskLifetime(5)
        self.fill_in_form_scheduledAdhocConcurrencyLimit(5)
        self.fill_in_form_scheduledAdhocTaskLifetime(5)
        self.submit_form()

        time.sleep(1)

        xpath = """//div[contains(@class, "alert-danger") and contains(text(), "Some settings were not changed due to an error")]"""
        xpath_failed = """//div[contains(@class, "alert-success") and contains(text(), "Changes saved")]"""

        try:
            success = self.driver.find_element(By.XPATH, xpath)
        except Exception:
            try:
                failed = self.driver.find_element(By.XPATH, xpath_failed)
            except Exception:
                failed = None

            if failed:
                success = False

            else:
                self.fail("No error message displayed")
        self.assertTrue(success)

    def test_invalid_scheduledConcurrencyLimit2(self):
        """Test invalid scheduled concurrency limit field.
        1. Enable cron
        2. Set scheduled concurrency limit to non-numeric value
        3. All other fields are valid
        4. Save changes
        5. Check if changes are saved
        """

        self.logger.log("Test invalid scheduled concurrency limit field", "info")
        self.checkCron()
        self.fill_in_form_keepAlive(5)
        self.fill_in_form_scheduledConcurrencyLimit("abc")
        self.fill_in_form_scheduledTaskLifetime(5)
        self.fill_in_form_scheduledAdhocConcurrencyLimit(5)
        self.fill_in_form_scheduledAdhocTaskLifetime(5)
        self.submit_form()

        time.sleep(1)

        xpath = """//div[contains(@class, "alert-danger") and contains(text(), "Some settings were not changed due to an error")]"""
        xpath_failed = """//div[contains(@class, "alert-success") and contains(text(), "Changes saved")]"""

        try:
            success = self.driver.find_element(By.XPATH, xpath)
        except Exception:
            try:
                failed = self.driver.find_element(By.XPATH, xpath_failed)
            except Exception:
                failed = None

            if failed:
                success = False

            else:
                self.fail("No error message displayed")
        self.assertTrue(success)

    def test_invalid_scheduledTaskLifetime1(self):
        """Test invalid scheduled task lifetime field.
        1. Enable cron
        2. Set scheduled task lifetime to -1
        3. All other fields are valid
        4. Save changes
        5. Check if changes are saved
        """

        self.logger.log("Test invalid scheduled task lifetime field", "info")
        self.checkCron()
        self.fill_in_form_keepAlive(5)
        self.fill_in_form_scheduledConcurrencyLimit(5)
        self.fill_in_form_scheduledTaskLifetime(-1)
        self.fill_in_form_scheduledAdhocConcurrencyLimit(5)
        self.fill_in_form_scheduledAdhocTaskLifetime(5)
        self.submit_form()

        time.sleep(1)

        xpath = """//div[contains(@class, "alert-danger") and contains(text(), "Some settings were not changed due to an error")]"""
        xpath_failed = """//div[contains(@class, "alert-success") and contains(text(), "Changes saved")]"""

        try:
            success = self.driver.find_element(By.XPATH, xpath)
        except Exception:
            try:
                failed = self.driver.find_element(By.XPATH, xpath_failed)
            except Exception:
                failed = None

            if failed:
                success = False

            else:
                self.fail("No error message displayed")
        self.assertTrue(success)

    def test_invalid_scheduledTaskLifetime2(self):
        """Test invalid scheduled task lifetime field.
        1. Enable cron
        2. Set scheduled task lifetime to non-numeric value
        3. All other fields are valid
        4. Save changes
        5. Check if changes are saved
        """

        self.logger.log("Test invalid scheduled task lifetime field", "info")
        self.checkCron()
        self.fill_in_form_keepAlive(5)
        self.fill_in_form_scheduledConcurrencyLimit(5)
        self.fill_in_form_scheduledTaskLifetime("abc")
        self.fill_in_form_scheduledAdhocConcurrencyLimit(5)
        self.fill_in_form_scheduledAdhocTaskLifetime(5)
        self.submit_form()

        time.sleep(1)

        xpath = """//div[contains(@class, "alert-danger") and contains(text(), "Some settings were not changed due to an error")]"""
        xpath_failed = """//div[contains(@class, "alert-success") and contains(text(), "Changes saved")]"""

        try:
            success = self.driver.find_element(By.XPATH, xpath)
        except Exception:
            try:
                failed = self.driver.find_element(By.XPATH, xpath_failed)
            except Exception:
                failed = None

            if failed:
                success = False

            else:
                self.fail("No error message displayed")
        self.assertTrue(success)

    def test_invalid_scheduledAdhocConcurrencyLimit1(self):
        """Test invalid scheduled adhoc concurrency limit field.
        1. Enable cron
        2. Set scheduled adhoc concurrency limit to -1
        3. All other fields are valid
        4. Save changes
        5. Check if changes are saved
        """

        self.logger.log("Test invalid scheduled adhoc concurrency limit field", "info")
        self.checkCron()
        self.fill_in_form_keepAlive(5)
        self.fill_in_form_scheduledConcurrencyLimit(5)
        self.fill_in_form_scheduledTaskLifetime(5)
        self.fill_in_form_scheduledAdhocConcurrencyLimit(-1)
        self.fill_in_form_scheduledAdhocTaskLifetime(5)
        self.submit_form()

        time.sleep(1)

        xpath = """//div[contains(@class, "alert-danger") and contains(text(), "Invalid scheduled adhoc concurrency limit value")]"""
        xpath_failed = """//div[contains(@class, "alert-success") and contains(text(), "Changes saved")]"""

        try:
            success = self.driver.find_element(By.XPATH, xpath)
        except Exception:
            try:
                failed = self.driver.find_element(By.XPATH, xpath_failed)
            except Exception:
                failed = None

            if failed:
                success = False

            else:
                self.fail("No error message displayed")
        self.assertTrue(success)

    def test_invalid_scheduledAdhocConcurrencyLimit2(self):
        """Test invalid scheduled adhoc concurrency limit field.
        1. Enable cron
        2. Set scheduled adhoc concurrency limit to non-numeric value
        3. All other fields are valid
        4. Save changes
        5. Check if changes are saved
        """

        self.logger.log("Test invalid scheduled adhoc concurrency limit field", "info")
        self.checkCron()
        self.fill_in_form_keepAlive(5)
        self.fill_in_form_scheduledConcurrencyLimit(5)
        self.fill_in_form_scheduledTaskLifetime(5)
        self.fill_in_form_scheduledAdhocConcurrencyLimit("abc")
        self.fill_in_form_scheduledAdhocTaskLifetime(5)
        self.submit_form()

        time.sleep(1)

        xpath = """//div[contains(@class, "alert-danger") and contains(text(), "Some settings were not changed due to an error")]"""
        xpath_failed = """//div[contains(@class, "alert-success") and contains(text(), "Changes saved")]"""

        try:
            success = self.driver.find_element(By.XPATH, xpath)
        except Exception:
            try:
                failed = self.driver.find_element(By.XPATH, xpath_failed)
            except Exception:
                failed = None

            if failed:
                success = False

            else:
                self.fail("No error message displayed")
        self.assertTrue(success)

    def test_invalid_scheduledAdhocTaskLifetime1(self):
        """Test invalid scheduled adhoc task lifetime field.
        1. Enable cron
        2. Set scheduled adhoc task lifetime to -1
        3. All other fields are valid
        4. Save changes
        5. Check if changes are saved
        """

        self.logger.log("Test invalid scheduled adhoc task lifetime field", "info")
        self.checkCron()
        self.fill_in_form_keepAlive(5)
        self.fill_in_form_scheduledConcurrencyLimit(5)
        self.fill_in_form_scheduledTaskLifetime(5)
        self.fill_in_form_scheduledAdhocConcurrencyLimit(5)
        self.fill_in_form_scheduledAdhocTaskLifetime(-1)
        self.submit_form()

        time.sleep(1)

        xpath = """//div[contains(@class, "alert-danger") and contains(text(), "Some settings were not changed due to an error")]"""
        xpath_failed = """//div[contains(@class, "alert-success") and contains(text(), "Changes saved")]"""

        try:
            success = self.driver.find_element(By.XPATH, xpath)
        except Exception:
            try:
                failed = self.driver.find_element(By.XPATH, xpath_failed)
            except Exception:
                failed = None

            if failed:
                success = False

            else:
                self.fail("No error message displayed")
        self.assertTrue(success)

    def test_invalid_scheduledAdhocTaskLifetime2(self):
        """Test invalid scheduled adhoc task lifetime field.
        1. Enable cron
        2. Set scheduled adhoc task lifetime to non-numeric value
        3. All other fields are valid
        4. Save changes
        5. Check if changes are saved
        """

        self.logger.log("Test invalid scheduled adhoc task lifetime field", "info")
        self.checkCron()
        self.fill_in_form_keepAlive(5)
        self.fill_in_form_scheduledConcurrencyLimit(5)
        self.fill_in_form_scheduledTaskLifetime(5)
        self.fill_in_form_scheduledAdhocConcurrencyLimit(5)
        self.fill_in_form_scheduledAdhocTaskLifetime("abc")
        self.submit_form()

        time.sleep(1)

        xpath = """//div[contains(@class, "alert-danger") and contains(text(), "Some settings were not changed due to an error")]"""
        xpath_failed = """//div[contains(@class, "alert-success") and contains(text(), "Changes saved")]"""

        try:
            success = self.driver.find_element(By.XPATH, xpath)
        except Exception:
            try:
                failed = self.driver.find_element(By.XPATH, xpath_failed)
            except Exception:
                failed = None

            if failed:
                success = False

            else:
                self.fail("No error message displayed")
        self.assertTrue(success)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalendarImport)
    RichTestRunner().run(suite)


# function getElementByXpath(path) {
#  return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
# }
