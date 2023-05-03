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
# href="https://sandbox.moodledemo.net/my/"

class TestCreateNewEvent(unittest.TestCase):  
#  def __init__(self, methodName: str = ...) -> None:
#    super().__init__(methodName)
#    self.login()
    
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
    #self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #driver = self.driver

    #driver.implicitly_wait(10)
    self.driver.get(LOGIN_URL)

    username = self.driver.find_element(By.ID, "username")
    username.send_keys(USERNAME)

    password = self.driver.find_element(By.ID, "password")
    password.send_keys(PASSWORD)

    login = self.driver.find_element(By.ID, "loginbtn").click()
    #wait = WebDriverWait(driver,timeout=100).until((EC.element_to_be_clickable((By.CSS_SELECTOR, "[href='https://sandbox.moodledemo.net/my/']"))))
    
    # dashboard = driver.find_element(By.CSS_SELECTOR, "[href='https://sandbox.moodledemo.net/my/']" ).click()
    # driver.implicitly_wait(10)
    #wait = WebDriverWait(driver,timeout=100).until((EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-action='new-event-button']"))))
    # new_event = driver.find_element(By.CSS_SELECTOR, "[data-action='new-event-button']").click()

  def save(self):
    #driver = self.driver
    save_locator = self.driver.find_element(By.CSS_SELECTOR, "[data-action='save']")
    save_locator.click()

  def test_with_event_title(self):
    wait = WebDriverWait(self.driver,timeout=100)
    
    #event_title_input_locator = driver.find_element(By.CSS_SELECTOR, "[id='id_name']")
    event_title_input_locator = self.driver.find_element(By.XPATH, '//*[@id="id_name"]')
    self.driver.implicitly_wait(10)

    # sends keys to the input field
    ActionChains(self.driver)\
    .move_to_element(event_title_input_locator)\
    .send_keys("ABC")\
    .perform()
    
    self.save()

    modal = self.driver.find_element(By.CLASS_NAME, "modal-content")

    self.assertEqual(True,modal.is_displayed())

#  def test_no_event_title(self):
#    driver = self.driver
#    self.save()
#    required_error_text = driver.find_element(By.CSS_SELECTOR, "[id='id_error_name']") 
#    self.assertEqual(True, required_error_text.isDisplayed())
    

    


#class TestCreateNewEvent (StudentTesting):
#  def test_with_event_title(self):
#    driver = self.driver
#    wait = WebDriverWait(driver,timeout=100)
    
#    #event_title_input_locator = driver.find_element(By.CSS_SELECTOR, "[id='id_name']")
#    event_title_input_locator = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id='id_name']")))

#    ActionChains(driver)\
#      .move_to_element(event_title_input_locator)\
#      .send_keys("ABC")
#    self.save()

#    modal = driver.find_element(By.CLASS_NAME, "modal-content")

#    self.assertEqual(True,modal.isDisplayed())

#  def test_no_event_title(self):
#    driver = self.driver
#    self.save()
#    required_error_text = driver.find_element(By.CSS_SELECTOR, "[id='id_error_name']") 
#    self.assertEqual(True, required_error_text.isDisplayed())

  # def test_with_event_title(self):
  #   driver = self.driver
  #   event_title_input_locator = driver.find_element(By.CSS_SELECTOR, "[id='id_name']")
  #   ActionChains(driver)\
  #     .move_to_element(event_title_input_locator)\
  #     .send_keys("ABC")
  #   self.save()

if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(TestCreateNewEvent)
	RichTestRunner().run(suite)