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
        # C1: điều kiện Course full name (full_name_field) đã được nhập.
        # C2: điều kiện Course short name (short_name_field) đã được nhập.
        # C3: điều kiện Course category đã được nhập.
        if hasattr(self, 'full_name_field'):
            return (self.full_name_field, self.short_name_field, self.submit_btn, self.badge_btn)
        
        driver.get(FEATURE_URL)
        self.full_name_field = driver.find_elements(By.CSS_SELECTOR, "input")[21]
        self.full_name_field.send_keys(Keys.CONTROL, 'a')
        self.full_name_field.send_keys(Keys.DELETE)
        
        self.short_name_field = driver.find_elements(By.CSS_SELECTOR, "input")[22]
        self.short_name_field.send_keys(Keys.CONTROL, 'a')
        self.short_name_field.send_keys(Keys.DELETE)
        
        self.badge_btn = driver.find_elements(By.CSS_SELECTOR, "span.badge")[6]
        
        self.submit_btn = driver.find_element(By.ID, "id_saveanddisplay")
        return (self.full_name_field, self.short_name_field, self.badge_btn, self.submit_btn)
    
    def test_rule_1(self):
        """C1: true, C2: true, C3: true"""
        elements = self.getElements()
        
        # Check that the page is correct
        ActionChains(driver).move_to_element(elements[0]).click().send_keys(
            "KIEM TRA PHAN MEM (CO3015) (CQ_HK222)"
        ).pause(DELAY).move_to_element(elements[1]).click().send_keys(
            "KTPM (CO3015)"
        ).pause(DELAY).move_to_element(elements[3]).click().pause(LONG_DELAY).perform()

    def test_rule_2(self):
        """C1: true, C2: true, C3: false"""
        elements = self.getElements()
        
        # Check that the page is correct
        ActionChains(driver).move_to_element(elements[0]).click().send_keys(
            "KIEM TRA PHAN MEM (CO3015) (CQ_HK222)"
        ).pause(DELAY).move_to_element(elements[1]).click().send_keys(
            "KTPM (CO3015)"
        ).pause(DELAY).move_to_element(elements[2]).click().pause(DELAY).move_to_element(elements[3]).click().pause(LONG_DELAY).perform()
    
    def test_rule_3(self):
        """C1: true, C2: false, C3: true"""
        elements = self.getElements()
        
        # Check that the page is correct
        ActionChains(driver).move_to_element(elements[0]).click().send_keys(
            "KIEM TRA PHAN MEM (CO3015) (CQ_HK222)"
        ).pause(DELAY).move_to_element(elements[3]).click().pause(LONG_DELAY).perform()
    
    def test_rule_4(self):
        """C1: true, C2: false, C3: false"""
        elements = self.getElements()
        
        # Check that the page is correct
        ActionChains(driver).move_to_element(elements[0]).click().send_keys(
            "KIEM TRA PHAN MEM (CO3015) (CQ_HK222)"
        ).move_to_element(elements[2]).click().pause(DELAY).move_to_element(elements[3]).click().pause(LONG_DELAY).perform()
        
    
    def test_rule_5(self):
        """C1: false, C2: true, C3: true"""
        elements = self.getElements()
        
        # Check that the page is correct
        ActionChains(driver).move_to_element(elements[1]).click().send_keys(
            "KTPM (CO3015)"
        ).pause(DELAY).move_to_element(elements[3]).click().pause(LONG_DELAY).perform()
    
    def test_rule_6(self):
        """C1: false, C2: true, C3: false"""
        elements = self.getElements()
        
        # Check that the page is correct
        ActionChains(driver).move_to_element(elements[1]).click().send_keys(
            "KTPM (CO3015)"
        ).move_to_element(elements[2]).click().pause(DELAY).move_to_element(elements[3]).click().pause(LONG_DELAY).perform()

    def test_rule_7(self):
        """C1: false, C2: false, C3: true"""
        elements = self.getElements()
        
        # Check that the page is correct
        ActionChains(driver).move_to_element(elements[3]).click().pause(LONG_DELAY).perform()
    
    def test_rule_8(self):
        """C1: false, C2: false, C3: false"""
        elements = self.getElements()
        
        # Check that the page is correct
        ActionChains(driver).move_to_element(elements[2]).click().pause(DELAY).move_to_element(elements[3]).click().pause(LONG_DELAY).perform()

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEditCourseGeneral)
    RichTestRunner().run(suite)
