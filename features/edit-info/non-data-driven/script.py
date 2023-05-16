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
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "utils"))
from rich_unittest import RichTestRunner
from logger import Logger

# Set up the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(10)

# Open the page
LOGIN_URL = "https://sandbox.moodledemo.net/login/index.php"
FEATURE_URL = "https://sandbox.moodledemo.net/user/edit.php?id=4&returnto=profile"
USERNAME = "student"
PASSWORD = "sandbox"
DELAY = 1
LONG_DELAY = 2

driver.get(LOGIN_URL)
# time.sleep(5)

# Log in
username = driver.find_element(By.ID, "username")
username.send_keys(USERNAME)

password = driver.find_element(By.ID, "password")
password.send_keys(PASSWORD)

login = driver.find_element(By.ID, "loginbtn")
login.click()

class TestHelper():    
    @staticmethod
    def performActions(ctx, firstNameValue: str, lastNameValue: str, emailValue: str):
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

# [Use Case 1/Module3] DecisionTable Technique
class TestEditInfo(unittest.TestCase):
    def testcase_1(self):
        """Testcase 1: empty firstNameField + empty emailField"""
        TestHelper.performActions(
            self,
            "",
            "Dang Quang",
            "",
        )
        errorFirstName = driver.find_element(By.ID, "id_error_firstname")
        errorEmail = driver.find_element(By.ID, "id_error_email")
        self.assertTrue(errorFirstName.is_displayed() and (errorEmail.text == "- Required"))

    def testcase_2(self):
        """Testcase 2: empty firstNameField + invalid emailField"""
        TestHelper.performActions(
            self,
            "",
            "Dang Quang",
            "email",
        )
        errorFirstName = driver.find_element(By.ID, "id_error_firstname")
        self.assertTrue(errorFirstName.is_displayed())

    def testcase_3(self):
        """Testcase 3: valid firstNameField + valid emailField"""
        TestHelper.performActions(
            self,
            "Thanh",
            "Dang Quang",
            "thanh.dangquang@hcmut.edu.vn",
        )
        self.assertTrue(str(driver.current_url) == "https://sandbox.moodledemo.net/user/edit.php")

    def testcase_4(self):
        """Testcase 4: empty firstNameField + valid emailField"""
        TestHelper.performActions(
            self,
            "",
            "Dang Quang",
            "thanh.dangquang@hcmut.edu.vn",
        )
        errorFirstName = driver.find_element(By.ID, "id_error_firstname")
        self.assertTrue(errorFirstName.is_displayed())

    def testcase_5(self):
        """Testcase 5: valid firstNameField + empty emailField"""
        TestHelper.performActions(
            self,
            "Thanh",
            "Dang Quang",
            "",
        )
        errorEmail = driver.find_element(By.ID, "id_error_email")
        self.assertTrue((errorEmail.text == "- Required"))

    def testcase_6(self):
        """Testcase 6: valid firstNameField + invalid emailField"""
        TestHelper.performActions(
            self,
            "Thanh",
            "Dang Quang",
            "invalidEmail",
        )
        errorEmail = driver.find_element(By.ID, "id_error_email")
        self.assertTrue((errorEmail.text == "Invalid email address"))

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEditInfo)
    RichTestRunner().run(suite)

        





