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
import pandas as pd

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
FEATURE_URL = "https://sandbox.moodledemo.net/course/view.php?id=2"
USERNAME = "teacher"
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
    def createSurvey(surveyName = 'Assignment 3: Survey'):
        driver.get(FEATURE_URL)
        driver.implicitly_wait(LONG_DELAY)
        
        # remove backdrop
        try:
            driver.execute_script("""document.querySelector('div[data-flexitour="backdrop"]').style.display ='none';""")
        except: pass
        
        # change to edit mode
        setModeBtn = driver.find_element(By.CSS_SELECTOR, 'input[name="setmode"]')
        if not setModeBtn.get_attribute('checked'):
            setModeBtn.click()
        
        # remove backdrop
        try:
            skipBtn = driver.find_element(By.CSS_SELECTOR, 'button[data-role="end"]')
            skipBtn.click()
        except:
            pass
        
        # check if assignment exists by name
        # activityNames = driver.find_elements(By.CSS_SELECTOR, '.aalink.stretched-link')
        # if activityNames:
        #     for name in activityNames:
        #         if str(name.get_property('innerText')) == surveyName:
        #             driver.implicitly_wait(DELAY)
        #             #name.click()
        
        # add an activity
        WebDriverWait(driver, TIME_OUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span.activity-add-text"))
        ).click()
        
        # select survey option
        WebDriverWait(driver, TIME_OUT).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.optionname"))
        )[17].click()
        
        # input data field
        surveyNameField = driver.find_element(By.ID, 'id_name')
        surveyNameField.send_keys(surveyName)
        
        driver.implicitly_wait(DELAY)
        surveyTypeField = Select(driver.find_element(By.ID, 'id_template'))
        surveyTypeField.select_by_value("1")
        
        driver.implicitly_wait(DELAY)
        submitBtn = driver.find_element(By.ID, 'id_submitbutton')
        submitBtn.click()
        
    @staticmethod
    def fillInSurvey():
        driver.implicitly_wait(LONG_DELAY)
        # option: almost never
        surveyOptions1 = WebDriverWait(driver, TIME_OUT).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[type="radio"][value="1"]'))
        )
        # option: seldom
        surveyOptions2 = WebDriverWait(driver, TIME_OUT).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[type="radio"][value="2"]'))
        )
        # option: sometimes
        surveyOptions3 = WebDriverWait(driver, TIME_OUT).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[type="radio"][value="3"]'))
        )
        # option: often
        surveyOptions4 = WebDriverWait(driver, TIME_OUT).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[type="radio"][value="4"]'))
        )
        # option: almost always
        surveyOptions5 = WebDriverWait(driver, TIME_OUT).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[type="radio"][value="5"]'))
        )
        
        data = pd.read_csv(DATA_PATH)
        questionIdx = 0
        
        # hide reset timer notification bar
        # this bar prevent selenium from auto clicking survey options
        try:
            driver.execute_script("""document.querySelectorAll('footer>div')[3].style.display ='none';""")
        except: pass
        
        for index, row in data.iterrows():
            for point in row[1:]:
                point += 1
                
                action = ActionChains(driver)
                if point == 1:
                    action = action.move_to_element(surveyOptions1[questionIdx])
                if point == 2:
                    action = action.move_to_element(surveyOptions2[questionIdx])
                if point == 3:
                    action = action.move_to_element(surveyOptions3[questionIdx])
                if point == 4:
                    action = action.move_to_element(surveyOptions4[questionIdx])
                if point == 5:
                    action = action.move_to_element(surveyOptions5[questionIdx])
                action.click().perform()
                
                time.sleep(SHORT_DELAY)
                questionIdx += 1
        
        question25 = Select(driver.find_element(By.ID, 'q43'))
        question25.select_by_value("2")
        
        submitBtn = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
        submitBtn.click()
        
        responseReportBtn = driver.find_element(By.CSS_SELECTOR, 'li[data-key="9"] .nav-link')
        responseReportBtn.click()
        
        time.sleep(LONG_DELAY)
        
        # return false if cannot find survey graph
        try:
            driver.find_element(By.CSS_SELECTOR, 'img.resultgraph')
            return True
        except:
            return False

class TestCreateSurvey(unittest.TestCase):
    def test_survey(self):
        TestHelper.createSurvey()
        self.assertTrue(TestHelper.fillInSurvey())
        pass


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCreateSurvey)
    RichTestRunner().run(suite)
