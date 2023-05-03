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
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "utils"))
from rich_unittest import RichTestRunner


# Set up the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(10)

# Open the page
LOGIN_URL = "https://sandbox.moodledemo.net/login/index.php"
FEATURE_URL = "https://sandbox.moodledemo.net/course/view.php?id=2"
USERNAME_TEACHER = "teacher"
USERNAME_STUDENT = "student"
PASSWORD = "sandbox"
DELAY = 0.5
LONG_DELAY = 2
TIME_OUT = 10

FILES_PATH = os.path.join(os.path.dirname(__file__), "files/")

NUM_OF_TESTCASE = 7
NUM_OF_FILES = 21


class TestHelper():
    @staticmethod
    def createAssignment(assignmentName = 'Assignment 3: Web Automation Test', numOfUploadFiles = 20):
        driver.get(FEATURE_URL)
        driver.implicitly_wait(LONG_DELAY)
        
        # remove backdrop
        try:
            driver.execute_script("""document.querySelector('div[data-flexitour="backdrop"]').style.display ='none';""")
        except: pass
        
        # check if assignment exists by name
        activityNames = driver.find_elements(By.CSS_SELECTOR, 'span.instancename')
        if activityNames:
            for name in activityNames:
                if str(name.get_property('innerText')) == assignmentName:
                    driver.implicitly_wait(DELAY)
                    return
        
        # remove backdrop
        try:
            skipBtn = driver.find_element(By.CSS_SELECTOR, 'button[data-role="end"]')
            skipBtn.click()
        except:
            pass
        
        # change to edit mode
        setModeBtn = driver.find_element(By.CSS_SELECTOR, 'input[name="setmode"]')
        if not setModeBtn.get_attribute('checked'):
            setModeBtn.click()
        
        # add an activity
        WebDriverWait(driver, TIME_OUT).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.activity-add-text"))
        )[1].click()
        
        # select assignment option
        WebDriverWait(driver, TIME_OUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.optionname"))
        ).click()
        
        # input data field
        assignmentNameField = driver.find_elements(By.CSS_SELECTOR, '.form-control')[1]
        maxUploadFilesField = driver.find_element(By.ID, 'id_assignsubmission_file_maxfiles')
        submitBtn = driver.find_element(By.CSS_SELECTOR, 'input[name="submitbutton2"]')
        
        action = (
            ActionChains(driver)
            .move_to_element(assignmentNameField).click().send_keys(assignmentName)
            .move_to_element(maxUploadFilesField).click().send_keys(numOfUploadFiles).pause(DELAY)
            .move_to_element(submitBtn).pause(DELAY).click()
        )
        
        action.perform()
        action.reset_actions()
    
    
    @staticmethod
    def uploadAssignment(ASSIGNMENT_NAME, fileNameCount: int):
        driver.get(FEATURE_URL)
        driver.implicitly_wait(DELAY)
        
        # remove backdrop
        try:
            driver.execute_script("""document.querySelector('div[data-flexitour="backdrop"]').style.display ='none';""")
        except: pass
        
        # check if assignment exists by name
        activityNames = WebDriverWait(driver, TIME_OUT).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.aalink.stretched-link'))
        )
        
        if activityNames:
            for activity in activityNames:
                if str(activity.get_property('innerText')) == ASSIGNMENT_NAME:
                    activity.click()
        
        # remove submission
        try:
            editBtn = WebDriverWait(driver, TIME_OUT).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button[type="submit"]'))
            )[1]
            
            if str(editBtn.get_property('innerText')) == "Edit submission":
                WebDriverWait(driver, TIME_OUT).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button[type="submit"]'))
                )[2].click()
                driver.implicitly_wait(DELAY)
                WebDriverWait(driver, TIME_OUT).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button[type="submit"]'))
                )[2].click()
        except: pass
        
        # click Add Submission button
        addSubmissionBtn = WebDriverWait(driver, TIME_OUT).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button[type="submit"]'))
        )[1]
        
        addSubmissionBtn.click()
        
        # wait until upload area is shown
        time.sleep(1.5)
        
        # upload files
        for i in range(fileNameCount):
            try:
                fileUploadIcon = WebDriverWait(driver, TIME_OUT).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'i.fa-file-o'))
                )
                fileUploadIcon.click()
            except:
                # when reach max files, the upload icon will disappear
                return False
            
            # upload option
            try:
                uploadOptions = WebDriverWait(driver, TIME_OUT).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fp-repo.nav-item'))
                )
                
                isActiveLink = False
                for elementClass in uploadOptions[1].get_attribute("class"):
                    if str(elementClass) == "active":
                        isActiveLink = True
                if not isActiveLink:
                    ActionChains(driver).move_to_element(uploadOptions[1]).click().pause(DELAY).perform()
                
            except: pass
            
            # input file
            inputFile = WebDriverWait(driver, TIME_OUT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="repo_upload_file"]'))
            )
            inputFile.send_keys(FILES_PATH + str(i) + ".txt")
            
            # upload files
            try:
                uploadBtn = WebDriverWait(driver, TIME_OUT).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.fp-upload-btn'))
                )
                ActionChains(driver).pause(DELAY).move_to_element(uploadBtn).click().pause(DELAY).perform()

            except:
                return False
        
        time.sleep(1)
        
        saveBtn = WebDriverWait(driver, TIME_OUT).until(
            EC.element_to_be_clickable((By.ID, 'id_submitbutton'))
        )
        saveBtn.click()
        
        # if an alert appears, pass testcase
        if fileNameCount == 0:
            try:
                ActionChains(driver).pause(DELAY).move_to_element(driver.find_element(By.CLASS_NAME, 'alert-danger.alert')).perform()
                return False
            except:
                return True
        
        
        # if submit table appears, pass testcase
        try:
            tbl = driver.find_elements(By.CLASS_NAME, 'table.generaltable')
            return True
        except:
            return False
        
    @staticmethod
    def createTxtFiles():
        if not os.path.exists(FILES_PATH):
            os.makedirs(FILES_PATH)
        for i in range(NUM_OF_FILES):
            f = open(FILES_PATH + "\\" + str(i) + ".txt", "w")
            f.write('hello world!!!')
            f.close()

    @staticmethod
    def login(USERNAME):
        driver.get(LOGIN_URL)
        # log out
        try:
            btns = WebDriverWait(driver, LONG_DELAY).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".btn"))
            )
            for btn in btns:
                if btn.get_property('innerText') == 'Log out':
                    btn.click()
                    break
        except:
            pass
        
        username = WebDriverWait(driver, TIME_OUT).until(
            EC.element_to_be_clickable((By.ID, "username"))
        )
        username.send_keys(Keys.CONTROL, 'a')
        username.send_keys(Keys.DELETE)
        username.send_keys(USERNAME)
        
        password = WebDriverWait(driver, TIME_OUT).until(
            EC.element_to_be_clickable((By.ID, "password"))
        )
        password.send_keys(Keys.CONTROL, 'a')
        password.send_keys(Keys.DELETE)
        password.send_keys(PASSWORD)
        
        driver.find_element(By.ID, "loginbtn").click()
    
    
    
class TestUploadAssignment(unittest.TestCase):
    ASSIGNMENT_NAME = "Assignment 3: Web Automation Test"
    
    """Teacher session must be long enough when running testcases."""
    def test_upload_assignment_1(self):
        """Student uploads 5 files"""
        TestHelper.createTxtFiles()
        driver.implicitly_wait(TIME_OUT)
        
        TestHelper.login(USERNAME_TEACHER)
        TestHelper.createAssignment()
        TestHelper.login(USERNAME_STUDENT)
        self.assertTrue(TestHelper.uploadAssignment(self.ASSIGNMENT_NAME, 5))
    
    def test_upload_assignment_2(self):
        """Student uploads 1 file"""
        # TestHelper.login(USERNAME_TEACHER)
        # TestHelper.createAssignment()
        # TestHelper.login(USERNAME_STUDENT)
        self.assertTrue(TestHelper.uploadAssignment(self.ASSIGNMENT_NAME, 1))
    
    def test_upload_assignment_3(self):
        """Student uploads 2 files"""
        # TestHelper.login(USERNAME_STUDENT)
        self.assertTrue(TestHelper.uploadAssignment(self.ASSIGNMENT_NAME, 2))
    
    def test_upload_assignment_4(self):
        """Student uploads 20 files"""
        # TestHelper.login(USERNAME_STUDENT)
        self.assertTrue(TestHelper.uploadAssignment(self.ASSIGNMENT_NAME, 20))

    def test_upload_assignment_5(self):
        """Student uploads 19 files"""
        # TestHelper.login(USERNAME_STUDENT)
        self.assertTrue(TestHelper.uploadAssignment(self.ASSIGNMENT_NAME, 19))
        
    def test_upload_assignment_6(self):
        """Student uploads 0 files"""
        # TestHelper.login(USERNAME_STUDENT)
        self.assertFalse(TestHelper.uploadAssignment(self.ASSIGNMENT_NAME, 0))
    
    def test_upload_assignment_7(self):
        """Student uploads 21 files"""
        # TestHelper.login(USERNAME_STUDENT)
        self.assertFalse(TestHelper.uploadAssignment(self.ASSIGNMENT_NAME, 21))
        driver.quit()


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUploadAssignment)
    RichTestRunner().run(suite)
