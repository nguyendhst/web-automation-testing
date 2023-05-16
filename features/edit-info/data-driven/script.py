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

# Set up the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(10)

# Open the page
LOGIN_URL = "https://sandbox.moodledemo.net/login/index.php"
FEATURE_URL = "https://sandbox.moodledemo.net/user/edit.php?id=4&returnto=profile"
USERNAME = "student"
PASSWORD = "sandbox"
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "dataset.csv"))
SHORT_DELAY = 0.4
DELAY = 1
LONG_DELAY = 2
TIME_OUT = 10

driver.get(LOGIN_URL)
time.sleep(DELAY)
# Log in
username = driver.find_element(By.ID, "username")
username.send_keys(USERNAME)

password = driver.find_element(By.ID, "password")
password.send_keys(PASSWORD)

login = driver.find_element(By.ID, "loginbtn")
login.click()