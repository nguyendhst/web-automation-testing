from selenium.webdriver.common.by import *
from selenium.webdriver import *

# from StudentTesting import StudentTesting
import unittest
import sys
import os
import time

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
FEATURE_URL = "https://sandbox.moodledemo.net/user/files.php"
USERNAME = "student"
PASSWORD = "sandbox"

MAX_FILE_SIZE = 100
MB_SIZE = 1024 * 1024

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
                    f.write("0")
                    f.close()
        else:
            with open(FILES_PATH + str(numFile) + ".txt", "w") as f:
                f.seek(size * MB_SIZE)
                f.write("0")
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

        btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(), 'Upload a file')]")
            )
        )
        btn.click()

        print("Click upload button, direct to the file picker!!")

    def clickSaveChanges(self):

        btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='submitbutton']"))
        )
        self.driver.execute_script("arguments[0].click();", btn)

        return True

    def inputFile(self, idx: int):
      # input file
      inputFile = self.wait.until(
          EC.element_to_be_clickable(
              (By.CSS_SELECTOR, 'input[name="repo_upload_file"]')
          )
      )
      print("send files", inputFile.is_displayed())
      inputFile.send_keys(FILES_PATH + str(idx) + ".txt")

    def clickUploadBtn(self):
      time.sleep(5)
      uploadBtn = self.wait.until(
          EC.element_to_be_clickable((By.XPATH, "//button[@class='fp-upload-btn btn-primary btn']"))
        )
      
      uploadBtn.click()

      try:
          # timeout = 5
          WebDriverWait(self.driver, 20).until(
              EC.visibility_of_element_located((By.CSS_SELECTOR, "p.fp-dlg-text"))
          )

          self.clickOverwriteBtn()
          self.driver.implicitly_wait(10)

      except:
            pass


    def uploadFile(self, fileNameCount):
        # upload files
        for i in range(fileNameCount):

            fileUploadIcon = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='fp-btn-add']"))
            )

            self.driver.execute_script("arguments[0].click();", fileUploadIcon)

            if i == 0:
                btn = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Upload a file')]")
                self.driver.execute_script("arguments[0].click();", btn)

            inputFile = self.wait.until(
                    EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'input[name="repo_upload_file"]')
                )
            )
            time.sleep(2)
       
            inputFile.send_keys(FILES_PATH + str(i) + ".txt")

            btn = self.wait.until(
                EC.element_to_be_clickable(        
                    (By.XPATH, "//button[@class='fp-upload-btn btn-primary btn']")
                )
            )

            btn.click()

            overwrite = False
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "p.fp-dlg-text"))
                )

                overwrite = self.clickOverwriteBtn()
                print("overwrite = {}".format(overwrite))

            except:
                pass
            
            # Save changes 
            btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//input[@name='submitbutton']")
                )
            )

            self.driver.execute_script("arguments[0].click();", btn)

            #self.driver.implicitly_wait(5)
            time.sleep(5)

        return True

    def countFilesOnBoard(self):
        uploadFiles = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.fp-filename.text-truncate")
            )
        )

        for upfile in uploadFiles:
            print(upfile.text)
        return len(uploadFiles)

    def clickOverwriteBtn(self):
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".fp-dlg-butoverwrite"))
        ).click()

        return True

    # def test_upload_no_file(self):
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

    # def test_upload_exist(self):
    #   fileCount = 1
    #   self.createTxtFiles(10,fileCount)
    #   fileUploadIcon = self.wait.until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'i.fa-file-o'))
    #       )
    #   fileUploadIcon.click()

    #   self.clickUploadByUpFileBtn()
    #   self.inputFile(0)
    #   self.clickUploadBtn()

    #   try:
    #     modal = self.wait.until(
    #       EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.file-picker.fp-dlg'))
    #     )
    #     print(modal)
    #   except:
    #     modal = None

    #   if modal is None:
    #     self.clickSaveChanges()
    #     fileUploadIcon = self.wait.until(
    #       EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.fp-btn-add'))
    #         )
    #     fileUploadIcon.click()

    #     self.clickUploadByUpFileBtn()
    #     self.inputFile(0)
    #     self.clickUploadBtn()
    #     modal = self.wait.until(
    #         EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.file-picker.fp-dlg'))
    #       )
    #   self.assertTrue(modal.is_displayed())

    def test_upload_valid_file(self):
        fileCount = 3
        self.createTxtFiles(3.0 / 1024, fileCount)
        ableToUploadFile = self.uploadFile(fileCount)
        self.driver.implicitly_wait(20)
        count = self.countFilesOnBoard()
        self.assertGreaterEqual(count, fileCount)

    def test_upload_oversized_file(self):
      fileCount = 1
      self.createTxtFiles(100,101,True)

      # fileUploadIcon = self.wait.until(
      #           EC.element_to_be_clickable((By.XPATH, "//div[@class='fp-btn-add']"))
      #       )

      fileUploadIcon = self.wait.until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, 'i.icon.fa-file-o'))
      )
      fileUploadIcon.click()
      self.driver.execute_script("arguments[0].click();", fileUploadIcon)
      self.inputFile(101)
      self.clickUploadByUpFileBtn()
      self.clickUploadBtn()
      error_dialog = self.wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.file-picker.fp-msg-error'))
      )
      self.assertTrue(error_dialog.is_displayed())


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCreateNewEvent)
    RichTestRunner().run(suite)
