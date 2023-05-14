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
import time

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

class Helper():
    @staticmethod
    def createEssayQ(ctx, name: str, text: str, mark: str, feedback: str, ID: str, out):
        driver = ctx.driver
        
        driver.find_element(By.CSS_SELECTOR, ".btn.btn-secondary").click()
        driver.find_element(By.ID, "item_qtype_essay").click()
        driver.find_element(By.CLASS_NAME, "submitbutton").click()
        time.sleep(1)
        # function to fill form
        Helper.formFiller(ctx, name, text, mark, feedback, ID, out)
    
    @staticmethod
    def editEssayFromQBank(ctx, name: str, text: str, mark: str, feedback: str, ID: str, out):
        driver = ctx.driver
        
        driver.find_element(By.ID, "action-menu-toggle-1").click()
        driver.find_element(By.ID, "actionmenuaction-1").click()
        time.sleep(1)
        Helper.formFiller(ctx, name, text, mark, feedback, ID, out)
        
    
    @staticmethod
    def formFiller(ctx, name: str, text: str, mark: str, feedback: str, ID: str, out = False):
        driver = ctx.driver
        
        # question name
        qname = driver.find_element(By.ID, "id_name")
        if qname.get_attribute('value') != "": qname.clear()
        qname.send_keys(name)
    
        # question text
        driver.switch_to.frame(driver.find_element(By.ID, "id_questiontext_ifr"))
        qtext = driver.find_element(By.XPATH, "//body/p")
        if qtext.text != "": qtext.clear()
        qtext.send_keys(text)
        
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
        
        time.sleep(2)       

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
        Helper.createEssayQ(cls, "Question 0", "Default descriptions... Q1", "10", "Some feedbacks", "001", True)
        Helper.createEssayQ(cls, "Question 100", "Default descriptions... Q100", "", "Feedback...", "100", True)

    def setUp(self): pass
        
    # TEST CASES
    def test_01(self):
        """ Test Normal flow:
            1. Question name = "Question 1"
            2. Question text = "These are some descriptions..."
            3. Default mark = 1
            4. Feedback = "Feedback..."
            5. ID = 002
            6. Click Save change buttom --> navigate to Question bank page
        """
        Helper.editEssayFromQBank(self, 
                                  "Question 1",
                                  "These are some descriptions...",
                                  "1", "Feedback...", "002", True)
    
    def test_02(self):
        """ 
        Don't update anything:
        1. Enter edit essay question page
        2. Click to 'Save changes' button without changeing anything --> navigate to Question bank page
        """
        self.driver.find_element(By.ID, "action-menu-toggle-1").click()
        self.driver.find_element(By.ID, "actionmenuaction-1").click()
        self.driver.find_element(By.ID, "id_submitbutton").click()
        
    def test_03(self):
        """ Missing 1 question name field
        1. Missing Question name field 
        2. --> can't submit form
        3. Type valid Question name
        4. Re-submit form --> navigate to Question bank page
        """
        # access to edit quesiton page from question bank
        Helper.editEssayFromQBank(self, "", "These are some descriptions...", "1", "Feedback...", "003", True)

        # fill all required fields and resubmit then navigate to question bank
        qname = self.driver.find_element(By.ID, "id_name").send_keys("Question 3")
        self.driver.find_element(By.ID, "id_submitbutton").click()
        
    def test_04(self):
        """ 1. Update question
            2. Click "Save changes and continue editing" button
            3. Update question again --> Save changes
        """
        Helper.editEssayFromQBank(self, "Question 4.1", "Description 04...", "4", "Feedback...", "0041", False)
        Helper.formFiller(self, "Question 4.2", "Description 04... 2", "", "Feedback...", "0042", True)
        
    def test_05(self):
        """ Type invalid input value
            1. Default mark's input value = "A"
            2. The system asserts error
        """
        try:
            Helper.editEssayFromQBank(self, "Quesiton 5", "Description 05...", "A", "Feedback", "005")
        except:
            self.assertTrue("Test 05")
    

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDrive)
    RichTestRunner().run(suite)