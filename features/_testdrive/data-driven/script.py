import time
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
import csv

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "utils"))
from rich_unittest import RichTestRunner
from logger import Logger


# Set preferred log level: DEBUG, INFO, WARNING, ERROR, CRITICAL

LOG_LV = "INFO"
logger = Logger(LOG_LV)

# Open the page
LOGIN_URL = "https://sandbox.moodledemo.net/login/index.php"
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

    def setUp(self):
        """setUp runs before each test case run.
        This is where you set up any data needed for the tests.
        """
        pass

        # iterate through the data
        # self.test_data = next(self.test_data_reader)
        # self.username = self.test_data[0]
        # self.password = self.test_data[1]

    # TEST CASES
    def test_drive(self):
        with open(DATA_PATH, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                self.logger.log(f"Testing: {row[0]}, {row[1]}", "info")
                self.username = row[0]
                self.password = row[1]
                self.expected = row[2]
                self.driver.get(LOGIN_URL)

                # if encounter alreary login alert, click logout
                # xpath = "//p[contains(text(),'You are already logged in')]"
                try:
                    alert_text = self.driver.find_element(
                        By.XPATH, "//p[contains(text(),'You are already logged in')]"
                    )
                except Exception:
                    alert_text = None
    
                if alert_text and alert_text.is_displayed():
                    logout = self.driver.find_element(
                        By.XPATH, "//button[contains(text(),'Log out')]"
                    )
                    if logout:
                        logout.click()
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.ID, "username"))
                        )

                username = self.driver.find_element(By.ID, "username")
                username.clear()
                password = self.driver.find_element(By.ID, "password")
                password.clear()
                login = self.driver.find_element(By.ID, "loginbtn")

                ActionChains(self.driver).move_to_element(username).click().send_keys(
                    self.username
                ).move_to_element(password).click().send_keys(
                    self.password
                ).move_to_element(
                    login
                ).click().perform()

                time.sleep(3)

                if (
                    "Invalid login, please try again" in self.driver.page_source
                    and self.expected == "success"
                ):
                    self.fail(
                        f"Login failed when it should have succeeded: {self.username}, {self.password}"
                    )
                elif (
                    "Available courses" in self.driver.page_source
                    and self.expected == "failure"
                ):
                    self.fail(
                        f"Login succeeded when it should have failed: {self.username}, {self.password}"
                    )
                else:
                    pass


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDrive)
    RichTestRunner().run(suite)
