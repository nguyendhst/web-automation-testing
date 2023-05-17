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
FEATURE_URL = "https://sandbox.moodledemo.net/my/"
USERNAME = "student"
PASSWORD = "sandbox"
TIME_OUT = 100
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "dataset.csv"))

from enum import Enum

# Set preferred log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LV = "INFO"
logger = Logger(LOG_LV)

class TestCreateNewEvent(unittest.TestCase):  
  @classmethod
  def setUpClass(cls):
    """setUpClass runs once per class.
        This is where you set up the driver and log in
        """
    cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    cls.wait = WebDriverWait(cls.driver, TIME_OUT)
    cls.login(cls)

  
  def setUp(self):
    self.driver.get(FEATURE_URL)
    new_event_btn = self.wait.until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-action='new-event-button']")))
    new_event_btn.click()
    time.sleep(5)

  def login(self):
    self.driver.get(LOGIN_URL)

    username = self.wait.until(
      EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(USERNAME)

    password = self.wait.until(
      EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(PASSWORD)

    self.wait.until(
      EC.element_to_be_clickable((By.ID, "loginbtn"))).click()

  def open_show_more(self):
    self.wait.until(
      EC.element_to_be_clickable((By.CLASS_NAME, "moreless-toggler"))).click()
  
  def fill_event_name(self, eventname):
    event_title_input_locator = self.wait.until(
      EC.element_to_be_clickable((By.XPATH, '//input[@id="id_name"]')))

    # sends keys to the input field
    action = (
      ActionChains(self.driver)
    .move_to_element(event_title_input_locator)
    .click(on_element = event_title_input_locator)
    .send_keys(eventname)
    )

    action.perform()
    action.reset_actions()

  def count_events(self, event_name):
    event_elements = self.wait.until(
      EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-action="view-event"]')))
    new_event_count = 0
    for event in event_elements:
      if event.get_attribute("title") == event_name:
        new_event_count += 1
    return new_event_count


  def save(self):
    #driver = self.driver
    save_locator = self.wait.until(
      EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-action="save"]')))
    save_locator.click()

  def test_no_event_title(self):
    self.save()
    required_error_text = self.wait.until(
      EC.element_to_be_clickable((By.XPATH, '//*[@id="id_error_name"]')))
    self.assertFalse(required_error_text.is_displayed())

  # def test_with_event_title(self):
  #   event_name = "This event is on"
  #   self.fill_event_name(event_name)
  #   self.save()
  #   self.driver.implicitly_wait(10)
  #   try:
  #     event_elements = self.wait.until(
  #       EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-action="view-event"]')))
  #   except:
  #     event_elements = self.wait.until(
  #       EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-action="view-event"]')))
    
  #   new_event = False
  #   for event in event_elements:
  #     if event.get_attribute("title") == event_name:
  #       new_event = True

  #   # self.assertTrue(new_event)
  #   self.assertFalse(new_event)
  
  def test_default_show_more(self):
    self.fill_event_name("Check event more")
    self.driver.implicitly_wait(10)

    self.open_show_more()

    location_input = self.wait.until(
      EC.element_to_be_clickable((By.ID, 'id_location')))
    location_input.send_keys('location something....')
    isDurEnable = False
    try:
      duration_input = self.wait.until(
        EC.element_to_be_clickable((By.ID, 'id_timedurationminutes')))
      isDurEnable = duration_input.is_enabled()
    except:
      print("No input allow")

    self.assertTrue(isDurEnable)

  def test_duration1(self):
    self.fill_event_name("Check event more")
    self.driver.implicitly_wait(10)

    self.open_show_more()

    location_input = self.wait.until(
      EC.element_to_be_clickable((By.ID, 'id_location')))
    location_input.send_keys('Location for event')

    self.wait.until(
      EC.element_to_be_clickable((By.ID, 'id_duration_1'))).click()
    date_picker = self.wait.until(
      EC.element_to_be_clickable((By.ID, 'id_timedurationuntil_day'))).click()
    date15 = self.wait.until(
      EC.element_to_be_clickable((By.XPATH, '//*[@id="id_timedurationuntil_day"]/option[15]')))
    date15.click()
    picked = date15.is_selected()
    self.assertFalse(picked)

  def test_duration2(self):
    self.fill_event_name("Check event more")
    self.driver.implicitly_wait(10)

    self.open_show_more()

    location_input = self.wait.until(
      EC.element_to_be_clickable((By.ID, 'id_location')))
    location_input.send_keys('location something....')

    self.wait.until(
      EC.element_to_be_clickable((By.ID, 'id_duration_1'))).click()
    date_picker = self.wait.until(
      EC.element_to_be_clickable((By.ID, 'id_timedurationuntil_day'))).click()
    date1 = self.wait.until(
      EC.element_to_be_clickable((By.XPATH, '//*[@id="id_timedurationuntil_day"]/option[1]')))
    date1.click()
    # picked = date1.is_selected()
    self.save()

    error_noti = self.wait.until(
      EC.element_to_be_clickable((By.ID, 'fgroup_id_error_durationgroup')))
    print(error_noti.text)
    self.assertFalse(error_noti.is_displayed())

  def test_duration3(self):
    self.fill_event_name("NEW BRANDING")
    self.open_show_more()

    location_input = self.wait.until(
      EC.element_to_be_clickable((By.ID, 'id_location')))
    location_input.send_keys('location something....')

    self.wait.until(
      EC.element_to_be_clickable((By.ID, 'id_duration_2'))).click()
    xpath = '//input[@id="id_timedurationminutes"]'
    minute_input = self.wait.until(
      # EC.element_to_be_clickable((By.XPATH, xpath))
      EC.element_to_be_clickable((By.NAME, "timedurationminutes"))
      )
    minute_input.send_keys(0)

    # picked = date1.is_selected()
    self.save()

    error_noti = self.wait.until(
      EC.element_to_be_clickable((By.ID, 'fgroup_id_error_durationgroup')))
    print(error_noti.text)
    self.assertFalse(error_noti.is_displayed())

  def test_repeat1(self):
    self.fill_event_name("Check event more")
    self.driver.implicitly_wait(10)

    self.open_show_more()

    location_input = self.wait.until(
      EC.element_to_be_clickable((By.ID, 'id_location')))
    location_input.send_keys('location something....')

    self.wait.until(
      EC.element_to_be_clickable((By.ID, 'id_repeat'))).click()
    repeat_input = self.wait.until(
      EC.element_to_be_clickable((By.XPATH, '//*[@id="id_repeats"]')))
    self.assertFalse(repeat_input.is_enabled())

  def test_repeat2(self):
    eventname = "Test repeat"
    event_repeat = 3
    self.fill_event_name(eventname)
    self.driver.implicitly_wait(10)

    self.open_show_more()

    location_input = self.wait.until(
      EC.element_to_be_clickable((By.ID, 'id_location')))
    location_input.send_keys('location something....')

    self.wait.until(
      EC.element_to_be_clickable((By.ID, 'id_repeat'))).click()
    repeat_input = self.wait.until(
      EC.element_to_be_clickable((By.XPATH, '//*[@id="id_repeats"]')))
    if repeat_input.is_enabled():
      repeat_input.send_keys(event_repeat)
    self.save()

    count = self.count_events(eventname)
    self.assertLess(count, event_repeat)
  

if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(TestCreateNewEvent)
	RichTestRunner().run(suite)