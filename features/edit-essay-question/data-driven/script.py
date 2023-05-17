from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from webdriver_manager.chrome import ChromeDriverManager

from rich.panel import Panel
from rich import print

import unittest
import sys
import os
import time
import csv

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "utils"))
from rich_unittest import RichTestRunner
from logger import Logger


# Set preferred log level: DEBUG, INFO, WARNING, ERROR, CRITICAL

LOG_LV = "INFO"
logger = Logger(LOG_LV)

# Open the page
LOGIN_URL = "https://sandbox.moodledemo.net/login/index.php"
FEATURE_URL = "https://sandbox.moodledemo.net/question/edit.php?courseid=1"
USERNAME = "admin"
PASSWORD = "sandbox"
DATA_PATH = os.path.join(os.path.dirname(__file__), "data.csv")

class Helper():
    @staticmethod
    def createEssayQ(ctx, name: str, text: str, mark: str, feedback: str, ID: str, out, expected):
        driver = ctx.driver
        
        driver.find_element(By.CSS_SELECTOR, ".btn.btn-secondary").click()
        driver.find_element(By.ID, "item_qtype_essay").click()
        driver.find_element(By.CLASS_NAME, "submitbutton").click()
        time.sleep(1)
        # function to fill form
        Helper.formFiller(ctx, name, text, mark, feedback, ID, out, expected)
    
    @staticmethod
    def editEssayFromQBank(ctx, name: str, text: str, mark: str, feedback: str, ID: str, out, expected):
        driver = ctx.driver
        
        driver.find_element(By.ID, "action-menu-toggle-1").click()
        driver.find_element(By.ID, "actionmenuaction-1").click()
        time.sleep(1)
        Helper.formFiller(ctx, name, text, mark, feedback, ID, out, expected)
        
    
    @staticmethod
    def formFiller(ctx, name: str, text: str, mark: str, feedback: str, ID: str, out = False, expected = ""):
        driver = ctx.driver
        
        # question name
        qname = driver.find_element(By.ID, "id_name")
        if qname.get_attribute('value') != "": qname.clear()
        qname.send_keys(name)
    
        # question text
        driver.switch_to.frame(driver.find_element(By.ID, "id_questiontext_ifr"))
        qtexts = driver.find_elements(By.XPATH, "//body/p")
        for qtext in qtexts:
            if qtext.text != "": qtext.clear()
        qtexts[0].send_keys(text)
        
        driver.switch_to.default_content()
        time.sleep(1)
        
        # question default mark
        qmark = driver.find_element(By.ID, "id_defaultmark")
        if qmark.get_attribute('value') != "" and mark != "": 
            qmark.clear()
            qmark.send_keys(mark)
        
        # question feedback
        driver.switch_to.frame(driver.find_element(By.ID, "id_generalfeedback_ifr"))
        qfeedback = driver.find_element(By.XPATH, "//body/p")
        if qfeedback.text != "": qfeedback.send_keys(feedback)
        
        driver.switch_to.default_content()
        
        # question ID
        qid = driver.find_element(By.ID, "id_idnumber")
        if qid != "": qid.clear()
        qid.send_keys(ID)
        
        if out == False: driver.find_element(By.ID, "id_updatebutton").click()
        else: driver.find_element(By.ID, "id_submitbutton").click()
        
        time.sleep(1)
        
        result = '...'
        if expected != "":
            try:
                driver.find_element(By.ID, "action-menu-toggle-1")
                result = "success"
            except NoSuchElementException:
                result = "failed"
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
        
        # Log in
        driver.get(LOGIN_URL)

        username = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")
        login = driver.find_element(By.ID, "loginbtn")

        ActionChains(driver).move_to_element(username).click().send_keys(
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
        
        # set up initial env
        driver.get(FEATURE_URL)
        time.sleep(1)
        # create some essays
        Helper.createEssayQ(cls, "Question 66", "Default descriptions... Q6", "1", "Some feedbacks", "066", True, "")

    def setUp(self): pass
        
    # TEST CASES
    def test(self):
        """
        Test-cases for Equivalence class partitioning technique
        """
        with open(DATA_PATH, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                try:
                    Helper.editEssayFromQBank(self, row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                except:
                    Helper.formFiller(self, row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                finally: continue

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDrive)
    RichTestRunner().run(suite)