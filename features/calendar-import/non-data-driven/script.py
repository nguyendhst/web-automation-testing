# Test script for the calendar import functionality

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "utils"))
from rich_unittest import RichTestRunner


# Set up the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(10)

# Open the page
LOGIN_URL = "https://sandbox.moodledemo.net/login/index.php"
FEATURE_URL = "https://sandbox.moodledemo.net/calendar/import.php"
USERNAME = "admin"
PASSWORD = "sandbox"

driver.get(LOGIN_URL)

# Log in
username = driver.find_element(By.ID, "username")
username.send_keys(USERNAME)

password = driver.find_element(By.ID, "password")
password.send_keys(PASSWORD)

login = driver.find_element(By.ID, "loginbtn")
login.click()


class TestCalendarImport(unittest.TestCase):

	def test_calendar_import(self):
		"""Simple access test for the calendar import page"""
		# Go to the calendar import page
		driver.get(FEATURE_URL)
		# Check that the page is correct
		self.assertTrue("Import calendar" in driver.page_source)

	#def test_calendar_import_ical(self):
	#	# Go to the calendar import page
	#	driver.get(FEATURE_URL)
	#	# Check that the page is correct
	#	self.assertTrue("Import caledar" in driver.page_source)

	def test_calendar_valid_field1(self):
		"""Use-case Tesing
		- name: Calendar Import Normal Flow
		- description: Test the calendar import .ics URL functionality with valid fields
		- preconditions: User is logged in
		"""

		# Go to the calendar import page
		driver.get(FEATURE_URL)

		# Check that the page is correct
		self.assertTrue("Import calendar" in driver.page_source)

		# Check that the name field is valid
		calendar_name = driver.find_element(By.ID, "id_name")
		calendar_name.send_keys("Test Calendar")

		# Check that the field is valid
		calendar_url = driver.find_element(By.ID, "id_url")
		calendar_url.send_keys("https://www.google.com/calendar/ical/en.usa%23holiday%40group.v.calendar.google.com/public/basic.ics")

		# Import
		import_button = driver.find_element(By.ID, "id_add")
		import_button.click()

		# Check if successfully redirected to the manage calendars page
		self.assertTrue("Import or export calendars" in driver.page_source)
		

	def test_calendar_valid_field2(self):
		"""Use-case Tesing
		- name: Calendar Import Alternative Flow 1
		- description: Test the calendar import functionality with File Picker
		- preconditions: User is logged in
		"""

		# Go to the calendar import page
		driver.get(FEATURE_URL)

		# Check that the page is correct
		self.assertTrue("Import calendar" in driver.page_source)

		# Check that the name field is valid
		calendar_name = driver.find_element(By.ID, "id_name")
		calendar_name.send_keys("Test Calendar")

		# Select the file picker option
		selector = Select(driver.find_element(By.ID, "id_importfrom"))
		selector.select_by_index(1)

		## Confirm that the file picker is visible
		#file_picker = driver.find_element(By.ID, "filepicker-wrapper-6447ad08ccd7e")
		#self.assertTrue(file_picker.is_displayed())

		# Click the file upload button name="importfilechoose"
		file_picker_button = driver.find_element(By.NAME, "importfilechoose")
		file_picker_button.click()

		# Click the file upload option fp-repo-6447ad08ccd7e-3
		file_picker_option = driver.find_element(By.ID, "fp-repo-6447ad08ccd7e-3")
		file_picker_option.click()

		# get the input type="file"
		file_input = driver.find_element(By.XPATH, "//input[@type='file']")
		file_input.send_keys("C:\\Users\\joshu\\Desktop\\test.ics")


		# Import
		import_button = driver.find_element(By.ID, "id_add")
		import_button.click()

		# Check if successfully redirected to the manage calendars page
		self.assertTrue("Import or export calendars" in driver.page_source)

		

if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(TestCalendarImport)
	RichTestRunner().run(suite)