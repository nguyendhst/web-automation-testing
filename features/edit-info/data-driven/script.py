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

# Set up the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(10)

# Open the page
LOGIN_URL = "https://sandbox.moodledemo.net/login/index.php"
FEATURE_URL = "https://sandbox.moodledemo.net/user/edit.php?id=4&returnto=profile"
USERNAME = "student"
PASSWORD = "sandbox"
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "dataset.csv"))
SHORT_DELAY = 0.4
DELAY = 1
LONG_DELAY = 2
TIME_OUT = 10

driver.get(LOGIN_URL)
time.sleep(DELAY)
# Log in
username = driver.find_element(By.ID, "username")
username.send_keys(USERNAME)

password = driver.find_element(By.ID, "password")
password.send_keys(PASSWORD)

login = driver.find_element(By.ID, "loginbtn")
login.click()

class TestHelper():    
    @staticmethod
    def performActions(ctx, firstNameValue: str, lastNameValue: str, emailValue: str, expected: str):
        # navigate to moodle page
        driver.get(FEATURE_URL)

        # wait until moodle page is fully loaded
        driver.implicitly_wait(LONG_DELAY)

        #email is requested a change -> cancel request
        try: 
            cancelEmail = driver.find_element(By.LINK_TEXT, "Cancel email change")
            cancelEmail.click()
            driver.implicitly_wait(LONG_DELAY)
        except Exception:
                pass

        # clear first name field and last name field     
        firstNameField = driver.find_element(By.ID,"id_firstname")
        firstNameField.clear()
        lastNameField = driver.find_element(By.ID,"id_lastname")
        lastNameField.clear()
        emailField = driver.find_element(By.ID,"id_email")
        emailField.clear()

        # Input first name, last name and email value
        action = ActionChains(driver)\
            .click(firstNameField)\
            .send_keys(firstNameValue)\
            .click(lastNameField)\
            .send_keys(lastNameValue)\
            .click(emailField)\
            .send_keys(emailValue)\
            .pause(DELAY)

        #submit form
        submitBtn = driver.find_element(By.ID, "id_submitbutton")
        action.click(submitBtn)

        action.perform()
        action.reset_actions()

        result = '...'

        try:
            errorFirstName = driver.find_element(By.ID, "id_error_firstname")
            result = "failure"
        except:
            result = "success"
        finally: pass

        try:
            ctx.assertEqual(result, expected)
            logger.log(
                f"Test passed: Got: {result}, Expected: {expected}", "info"
            )
        except AssertionError:
            logger.log(
                f"Test failed: Got: {result}, Expected: {expected}", "error"
            )
        finally: pass


class TestEditInfo(unittest.TestCase):
    def test(self):
        with open(DATA_PATH, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                try:
                    TestHelper.performActions(self, row[0], row[1], row[2], row[3])
                finally: continue
        

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEditInfo)
    RichTestRunner().run(suite)