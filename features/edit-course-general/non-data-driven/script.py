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

import unittest
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "utils"))
from rich_unittest import RichTestRunner


# Set up the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(10)

# Open the page
LOGIN_URL = "https://sandbox.moodledemo.net/login/index.php"
FEATURE_URL = "https://sandbox.moodledemo.net/course/edit.php?id=2"
USERNAME = "teacher"
PASSWORD = "sandbox"
DELAY = 1
LONG_DELAY = 2

driver.get(LOGIN_URL)

# Log in
username = driver.find_element(By.ID, "username")
username.send_keys(USERNAME)

password = driver.find_element(By.ID, "password")
password.send_keys(PASSWORD)

login = driver.find_element(By.ID, "loginbtn")
login.click()


class TestEditCourseGeneral(unittest.TestCase):
    def getElements(self):
        driver.get(FEATURE_URL)

        # wait until moodle page is fully loaded
        driver.implicitly_wait(LONG_DELAY)

        # clear full name field
        fullNameField = driver.find_elements(By.CSS_SELECTOR, ".form-control")[1]
        fullNameField.send_keys(Keys.CONTROL, "a")
        fullNameField.send_keys(Keys.DELETE)

        # clear short name field
        shortNameField = driver.find_elements(By.CSS_SELECTOR, ".form-control")[2]
        shortNameField.send_keys(Keys.CONTROL, "a")
        shortNameField.send_keys(Keys.DELETE)

        # clear course category field
        driver.find_element(
            By.CSS_SELECTOR, ".form-autocomplete-selection span.badge"
        ).click()

        submitBtn = driver.find_element(By.ID, "id_saveanddisplay")

        return (fullNameField, shortNameField, submitBtn)

    def performActions(self, fullName: str, shortName: str, category: bool, redirect = False):
        elements = self.getElements()

        # Input full name and short name value
        action = (
            ActionChains(driver)
            .move_to_element(elements[0])
            .click()
            .send_keys(fullName)
            .pause(DELAY)
            .move_to_element(elements[1])
            .click()
            .send_keys(shortName)
            .pause(DELAY)
        )

        # if category == True, select the first course category
        if category == True:
            category_downarrow = driver.find_element(
                By.CSS_SELECTOR, ".form-autocomplete-downarrow"
            )
            action = action.move_to_element(category_downarrow).click().pause(DELAY)

            category_selection = driver.find_elements(By.CSS_SELECTOR, ".form-control")[3]
            action = (
                action.move_to_element(category_selection)
                .click()
                .send_keys(Keys.ENTER)
                .pause(DELAY)
            )

        # submit form
        action = action.move_to_element(elements[2]).click().pause(LONG_DELAY)
        action.perform()
        
        # check if browser redirect or not
        if redirect == True:
            self.assertTrue(str(driver.current_url) == "https://sandbox.moodledemo.net/course/view.php?id=2")
        else:
            self.assertTrue(str(driver.current_url) == FEATURE_URL)
        
        action.reset_actions()

    """ C1: điều kiện Course full name (full_name_field) đã được nhập.
        C2: điều kiện Course short name (short_name_field) đã được nhập.
        C3: điều kiện Course category đã được nhập.
    """

    def test_rule_1(self):
        """C1: true, C2: true, C3: true"""
        self.performActions(
            "KIEM TRA PHAN MEM (CO3015) (CQ_HK222)",
            "KTPM (CO3015)",
            True,
            True,
        )

    def test_rule_2(self):
        """C1: true, C2: true, C3: false"""
        self.performActions(
            "KIEM TRA PHAN MEM (CO3015) (CQ_HK222)", "KTPM (CO3015)", False
        )

    def test_rule_3(self):
        """C1: true, C2: false, C3: true"""
        self.performActions("KIEM TRA PHAN MEM (CO3015) (CQ_HK222)", "", True)

    def test_rule_4(self):
        """C1: true, C2: false, C3: false"""
        self.performActions("KIEM TRA PHAN MEM (CO3015) (CQ_HK222)", "", False)

    def test_rule_5(self):
        """C1: false, C2: true, C3: true"""
        self.performActions("", "KTPM (CO3015)", True)

    def test_rule_6(self):
        """C1: false, C2: true, C3: false"""
        self.performActions("", "KTPM (CO3015)", False)

    def test_rule_7(self):
        """C1: false, C2: false, C3: true"""
        self.performActions("", "", True)

    def test_rule_8(self):
        """C1: false, C2: false, C3: false"""
        self.performActions("", "", False)
        driver.quit()


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEditCourseGeneral)
    RichTestRunner().run(suite)
