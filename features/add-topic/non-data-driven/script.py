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

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "utils"))
from rich_unittest import RichTestRunner
from logger import Logger


# Set preferred log level: DEBUG, INFO, WARNING, ERROR, CRITICAL

LOG_LV = "INFO"
logger = Logger(LOG_LV)

# Open the page
LOGIN_URL = "https://sandbox.moodledemo.net/login/index.php"
COURSES_URL = "https://sandbox.moodledemo.net/my/courses.php"
USERNAME = "teacher"
PASSWORD = "sandbox"

class Helper():
    @staticmethod
    def addTopic(ctx, subject: str, msg: str, post = True):
        driver = ctx.driver
        # subject name
        sub = driver.find_element(By.ID, "id_subject")
        if sub.get_attribute('value') != "": sub.clear()
        sub.send_keys(subject)
        
        # message
        driver.switch_to.frame(driver.find_element(By.ID, "id_message_ifr"))
        mess = driver.find_element(By.XPATH, "//body/p")
        if mess.text != "": mess.clear()
        mess.send_keys(msg)
            
        driver.switch_to.default_content()
        # time.sleep(1)
            
        driver.find_element(By.ID, "id_submitbutton").click()
        time.sleep(2)
        
        

# END OF TEMPLATE -- CREATE YOUR OWN CLASS
class AddTopic(unittest.TestCase):
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
        
        # setup testing page    
        driver.get(COURSES_URL)
        #  access to specific course page
        driver.find_element(By.CLASS_NAME, "coursename").click()
        # open forum page
        driver.execute_script('document.querySelector(".aalink.stretched-link").click()')
        
        time.sleep(1)
    

    def setUp(self): pass
        # CURRENT = self.driver.current_url
        # self.driver.get(CURRENT)
        # time.sleep(2)

    # TEST CASES
    def test_01(self):
        """Test 01: Normal flow
        1. Subject = "subject HI"
        2. Message = "content HI"
        3. Click Post to forum btn
        """
        self.logger.log("Test 00: Normal flow", "info")
        # add topic btn
        self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary").click()
        Helper.addTopic(self, "subject HI", "content HI")
        
    def test_02(self):
        """Test 02: Msg field is blank
        1. Subject = "Subject 1"
        2. Message = ""
        3. Click Post to forum btn --> erro: missing message field 
        """
        self.logger.log("Test 01: Msg field is blank", "info")
        # add topic btn
        self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary").click()
        Helper.addTopic(self, "Subject 1", "")
    
    def test_03(self):
        """Test 03: Subject field is blank
        1. Subject = ""
        2. Message = "message..."
        3. Click Post to forum btn --> erro: missing subject field 
        """
        self.logger.log("Test 02: Subject field is blank", "info")    
        Helper.addTopic(self, "", "message...")
        
    def test_04(self):
        """Test 04: the length of subject field is greater than 255 chars
        1. Subject = "But I must explain to..." (> 255 chars)
        2. Message = "message"
        3. Click Post to forum btn --> error at subject field: Maximum of 255 characters
        """
        self.logger.log("Test 03: the length of subject field is greater than 255 chars", "info")    
        Helper.addTopic(self, "But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness.", "message...")
    
    def test_05(self):
        """Test 05: Both fields are empty --> error, missing required fields"""
        self.logger.log("Test 04: Both fields are empty", "info")    
        Helper.addTopic(self, "", "")
        

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(AddTopic)
    RichTestRunner().run(suite)
