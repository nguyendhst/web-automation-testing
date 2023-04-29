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

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "utils"))
from rich_unittest import RichTestRunner
from logger import Logger


# Set preferred log level: DEBUG, INFO, WARNING, ERROR, CRITICAL

LOG_LV = "INFO"
logger = Logger(LOG_LV)

# Open the page
LOGIN_URL = "https://sandbox.moodledemo.net/login/index.php"
FEATURE_URL = "https://sandbox.moodledemo.net/calendar/import.php"
USERNAME = "admin"
PASSWORD = "sandbox"
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "dataset.csv"))
# ../non-data-driven/
ICS_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "non-data-driven", "calendar.ics")
)
BAD_ICS_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "non-data-driven", "yolo.json")
)
ICS_URL = "https://www.google.com/calendar/ical/en.usa%23holiday%40group.v.calendar.google.com/public/basic.ics"


# END OF TEMPLATE -- CREATE YOUR OWN CLASS
class TestCalendarImport(unittest.TestCase):
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

        # check if files exist
        if (
            not os.path.exists(ICS_PATH)
            or not os.path.exists(BAD_ICS_PATH)
            or not os.path.exists(DATA_PATH)
        ):
            raise Exception("Files needed for tests not found")
        else:
            print(Panel.fit(f"Found files: {ICS_PATH}, {BAD_ICS_PATH}, {DATA_PATH}"))

        # login
        cls.login(cls)

    def setUp(self):
        """setUp runs before each test case run.
        This is where you set up any data needed for the tests.
        """
        pass

        # iterate through the data
        # self.test_data = next(self.test_data_reader)
        # self.username = self.test_data[0]
        # self.password = self.test_data[1]

    def login(self):
        self.driver.get(LOGIN_URL)
        username = self.driver.find_element(By.ID, "username")
        password = self.driver.find_element(By.ID, "password")
        login = self.driver.find_element(By.ID, "loginbtn")

        ActionChains(self.driver).move_to_element(username).click().send_keys(
            USERNAME
        ).move_to_element(password).click().send_keys(PASSWORD).move_to_element(
            login
        ).click().perform()

    def import_file(self, file):
        path = None
        for abs_path in [ICS_PATH, BAD_ICS_PATH]:
            if abs_path.endswith(file):
                path = abs_path
                break

        if path is None:
            raise Exception("File not found")

        selector = Select(self.driver.find_element(By.ID, "id_importfrom"))
        selector.select_by_visible_text("Calendar file (.ics)")
        btn = self.driver.find_element(By.XPATH, "//input[@name='importfilechoose']")
        btn.click()

        # click the upload file option driver.findElement(By.xpath("//span[contains(@class,'fp-repo-name') and contains(text(), 'Upload a file')]"))
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(), 'Upload a file')]")
            )
        )
        btn.click()

        # wait for 5 seconds for the shitty UI to load
        time.sleep(5)

        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='repo_upload_file']"))
        )
        btn.send_keys(path)

        time.sleep(2)

        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='fp-upload-btn btn-primary btn']")
            )
        )
        btn.click()

        time.sleep(2)
       
        btn = self.driver.find_element(By.ID, "id_add")

        self.driver.execute_script("arguments[0].click();", btn)

        ## Check if exception is thrown moodle-exception-message
        # promp_xpath = (
        #    "//div[contains(text(), 'JSON text filetype cannot be accepted.')]"
        # )
        # err = WebDriverWait(self.driver, 10).until(
        #    EC.visibility_of_element_located((By.XPATH, promp_xpath))
        # )
        # self.assertTrue(err.is_displayed())

    def import_url(self, url):
        # Check that the field is valid
        self.driver.find_element(By.ID, "id_url").send_keys(url)

        # Import
        self.driver.find_element(By.ID, "id_add").click()

        time.sleep(2)

    # TEST CASES
    def test_drive(self):
        with open(DATA_PATH, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                self.logger.log(
                    f"Testing: {row[0]}, {row[1]}, {row[2]}, {row[3]}", "info"
                )
                self.calenar_name = row[0]
                self.calendar_url = row[1]
                self.file_name = row[2]
                self.expected = row[3]

                self.driver.get(FEATURE_URL)
                time.sleep(2)

                # fill in the form
                calendar_name = self.driver.find_element(By.ID, "id_name")
                calendar_name.clear()
                if len(self.calenar_name) > 0:
                    calendar_name.send_keys(self.calenar_name)

                calendar_url = self.driver.find_element(By.ID, "id_url")
                calendar_url.clear()

                if len(self.calendar_url) > 0:
                    self.import_url(self.calendar_url)
                elif len(self.file_name) > 0:
                    self.import_file(self.file_name)
                elif len(self.calendar_url) == 0 and len(self.file_name) == 0:
                    # click submit btn
                    self.driver.find_element(By.ID, "id_add").click()
                    time.sleep(2)

                    try:
                        promp_xpath = "//div[contains(text(), 'JSON text filetype cannot be accepted.')]"
                        err = WebDriverWait(self.driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, promp_xpath))
                        )
                        if err.is_displayed() and self.expected == "success":
                            self.fail("Import failed when it should have succeeded")

                    except Exception:
                        pass

                time.sleep(2)

                if (
                    "events were imported" in self.driver.page_source
                    and self.expected != "success"
                ):
                    self.fail("Import succeeded when it should have failed")
                elif (
                    "events were imported" not in self.driver.page_source
                    and self.expected == "success"
                ):
                    self.fail("Import failed when it should have succeeded")
                else:
                    pass


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalendarImport)
    RichTestRunner().run(suite)
