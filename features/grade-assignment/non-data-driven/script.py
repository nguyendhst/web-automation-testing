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
# from logger import Logger 

# # Set preferred log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
# LOG_LV = "INFO"
# logger = Logger(LOG_LV)

# Set up the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(10)

# Open the page
LOGIN_URL = "https://sandbox.moodledemo.net/login/index.php"
FEATURE_URL = "https://sandbox.moodledemo.net/mod/assign/view.php?id=4"
USERNAME = "teacher"
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
    def OpenGradeSite(ctx):
        # navigate to moodle page
        driver.get(FEATURE_URL)

        # wait until moodle page is fully loaded
        driver.implicitly_wait(LONG_DELAY)

        gradeBtn = driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary")
        gradeBtn.click()

    @staticmethod
    def fillinGrade(ctx, grd: float):
        #fill in grade
        grade = driver.find_element(By.ID,"id_grade")
        grade.clear()
        grade.send_keys(grd)
        driver.implicitly_wait(2)

    #click Save change button
    @staticmethod
    def saveChange(ctx): 
        saveBtn = driver.find_element(By.NAME, "savechanges")
        saveBtn.click()

    #click Save and show next button
    @staticmethod
    def clickSaveAndShowNext(ctx):
        saveshownextBtn = driver.find_element(By.NAME, "saveandshownext")
        saveshownextBtn.click()
        
    #click Reset button
    @staticmethod
    def clickReset(ctx):
        resetBtn = driver.find_element(By.NAME, "savechanges")
        resetBtn.click()

class TestGradeAssignment(unittest.TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     cls.driver = driver
    #     cls.logger = logger

    def testcase_1(self):
        """Testcase 1: Normal Flow
        Step 1: Enter grade assignment page
        Step 2: Click button "Grade"
        Step 3: Fill in Grade: 5.0
        Step 4: Click button "Save Change" 
        """
        # self.logger.log("Test 00: Normal flow", "info")
        TestHelper.OpenGradeSite(self)
        TestHelper.fillinGrade(self,5.0)
        TestHelper.saveChange(self)

    def testcase_2(self):
        """Testcase 2: Alternative flow 1
        Step 1: Enter grade assignment page
        Step 2: Click button "Grade"
        Step 3: Fill in Grade: 5.0
        Step 4: Click button "Save and Show next" 
        """
        TestHelper.OpenGradeSite(self)
        TestHelper.fillinGrade(self,5.0)
        TestHelper.clickSaveAndShowNext(self)

    def testcase_3(self):
        """Testcase 3: Alternative flow 2
        Step 1: Enter grade assignment page
        Step 2: Click button "Grade"
        Step 3: Fill in Grade: 5.0
        Step 4: Click button "Reset" 
        """
        TestHelper.OpenGradeSite(self)
        TestHelper.fillinGrade(self,5.0)
        TestHelper.clickReset(self)

    def testcase_4(self):
        """Testcase 4: Exception flow 1
        Step 1: Enter grade assignment page
        Step 2: Click button "Grade"
        Step 3: Fill in Grade: -5.0
        Step 4: Click button "Save Changes" 
        """
        TestHelper.OpenGradeSite(self)
        TestHelper.fillinGrade(self,-5.0)
        TestHelper.saveChange(self)
        time.sleep(2)
        errorValue = driver.find_element(By.ID, "id_error_grade")
        self.assertTrue(errorValue)

    def testcase_5(self):
        """Testcase 5: Exception flow 2
        Step 1: Enter grade assignment page
        Step 2: Click button "Grade"
        Step 3: Fill in Grade: 102
        Step 4: Click button "Save Changes" 
        """
        TestHelper.OpenGradeSite(self)
        TestHelper.fillinGrade(self,102)
        TestHelper.saveChange(self)
        time.sleep(2)
        errorValue = driver.find_element(By.ID, "id_error_grade")
        self.assertTrue(errorValue)
    
    def testcase_6(self):
        """Testcase 6: Exception flow 3
        Step 1: Enter grade assignment page
        Step 2: Click button "Grade"
        Step 3: Fill in Grade: "ad"
        Step 4: Click button "Save Changes" 
        """
        TestHelper.OpenGradeSite(self)
        TestHelper.fillinGrade(self,"ad")
        TestHelper.saveChange(self)
        time.sleep(2)
        errorValue = driver.find_element(By.ID, "id_error_grade")
        self.assertTrue(errorValue)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGradeAssignment)
    RichTestRunner().run(suite)






