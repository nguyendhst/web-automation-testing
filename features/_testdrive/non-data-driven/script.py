
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

# Open the page
LOGIN_URL = "https://sandbox.moodledemo.net/login/index.php"
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

class TestDrive(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.driver = driver
        cls.logger = Logger()
    
    def test_drive(self):

        self.assertTrue("Available courses" in driver.page_source)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDrive)
    RichTestRunner().run(suite)
