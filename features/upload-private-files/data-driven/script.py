from selenium.webdriver.common.by import *
from selenium.webdriver import *

# from StudentTesting import StudentTesting
import unittest
import sys
import os
import csv
import time
import re
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "utils"))
from rich_unittest import RichTestRunner
from logger import Logger

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

# Open the page
LOGIN_URL = "https://sandbox.moodledemo.net/login/index.php"
FEATURE_URL = "https://sandbox.moodledemo.net/my/"
USERNAME = "student"
PASSWORD = "sandbox"

MAX_FILE_SIZE = 100
MB_SIZE = 1024*1024

TIME_OUT = 10

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "dataset.csv"))
FILES_PATH = os.path.join(os.path.dirname(__file__), "files/")
NUM_OF_FILES = 10
# mode
MODE = 0o777

LOG_LV = "INFO"
logger = Logger(LOG_LV)

class TestCreateNewEvent(unittest.TestCase):  
  @classmethod
  def setUpClass(cls):
    cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    cls.wait = WebDriverWait(cls.driver, TIME_OUT)
    cls.login(cls)
    cls.logger = logger

  @staticmethod
  def createTxtFiles(size, numFile: int = 1):
    if not os.path.exists(FILES_PATH):
      os.makedirs(FILES_PATH)
    for i in range(numFile):
      with open(FILES_PATH + "\\" + str(i) + ".txt", "w") as f:
        f.seek(size)
        f.write('0')
        f.close()

  def setUp(self):
    self.driver.get(FEATURE_URL)
    self.driver.get("https://sandbox.moodledemo.net/user/files.php")
    

  def login(self):
    self.driver.get(LOGIN_URL)

    username = self.driver.find_element(By.ID, "username")
    username.send_keys(USERNAME)

    password = self.driver.find_element(By.ID, "password")
    password.send_keys(PASSWORD)

    self.driver.find_element(By.ID, "loginbtn").click()

  def uploadByChooseFile(self):
    uploadOptions = self.wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fp-repo.nav-item'))
    )
    
    isActiveLink = False
    for elementClass in uploadOptions[1].get_attribute("class"):
        if str(elementClass) == "active":
            isActiveLink = True
    if not isActiveLink:
        action = (
          ActionChains(self.driver)
          .move_to_element(uploadOptions[1])
          .click()
          .pause(20)
          )
        action.perform()
        action.reset_actions()

  def inputFile(self, idx: int):
    # input file
    inputFile = self.wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="repo_upload_file"]'))
    )
    inputFile.send_keys(FILES_PATH + str(idx) + ".txt")
  
  def clickUploadBtn(self):
    uploadBtn = self.wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.fp-upload-btn'))
    )
    action = (
      ActionChains(self.driver).move_to_element(uploadBtn).click()
      )
    action.perform()
    action.reset_actions()

  def uploadFile(self,fileNameCount):
    # upload files
    try:
      fileUploadIcon = self.wait.until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, 'i.fa-file-o'))
      )
      fileUploadIcon.click()
    except:
        # when reach max files, the upload icon will disappear
        return False
    
    # upload option
    try:
      self.uploadByChooseFile()
            
    except: pass
    for i in range(fileNameCount):
      self.inputFile(i)
      try:
        self.clickUploadBtn()
      except:
        return False

    return False

  def test_upload_no_file(self):
    self.uploadFile(0)

  def test_upload_valid_file(self):
    fileCount = 1
    self.createTxtFiles(10,fileCount)
    self.uploadFile(fileCount)

  

if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(TestCreateNewEvent)
	RichTestRunner().run(suite)