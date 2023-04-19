from selenium import webdriver

from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions

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
    time.sleep(1)
    print("Logging in...")
    try:
        user = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "j_username"))).send_keys(username)
        pasw = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "j_password"))).send_keys(password)
        button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "_eventId_proceed"))).click()

        WebDriverWait(driver, 30).until(EC.url_changes("https://shib.bu.edu/idp/profile/SAML2/POST-SimpleSign"))
        print("switched to shibboleth")

        #check if url is now https://student.bu.edu/MyBU/s/ otherwise go to duo() function
        time.sleep(2)
        if driver.current_url == "https://student.bu.edu/MyBU/s/":
            print("DUO NOT NEEDED")
            pass
        else:
            duo(driver)
        
        print("Login successful")
    except TimeoutException:
        print("Timed out waiting for page to load")
        driver.quit()
    
    finish = WebDriverWait(driver, 30).until(EC.presence_of_element_located(((By.CLASS_NAME, "community_navigation-tileMenuItemBanner_tileMenuItemBanner"))))

def duo(driver):
    try:
        frame = WebDriverWait(driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "duo_iframe")))
        save = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "dampen_choice"))).click()
        passcode = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "passcode")))
        auth_buttons = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "auth-button")))
        push = auth_buttons[0].click()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    options = ChromeOptions()
    options.add_experimental_option("detach", True) #add expirimental option to keep window open after test is done for debugging
    
    path = os.getcwd()
    profile_path = path+"/profile"
    options.add_argument("user-data-dir={}".format(profile_path))

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(entry)
    login(driver)

    #check if cookies exist in cookies.pkl
    """ if os.path.exists("cookies.pkl"):
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
 """