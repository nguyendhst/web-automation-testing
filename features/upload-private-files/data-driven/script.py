from selenium.webdriver.common.by import *
from selenium.webdriver import *

# from StudentTesting import StudentTesting
import unittest
import sys
import os
import csv
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "utils"))
from rich_unittest import RichTestRunner
# from logger import Logger

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

TIME_OUT = 100

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "dataset.csv"))
FILES_PATH = os.path.join(os.path.dirname(__file__), "files/")
NUM_OF_FILES = 10


# LOG_LV = "INFO"
# logger = Logger(LOG_LV)

class TestCreateNewEvent(unittest.TestCase):  
  @classmethod
  def setUpClass(cls):
    cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    cls.wait = WebDriverWait(cls.driver, TIME_OUT)
    cls.login(cls)

    # cls.logger = logger

  @staticmethod
  def createTxtFiles(size, numFile, fileIdx: bool = False):
    if not os.path.exists(FILES_PATH):
      os.makedirs(FILES_PATH)
    if not fileIdx:
      for i in range(numFile):
        with open(FILES_PATH + str(i) + ".txt", "w") as f:
          f.seek(size * MB_SIZE)
          f.write('0')
          f.close()
    else:
      with open(FILES_PATH + str(numFile) + ".txt", "w") as f:
        f.seek(size * MB_SIZE)
        f.write('0')
        f.close()

  def setUp(self):
    self.driver.get("https://sandbox.moodledemo.net/user/files.php")
    

  def login(self):
    self.driver.get(LOGIN_URL)

    username = self.driver.find_element(By.ID, "username")
    username.send_keys(USERNAME)

    password = self.driver.find_element(By.ID, "password")
    password.send_keys(PASSWORD)

    self.driver.find_element(By.ID, "loginbtn").click()

  def clickUploadByUpFileBtn(self):
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

  def clickSaveChanges(self):
    self.wait.until(
       EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class,'filepicker')]"))
      ) 
    btn = self.wait.until(
          EC.element_to_be_clickable((By.XPATH, "//input[@name='submitbutton']"))
      )
    btn.click()
    print(btn.get_attribute("class"))
    return True

  def inputFile(self, idx: int):
    # input file
    print("input file index = {}".format(idx))
    self.wait.until(
       EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'filepicker')]"))
      )
    self.wait.until(
      EC.invisibility_of_element_located((By.CSS_SELECTOR, 'i.icon.fa.fa-spin'))
    )
    inputFile = self.wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="repo_upload_file"]'))
    )
    inputFile.send_keys(FILES_PATH + str(idx) + ".txt")
  
  def clickUploadBtn(self):
    try:
      uploadBtn = self.wait.until(
          EC.element_to_be_clickable((By.XPATH, "//button[@class='fp-upload-btn btn-primary btn']"))
      )
      ActionChains(self.driver).move_to_element(uploadBtn).click().perform()
      return True
    except:
      return False


  def startUpload(self):
    try:
      fileUploadIcon = self.wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.fm-empty-container'))
      )
      fileUploadIcon.click()
    except:
        # when existing files, the upload icon will disappear
      fileUploadIcon = self.wait.until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, 'i.fa-file-o'))
      )
      fileUploadIcon.click()

  def uploadFile(self, fileNameCount):
    # upload files
    for i in range(fileNameCount):
      fileUploadIcon = self.wait.until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, 'i.fa-file-o'))
      )
      fileUploadIcon.click()
      
      # upload option
      self.clickUploadByUpFileBtn()            
      self.inputFile(i)
      self.clickUploadBtn()
      
      try:
        modal = self.wait.until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, 'p.fp-dlg-text'))
        )
        print(modal)
      except:
        modal = None
      
      if modal is not None:
        self.clickOverwriteBtn()
      
      saveChange = self.clickSaveChanges()
      if not saveChange:
        print("Cannot Save Changes")
      self.driver.implicitly_wait(10)
    
    return True

  def countFilesOnBoard(self):
    uploadFiles = self.wait.until(
      EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.fp-filename.text-truncate'))
    )
    
    for upfile in uploadFiles:
      print(upfile.text)
    return len(uploadFiles)

  def clickOverwriteBtn(self):
    self.wait.until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, '.fp-dlg-butoverwrite'))
    ).click()

  def test_upload_valid_file(self):
    with open(DATA_PATH, "r") as csv_file:
      reader = csv.reader(csv_file, delimiter=';')
      next(reader)
      for row in reader:
        self.logger.log(
            f"Testing: {row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}", "info"
        )
        fileSize = row[0]
        expected = row[2]
        fileCount = row[1]

        self.createTxtFiles(fileSize,fileCount)
        ableToUploadFile = self.uploadFile(fileCount)

        # count = self.countFilesOnBoard()
        # self.assertGreaterEqual(count, fileCount)

  
  # def test_upload_oversized_file(self):
  #   fileCount = 1
  #   self.createTxtFiles(10,fileCount)
  #   fileUploadIcon = self.wait.until(
  #       EC.element_to_be_clickable((By.CSS_SELECTOR, 'i.fa-file-o'))
  #   )
  #   fileUploadIcon.click()
  #   self.clickUploadByUpFileBtn()
  #   self.clickUploadBtn()
  #   error_dialog = self.wait.until(
  #     EC.element_to_be_clickable((By.CSS_SELECTOR, '.file-picker.fp-msg-error'))
  #   )
  #   self.assertTrue(error_dialog.is_displayed())

  # def test_upload_a_new_file(self):
  #   fileIdx = 40
  #   self.createTxtFiles(10,fileIdx, True)
  #   fileUploadIcon = self.wait.until(
  #       EC.element_to_be_clickable((By.CSS_SELECTOR, 'i.fa-file-o'))
  #   )
  #   fileUploadIcon.click()
  #   self.clickUploadByUpFileBtn()
  #   self.inputFile(fileIdx)
  #   self.clickUploadBtn()

  #   # wait until dialog disappear
  #   # a div with class that contains 'filepicker' is still there
    
  #   self.driver.implicitly_wait(20)
  #   self.clickSaveChanges()
  #   count = self.countFilesOnBoard()
  #   self.assertGreaterEqual(count, 1)




if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCreateNewEvent)
    RichTestRunner().run(suite)