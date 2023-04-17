from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import time

import os
from dotenv import load_dotenv

load_dotenv()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

entry = "https://bu.my.site.com/myBU/"

def login(driver):
    #get element by id j_username
    try:
        user = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "j_username")))
        user.send_keys("saad7")
        passw = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "j_password")))
        passw.send_keys(password)
        button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "_eventId_proceed")))
        button.click()
    except TimeoutException:
        print("Timed out waiting for page to load")
        driver.quit()

if __name__ == "__main__":
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    driver.get(entry)
    login(driver)
