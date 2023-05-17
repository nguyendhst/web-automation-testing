from selenium.webdriver.common.by import *
from selenium.webdriver import *

# from StudentTesting import StudentTesting
import unittest
import sys
import os
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
FEATURE_URL = "https://sandbox.moodledemo.net/user/files.php"
USERNAME = "student"
PASSWORD = "sandbox"

MAX_FILE_SIZE = 100
MB_SIZE = 1024 * 1024

TIME_OUT = 100

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "dataset.csv"))
FILES_PATH = os.path.join(os.path.dirname(__file__), "files/")
NUM_OF_FILES = 10
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
    def createTxtFiles(size, numFile, fileIdx: bool = False):
        if not os.path.exists(FILES_PATH):
            os.makedirs(FILES_PATH)
        if not fileIdx:
            for i in range(numFile):
                with open(FILES_PATH + str(i) + ".txt", "w") as f:
                    filesize = size - 1 if size > 2 else size
                    f.seek(filesize * MB_SIZE)
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
            self.logger.log(
                    f'Reset board', 'info'
                )


    def clickUploadByUpFileBtn(self):
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
        # print("send files", inputFile.is_displayed())
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
            return True
        except:
            return False


    def uploadFile(self, fileNameCount):
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
            self.logger.log(
                f'Upload file {str(i) + ".txt"}', 'info'
            )

            try: 
                btn = self.wait.until(
                    EC.element_to_be_clickable(        
                        (By.XPATH, "//button[@class='fp-upload-btn btn-primary btn']")
                    )
                )

                btn.click()
            except:
                self.logger.log(
                    f'Test failed: Cannot click to upload file', 'error'
                )

            overwrite = False
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "p.fp-dlg-text"))
                )

                overwrite = self.clickOverwriteBtn()
                # print("overwrite = {}".format(overwrite))

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
                (By.CSS_SELECTOR, "td.yui3-datatable-col-displayname.yui3-datatable-cell ")
            )
        )

        for upfile in uploadFiles:
            self.logger.log(
                f'Found existing file {upfile}', 'info'
            )
        return len(uploadFiles)

    def clickOverwriteBtn(self):
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".fp-dlg-butoverwrite"))
        ).click()

        return True
    def filePickerClick(self):
        fileUploadIcon = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='fp-btn-add']"))
        )
        self.driver.execute_script("arguments[0].click();", fileUploadIcon)
        return True

    def test_upload_no_file(self):
        self.logger.log(
                f'--- TEST: UPLOAD NO FILE', 'info'
            )
        fileUploadIcon = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'i.fa-file-o'))
        )
        fileUploadIcon.click()
        self.clickUploadByUpFileBtn()
        self.clickUploadBtn()
        error_dialog = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.file-picker.fp-msg-error'))
        )
        res = False
        try:
            res = self.assertTrue(error_dialog.is_displayed())
            self.logger.log(
                f'Test failed: Got Error Dialog {res} as expected', 'info'
            )
        except:
            self.logger.log(
                f'Test failed: Got Error Dialog {res}', 'error'
            )

 

    def test_upload_exist(self):
        self.logger.log(
                f'---  TEST: REUP EXISTING FILE', 'info'
            )
        fileCount = 1
        self.createTxtFiles(10,fileCount)
        self.filePickerClick()
        self.clickUploadByUpFileBtn()
        self.inputFile(0)
        self.clickUploadBtn()

        try:
            modal = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.file-picker.fp-dlg'))
            )
            # print(modal.get)
        except:
            modal = None

        if modal is None:
            self.clickSaveChanges()
            fileUploadIcon = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.fp-btn-add'))
                )
            fileUploadIcon.click()

            self.clickUploadByUpFileBtn()
            self.inputFile(0)
            self.clickUploadBtn()
            modal = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.file-picker.fp-dlg'))
            )
        try:
            self.assertTrue(modal.is_displayed())
            self.logger.log (
                f'Failed test: Detect Repeated File {True}', 'info'
            )
        except:
            self.logger.log (
                f'Failed test: Detect Repeated File {False}', 'error'
            )

    def test_upload_valid_file(self):
        self.logger.log(
                f'---  TEST: MULTIPLE VALID FILES', 'info'
            )
        self.emptyBoard()
        fileCount = 3
        self.createTxtFiles(3, fileCount)
        ableToUploadFile = self.uploadFile(fileCount)
        count = self.countFilesOnBoard()

        try:
            self.assertEqual(count, fileCount)
            self.logger.log(
                f'Test success: There are {count} files as expected', 'info'
            )
        except:
            self.logger.log(
                f'Failed test: There are only {count} files while expected {fileCount}', 'error'
            )
        

    def test_upload_oversized_file(self):
        self.logger.log(
                f'---  TEST: UPLOAD OVERSIZED 105MB FILE', 'info'
            )
        self.createTxtFiles(105,101,True)

        self.filePickerClick()
        self.clickUploadByUpFileBtn()

        self.inputFile(101)
        if not self.clickUploadBtn():
            self.logger.log(
                f'Success: Cannot upload oversized {105} MB file', 'info'
            )
            return
        
        error_dialog = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.file-picker.fp-msg-error'))
        )
        try:
            self.assertTrue(error_dialog.is_displayed())
            self.logger.log(
                f'Success: Error Dialog is displayed: {False}', 'info'
            )
        except:
            self.logger.log(
                f'Test failed: Error Dialog is displayed: {False}', 'error'
            )


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCreateNewEvent)
    RichTestRunner().run(suite)
