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

TIME_OUT = 100

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "dataset.csv"))
LOG_LV = "INFO"
logger = Logger(LOG_LV)

class TestCreateNewEvent(unittest.TestCase):  
  @classmethod
  def setUpClass(cls):
    """setUpClass runs once per class.
        This is where you set up the driver and log in
        """
    cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    cls.wait =  WebDriverWait(cls.driver, TIME_OUT)
    cls.login(cls)
    cls.logger = logger

    if not DATA_PATH:
      raise Exception("Files needed for tests not found")
  
  def setUp(self):
    self.driver.get(FEATURE_URL)
    new_event_btn = self.wait.until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-action='new-event-button']"))
    )
    new_event_btn.click()
    time.sleep(5)

  def login(self):
    self.driver.get(LOGIN_URL)

    username = self.driver.find_element(By.ID, "username")
    username.send_keys(USERNAME)

    password = self.driver.find_element(By.ID, "password")
    password.send_keys(PASSWORD)

    self.wait.until(
      EC.element_to_be_clickable((By.ID, "loginbtn"))
      ).click()

  def save(self):
    #driver = self.driver
    self.wait.until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-action="save"]'))
    ).click()

  def fill_title(self):
    if self.event_title == "":
      return
    event_title_input_locator = self.wait.until(
       EC.element_to_be_clickable((By.XPATH, '//*[@id="id_name"]'))
      )

    # sends keys to the input field
    action = (
      ActionChains(self.driver)
      .move_to_element(event_title_input_locator)
      .click(on_element = event_title_input_locator)
      .send_keys(self.event_title)
      )
    
    action.perform()
    action.reset_actions()

  def choose_event_date(self):
    if self.event_date == "":
      return
    date = int(self.event_date)
    self.wait.until(
        EC.element_to_be_clickable((By.ID, 'id_timestart_day'))
      ).click()
    
    self.wait.until(
      EC.element_to_be_clickable((
          By.XPATH, '//*[@id="id_timestart_day"]/option[{date}]'.format(date = date)))
        ).click()

    self.driver.implicitly_wait(5)

  def open_show_more(self):
    self.driver.find_element(By.CLASS_NAME, "moreless-toggler").click()

  def fill_location(self):
    location = str(self.location)
    location_input = self.wait.until(
      EC.element_to_be_clickable((By.ID, 'id_location'))
    )
    location_input.send_keys(location)
  
  def pick_minutes(self, minute):
    self.wait.until(
      EC.element_to_be_clickable((By.ID, 'id_duration_2'))
      ).click()
    minute_input = self.wait.until(
      EC.element_to_be_clickable((By.NAME, "timedurationminutes"))
      )
    minute_input.send_keys(minute)
    # xpath = '//input[@id="id_timedurationminutes"]'
    # minute_input = self.wait.until(
    #   EC.element_to_be_clickable((By.XPATH, xpath))
    #   )
    # minute_input.send_keys(minute)


  def pick_date(self, datemonth):
    date, month = [int(res) for res in re.findall("[0-9]?[0-9]", str(datemonth))]

    self.wait.until(
      EC.element_to_be_clickable((By.ID, 'id_duration_1'))
      ).click()
    self.wait.until(
      EC.element_to_be_clickable((By.ID, 'id_timedurationuntil_day'))).click()
    datexpath = '//*[@id="id_timedurationuntil_day"]/option[{date}]'.format(date = date)
    self.wait.until(
      EC.element_to_be_clickable((By.XPATH, datexpath))
      ).click()

    self.wait.until(
      EC.element_to_be_clickable((By.ID, 'id_timedurationuntil_month'))
      ).click()
    monthxpath = '//*[@id="id_timedurationuntil_month"]/option[{month}]'.format(month=month)
    self.wait.until(
      EC.element_to_be_clickable((By.XPATH, monthxpath))
      ).click()
  
  def pick_duration(self):
    duration = str(self.duration)
    if duration == "":
      return 
    x = re.search("[0-9]?[0-9]/[0-9]?[0-9]", duration)
    if x is None:
      start, end = re.search("[0-9]+", duration).span()
      self.pick_minutes(duration[start:end])
    else:
      start, end = x.span()
      self.pick_date(duration)

  def choose_repeat(self):
    repeat_times = self.repeat_time
    if repeat_times == "":
      return
    repeat_times = int(repeat_times)
    self.wait.until(
      EC.element_to_be_clickable((By.XPATH, '//*[@id="id_repeat"]'))
      ).click()
    repeat_input = self.wait.until(
      EC.element_to_be_clickable((By.CLASS_NAME, 'form-check-input')))
    if repeat_input.is_enabled():
      repeat_input.send_keys(repeat_times)

  def test_drive(self):
    with open(DATA_PATH, "r") as csv_file:
      reader = csv.reader(csv_file, delimiter=';')
      next(reader)
      for row in reader:
        self.logger.log(
            f"Testing: {row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}", "info"
        )
        self.event_title = row[0]
        self.event_date = row[1]
        self.location = row[2]
        self.duration = row[3]
        self.repeat_time = row[4]
        self.expected = row[5]
        
        self.setUp()
        self.fill_title()
        self.choose_event_date()
        self.open_show_more()
        self.fill_location()
        self.pick_duration()
        self.choose_repeat()
        self.save()


        error_noti = self.driver.find_element(By.ID, 'fgroup_id_error_durationgroup')
        required_error_text = self.driver.find_element(By.XPATH, '//*[@id="id_error_name"]') 

        if (error_noti.is_displayed() and self.expected == 'success'):
          self.fail("Error on configuring duration for event")
        elif (required_error_text.is_displayed() and self.expected == 'success'):
          self.fail("Event name is required")

        self.driver.implicitly_wait(30)
        
  

if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(TestCreateNewEvent)
	RichTestRunner().run(suite)