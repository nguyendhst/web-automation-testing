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

# LOG_LV = "INFO"
# logger = Logger(LOG_LV)

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
                    filesize = size - 4.9 if size > 5 else size
                    f.seek(filesize * MB_SIZE)
                    print(".FILE {1} has size {1}".format(i, filesize))
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

    def login(self):
        self.driver.get(LOGIN_URL)

        username = self.driver.find_element(By.ID, "username")
        username.send_keys(USERNAME)

        password = self.driver.find_element(By.ID, "password")
        password.send_keys(PASSWORD)

        self.driver.find_element(By.ID, "loginbtn").click()

    def clickUploadByUpFileBtn(self):
        # print('--- Click Navigation Button ---')
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
        # print('--- Click Save Changes ---')

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
            # print(btn.get_attribute("class"))
        except:
            return False
        return True

    def inputFile(self, idx: int):
        # input file
        # print("INPUT FILE = {}".format(idx))
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'filepicker')]")
            )
        )
        self.wait.until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "i.icon.fa.fa-spin"))
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
        # print('--- Click Upload a file Button ---')
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
        # print('--- File Picker ---')
        fileUploadIcon = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='fp-btn-add']"))
        )
        self.driver.execute_script("arguments[0].click();", fileUploadIcon)
        return True

    def uploadEachFile(self, filename):
        # upload files
        # print('--- File Picker ---')
        fileUploadIcon = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='fp-btn-add']"))
        )
        self.driver.execute_script("arguments[0].click();", fileUploadIcon)

        if filename == 0:
            btn = self.driver.find_element(
                By.XPATH, "//span[contains(text(), 'Upload a file')]"
            )
            self.driver.execute_script("arguments[0].click();", btn)

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
            # print("OVERWRITE = {}".format(overwrite))

        except:
            pass

        # Save changes
        print("--- Click Save Changes ---")
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='submitbutton']"))
        )

        self.driver.execute_script("arguments[0].click();", btn)
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

    def test_upload_valid_file(self):
        with open(DATA_PATH, "r") as csv_file:
            reader = csv.reader(csv_file, delimiter=";")
            next(reader)
            for row in reader:
                print(f"Testing: {row[0]}, {row[1]}, {row[2]}", "info")
                fileSize = int(row[0])
                self.expected = row[2]
                fileCount = int(row[1])

                ableToUploadFile = False
                if fileCount == 0:
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

                    except:
                        self.logger.log(
                            f"Test failed: Got: {error_dialog.is_displayed()}, Expected: {self.expected}",
                            "error",
                        )
                        # print('>>> FAILED: no file attached but error dialog not displayed')

                else:
                    self.createTxtFiles(fileSize, fileCount)
                    for fileIdx in range(int(fileCount)):
                        ableToUploadFile = self.uploadEachFile(fileIdx)
                        if not ableToUploadFile:
                            break
                    self.driver.implicitly_wait(20)

                try:
                    result = False
                    if self.expected == "failure" and not ableToUploadFile:
                        result = True
                    elif self.expected == "success" and ableToUploadFile:
                        result = True
                    self.asserTrue(result)
                except:
                    self.logger.log(
                        f"Test failed: Upload file {fileIdx}, Expected: {self.expected}",
                        "error",
                    )
                    print(">>> FAILED: upload file {0}".format(fileIdx))

            if fileCount != 0:
                try:
                    self.asserTrue(ableToUploadFile)
                    try:
                        count = self.countFilesOnBoard()
                        self.assertGreaterEqual(count, fileCount)
                    except:
                        self.logger.log(
                            f"Test failed: Got: {count} files, Expected: {self.expected}",
                            "error",
                        )
                        # print('>>> failed')
                except:
                    self.logger.log(
                        f"Test failed: Got: {ableToUploadFile}, Expected: {self.expected}",
                        "error",
                    )


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCreateNewEvent)
    RichTestRunner().run(suite)
