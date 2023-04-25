# Test script for the calendar import functionality

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

import os
import sys
import time
import datetime


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

# Go to the calendar import page
driver.get(FEATURE_URL)

# Check that the page is correct
assert "Import calendar" in driver.page_source
