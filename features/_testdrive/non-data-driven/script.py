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
from logger import Logger

# Set up the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(10)

# Set preferred log level: DEBUG, INFO, WARNING, ERROR, CRITICAL

LOG_LV = "DEBUG"
logger = Logger(LOG_LV)

# Open the page
LOGIN_URL = "https://sandbox.moodledemo.net/login/index.php"
USERNAME = "admin"
PASSWORD = "sandbox"

driver.get(LOGIN_URL)

# Log in
username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")
login = driver.find_element(By.ID, "loginbtn")

ActionChains.move_to_element(username) \
    .click() \
    .send_keys(USERNAME) \
    .move_to_element(password) \
    .click() \
    .send_keys(PASSWORD) \
    .move_to_element(login) \
    .click() \
    .perform()

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


# END OF TEMPLATE -- CREATE YOUR OWN CLASS
class TestDrive(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = driver
        cls.logger = logger

    def test_drive(self):
        self.assertTrue("Available courses" in self.driver.page_source)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDrive)
    RichTestRunner().run(suite)
