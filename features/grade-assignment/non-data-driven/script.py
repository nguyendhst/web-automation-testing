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
FEATURE_URL = "https://sandbox.moodledemo.net/mod/assign/view.php?id=5"
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

        saveBtn = driver.find_element(By.NAME, "savechanges")
        saveBtn.click()

        #try (grade<0) except (grade>100) except (grade not a real)
        #finally: pass

    # @staticmethod
    # def clickSaveAndShowNext(ctx):
        
    # @staticmethod
    # def clickReset(ctx):

    
class TestGradeAssignment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = driver
        cls.logger = logger

    def testcase_1(self):
        """Testcase 1: Normal Flow"""
        self.logger.log("Test 00: Normal flow", "info")
        TestHelper.OpenGradeSite(self)
        TestHelper.fillinGrade(self,5.0)

    # def alt_flow_1(self):

    # def alt_flow_2(self):

    # def except_flow_1(self):

    # def except_flow_2(self):
    
    # def except_flow_3(self):
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGradeAssignment)
    RichTestRunner().run(suite)






