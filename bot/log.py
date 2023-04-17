from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

import time
import pickle

import os
from dotenv import load_dotenv

load_dotenv()
username = os.getenv("USER")
password = os.getenv("PASS")

entry = "https://student.bu.edu/MyBU/s/"

def getCookies(driver):
    #wait until url changes to https://student.bu.edu/MyBU/s/ to save cookies
    WebDriverWait(driver, 30).until(EC.url_changes(entry))
    finish = WebDriverWait(driver, 30).until(EC.presence_of_element_located(((By.CLASS_NAME, "community_navigation-tileMenuItemBanner_tileMenuItemBanner")))).click()
    #save cookies to cookies.pkl
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    for cookie in driver.get_cookies():
        print(cookie)

def login(driver):
    time.sleep(2)
    print("Logging in...")
    try:
        user = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "j_username"))).send_keys(username)
        pasw = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "j_password"))).send_keys(password)
        button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "_eventId_proceed"))).click()
    except TimeoutException:
        print("Timed out waiting for page to load")
        driver.quit()

if __name__ == "__main__":
    options = webdriver.FirefoxOptions()
    #options.add_argument("user-data-dir=cookies")

    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    driver.get(entry)
    #check if cookies exist in cookies.pkl
    if os.path.exists("cookies.pkl"):
        print("Cookies exist, loading...")
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            print(cookie)
            driver.add_cookie(cookie)
        driver.refresh()
        #login(driver)
    else:
        print("Cookies do not exist, logging in...")
        login(driver)
        getCookies(driver)
