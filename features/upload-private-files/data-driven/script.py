from selenium.webdriver.common.by import *
from selenium.webdriver import *

# from StudentTesting import StudentTesting
import unittest
import sys
import os
import csv
import time

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

LOG_LV = "INFO"
logger = Logger(LOG_LV)

USERNAME = "student"
PASSWORD = "sandbox"

MAX_FILE_SIZE = 100
MB_SIZE = 1024 * 1024

TIME_OUT = 100

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "dataset.csv"))
FILES_PATH = os.path.join(os.path.dirname(__file__), "files/")


class TestCreateNewEvent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.wait = WebDriverWait(cls.driver, TIME_OUT)
        cls.login(cls)
        cls.logger = logger

    @staticmethod
    def createTxtFiles(size, numFile, fileIdx: bool = False):
        if not os.path.exists(FILES_PATH):
            os.makedirs(FILES_PATH)
        if not fileIdx:
            for i in range(int(numFile)):
                with open(FILES_PATH + str(i) + ".txt", "w") as f:
                    filesize = size - 1.0 if size > 2 else size
                    f.seek(filesize * MB_SIZE)
                    f.write("0")
                    f.close()
        else:
            with open(FILES_PATH + str(numFile) + ".txt", "w") as f:
                filesize = size - 4.9 if size > 5 else size
                f.seek(size * MB_SIZE)
                f.write("0")
                f.close()
        time.sleep(5)

    def setUp(self):
        self.driver.get("https://sandbox.moodledemo.net/user/files.php")


    def emptyBoard(self):
      try :
        empty = self.wait.until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, ".fm-empty-container"))
          )
        empty = True
      except:
        empty = False

      if not empty:
        self.wait.until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, "i.icon.fa-list.fa-fw"))
        ).click()
        self.wait.until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-togglegroup="file-selections"]'))
        ).click()
        self.wait.until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, "i.icon.fa-trash.fa-fw"))
        ).click()
        self.wait.until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fp-dlg-butconfirm.btn-primary.btn"))
        ).click()


    def login(self):
        self.driver.get(LOGIN_URL)

        username = self.driver.find_element(By.ID, "username")
        username.send_keys(USERNAME)

        password = self.driver.find_element(By.ID, "password")
        password.send_keys(PASSWORD)

        self.driver.find_element(By.ID, "loginbtn").click()

    def clickUploadByUpFileBtn(self):
        # self.logger.log('** Click Navigation Button **', "info")
        uploadOptions = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".fp-repo.nav-item"))
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
        # self.logger.log('** Click Save Changes **', "info")
        try:
          self.wait.until(
              EC.invisibility_of_element_located(
                  (By.XPATH, "//div[contains(@class,'filepicker')]")
              )
          )
          try:
            btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@name='submitbutton']"))
            )
            btn.click()
          except:
            return False
          return True
        except:
          return False
        

    def inputFile(self, idx: int):
        # input file
        # self.logger.log("INPUT FILE = {}".format(idx), "info")
        self.wait.until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "i.icon.fa.fa-spin"))
        )
        self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.fp-formset")
            )
        )
        
        try:
            inputFile = self.wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'input[name="repo_upload_file"]')
                )
            )
            time.sleep(3)
            inputFile.send_keys(FILES_PATH + str(idx) + ".txt")
        except:
            return False
        return True

    def clickUploadBtn(self):
        # self.logger.log('** Click Upload a file Button **', "info")
        try:
            uploadBtn = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@class='fp-upload-btn btn-primary btn']")
                )
            )
            ActionChains(self.driver).move_to_element(uploadBtn).click().perform()
            return True
        except:
            return False

    def filePickerClick(self):
        # self.logger.log('** File Picker **', "info")
        fileUploadIcon = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='fp-btn-add']"))
        )
        self.driver.execute_script("arguments[0].click();", fileUploadIcon)
        return True

    def uploadEachFile(self, filename):
        # upload files
        path = FILES_PATH + str(filename) + ".txt"
        file_stats = os.stat(path).st_size/ MB_SIZE
        self.fileSize = file_stats
        self.logger.log(
          '** File {1} Size {0} MB **'.format(file_stats, filename), 
          "info")
        fileUploadIcon = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='fp-btn-add']"))
        )
        self.driver.execute_script("arguments[0].click();", fileUploadIcon)

        if not self.inputFile(filename):
            return False

        if not self.clickUploadBtn():
            return False

        overwrite = False

        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "p.fp-dlg-text"))
            )

            overwrite = self.clickOverwriteBtn()
            # self.logger.log("OVERWRITE = {}".format(overwrite))

        except:
            pass

        # Save changes
        # self.logger.log("** Click Save Changes **", "info")
        # btn = WebDriverWait(self.driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, "//input[@name='submitbutton']"))
        # )

        # self.driver.execute_script("arguments[0].click();", btn)
        if not self.clickSaveChanges():
          return False
        time.sleep(5)
        return True

        # return self.clickSaveChanges()

    def countFilesOnBoard(self):
        uploadFiles = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.fp-filename.text-truncate")
            )
        )

        for upfile in uploadFiles:
            self.logger.log(upfile.text, "info")
        return len(uploadFiles)

    def clickOverwriteBtn(self):
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".fp-dlg-butoverwrite"))
        ).click()

    def test_upload_valid_file(self):
        with open(DATA_PATH, "r") as csv_file:
            reader = csv.reader(csv_file, delimiter=";")
            next(reader)
            for row in reader:
                self.logger.log(f"--- TESTING: {row[0]}, {row[1]}, {row[2]}", "info")
                self.fileSize = int(row[0])
                self.expected = row[2]
                fileCount = int(row[1])
                time.sleep(5)

                self.emptyBoard()
                ableToUploadFile = False
                if fileCount == 0:
                  self.logger.log(f'Test upload no file', "info")
                  self.filePickerClick()
                  self.clickUploadByUpFileBtn()
                  self.clickUploadBtn()
                  error_dialog = self.wait.until(
                      EC.element_to_be_clickable(
                          (By.CSS_SELECTOR, ".file-picker.fp-msg-error")
                      )
                  )
                  try:
                    self.assertTrue(error_dialog.is_displayed())
                    self.logger.log(
                          f"Error Dialog is displayed: {error_dialog.is_displayed()}",
                          "info",
                    )
                  except:
                    self.logger.log(
                        f"Test failed: Got: {error_dialog.is_displayed()}, Expected: {self.expected}",
                        "error",
                    )
                        # self.logger.log('>>> FAILED: no file attached but error dialog not displayed')

                else:
                  self.createTxtFiles(self.fileSize, fileCount)
                  for fileIdx in range(int(fileCount)):
                    ableToUploadFile = self.uploadEachFile(fileIdx)

                    try:
                      result = False
                      if self.expected == "failure" and not ableToUploadFile and fileIdx == fileCount-1:
                          result = True
                      elif ableToUploadFile:
                          result = True
                      self.assertTrue(result)
                      self.logger.log(
                          f"Test success: Upload file {fileIdx} file size {self.fileSize}, Got: {ableToUploadFile} as expected",
                          "info",
                      )
                    except:
                      self.logger.log(
                          f"Test failed: Upload file {fileIdx}, Expected: {self.expected}, Got: {result}",
                          "error",
                      )

            if fileCount != 0 and ableToUploadFile:
              try:
                  count = self.countFilesOnBoard()
                  self.assertGreaterEqual(count, fileCount)
              except:
                  self.logger.log(
                      f"Test failed: Got: {count} files, Expected: {self.expected}",
                      "error",
                  )

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCreateNewEvent)
    RichTestRunner().run(suite)
