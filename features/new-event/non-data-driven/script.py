from selenium.webdriver.common.by import *
from selenium.webdriver import *

# from StudentTesting import StudentTesting
import unittest
import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "utils"))
from rich_unittest import RichTestRunner

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

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "dataset.csv"))

class TestCreateNewEvent(unittest.TestCase):  
  @classmethod
  def setUpClass(cls):
    cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    cls.login(cls)

  
  def setUp(self):
    self.driver.get(FEATURE_URL)
    new_event_btn = self.driver.find_element(By.CSS_SELECTOR, "[data-action='new-event-button']")
    new_event_btn.click()
    time.sleep(5)

  def login(self):
    self.driver.get(LOGIN_URL)

    username = self.driver.find_element(By.ID, "username")
    username.send_keys(USERNAME)

    password = self.driver.find_element(By.ID, "password")
    password.send_keys(PASSWORD)

    login = self.driver.find_element(By.ID, "loginbtn").click()

  def open_show_more(self):
    self.driver.find_element(By.CLASS_NAME, "moreless-toggler").click()
  
  def fill_event_name(self, eventname):
    wait = WebDriverWait(self.driver,timeout=100)
    
    event_title_input_locator = self.driver.find_element(By.XPATH, '//input[@id="id_name"]')
    self.driver.implicitly_wait(10)

    # sends keys to the input field
    ActionChains(self.driver)\
    .move_to_element(event_title_input_locator)\
    .click(on_element = event_title_input_locator)\
    .send_keys(eventname)\
    .perform()

  def count_events(self, event_name):
    event_elements = self.driver.find_elements(By.CLASS_NAME, 'eventname')
    new_event_count = 0
    for event in event_elements:
      if event.text == event_name:
        new_event_count += 1
    return new_event_count


  def save(self):
    #driver = self.driver
    save_locator = self.driver.find_element(By.CSS_SELECTOR, '[data-action="save"]')
    save_locator.click()

  # def test_no_event_title(self):
  #   driver = self.driver
  #   self.save()
  #   required_error_text = driver.find_element(By.XPATH, '//*[@id="id_error_name"]') 
  #   self.assertEqual(True, required_error_text.is_displayed())

  # def test_with_event_title(self):
  #   event_name = "This event is on"
  #   self.fill_event_name(event_name)
  #   self.save()
  #   self.driver.implicitly_wait(10)
  #   event_elements = self.driver.find_elements(By.CLASS_NAME, 'eventname')
  #   new_event = False
  #   for event in event_elements:
  #     if event.text == event_name:
  #       new_event = True

  #   self.assertEqual(True, new_event)
  
  # def test_default_show_more(self):
  #   self.fill_event_name("Check event more")
  #   self.driver.implicitly_wait(10)

  #   self.open_show_more()

  #   location_input = self.driver.find_element(By.ID, 'id_location')
  #   location_input.send_keys('location something....')

  #   duration_input = self.driver.find_element(By.ID, 'id_timedurationminutes')
  #   isDurEnable = duration_input.is_enabled()
  #   self.assertEqual(False, isDurEnable)

  def test_duration1(self):
    self.fill_event_name("Check event more")
    self.driver.implicitly_wait(10)

    self.open_show_more()

    # desc_input = self.driver.find_element(By.ID, 'id_description_ifr')
    # desc_input.send_keys('SOME random description')

    location_input = self.driver.find_element(By.ID, 'id_location')
    location_input.send_keys('location something....')

    self.driver.find_element(By.ID, 'id_duration_1').click()
    date_picker = self.driver.find_element(By.ID, 'id_timedurationuntil_day').click()
    date15 = self.driver.find_element(By.XPATH, '//*[@id="id_timedurationuntil_day"]/option[15]')
    date15.click()
    picked = date15.is_selected()
    self.assertEqual(True, picked)

  def test_duration2(self):
    self.fill_event_name("Check event more")
    self.driver.implicitly_wait(10)

    self.open_show_more()

    location_input = self.driver.find_element(By.ID, 'id_location')
    location_input.send_keys('location something....')

    self.driver.find_element(By.ID, 'id_duration_1').click()
    date_picker = self.driver.find_element(By.ID, 'id_timedurationuntil_day').click()
    date1 = self.driver.find_element(By.XPATH, '//*[@id="id_timedurationuntil_day"]/option[1]')
    date1.click()
    # picked = date1.is_selected()
    self.save()

    error_noti = self.driver.find_element(By.ID, 'fgroup_id_error_durationgroup')
    print(error_noti.text)
    self.assertTrue(True, error_noti.is_displayed())

  def test_duration3(self):
    self.fill_event_name("Check event more")
    self.driver.implicitly_wait(10)

    self.open_show_more()

    location_input = self.driver.find_element(By.ID, 'id_location')
    location_input.send_keys('location something....')

    self.driver.find_element(By.ID, 'id_duration_2').click()
    date_picker = self.driver.find_element(By.ID, 'id_timedurationuntil_day').click()
    mininutes = self.driver.find_element(By.ID, 'id_timedurationminutes')
    mininutes.send_keys(0)
    # picked = date1.is_selected()
    self.save()

    error_noti = self.driver.find_element(By.ID, 'fgroup_id_error_durationgroup')
    print(error_noti.text)
    self.assertTrue(True, error_noti.is_displayed())

  def test_repeat1(self):
    self.fill_event_name("Check event more")
    self.driver.implicitly_wait(10)

    self.open_show_more()

    location_input = self.driver.find_element(By.ID, 'id_location')
    location_input.send_keys('location something....')

    # self.driver.find_element(By.ID, 'id_repeat').click()
    repeat_input = self.driver.find_element(By.XPATH, '//*[@id="id_repeats"]')
    self.assertFalse(repeat_input.is_enabled())

  def test_repeat2(self):
    eventname = "Test repeat"
    event_repeat = 3
    self.fill_event_name(eventname)
    self.driver.implicitly_wait(10)

    self.open_show_more()

    location_input = self.driver.find_element(By.ID, 'id_location')
    location_input.send_keys('location something....')

    self.driver.find_element(By.ID, 'id_repeat').click()
    repeat_input = self.driver.find_element(By.XPATH, '//*[@id="id_repeats"]')
    if repeat_input.is_enabled():
      repeat_input.send_keys(event_repeat)
    self.save()

    count = self.count_events(eventname)
    self.assertGreaterEqual(count, event_repeat)











  

if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(TestCreateNewEvent)
	RichTestRunner().run(suite)