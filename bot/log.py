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

class Sniper:
    load_dotenv()
    username = os.getenv("USER")
    password = os.getenv("PASS")
    path = os.getcwd()
    entry = "https://student.bu.edu/MyBU/s/"

    def __init__(self):
        options = ChromeOptions()
        options.add_experimental_option("detach", True) #add expirimental option to keep window open after test is done for debugging
        options.add_argument("user-data-dir={}".format(self.path+"/profile"))
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    def getCookies(self):
        driver = self.driver
        #wait until url changes to https://student.bu.edu/MyBU/s/ to save cookies
        WebDriverWait(driver, 30).until(EC.url_changes(self.entry))
        finish = WebDriverWait(driver, 30).until(EC.presence_of_element_located(((By.CLASS_NAME, "community_navigation-tileMenuItemBanner_tileMenuItemBanner"))))
        #save cookies to cookies.pkl
        pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
        for cookie in driver.get_cookies(): print(cookie)

    def login(self):
        driver = self.driver
        driver.get(self.entry)
        print("Logging in...")
        try:
            user = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "j_username"))).send_keys(self.username)
            pasw = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "j_password"))).send_keys(self.password)
            button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "_eventId_proceed"))).click()

            WebDriverWait(driver, 30).until(EC.url_changes("https://shib.bu.edu/idp/profile/SAML2/POST-SimpleSign"))
            print("switched to shibboleth")

            #check if url is now https://student.bu.edu/MyBU/s/ otherwise go to duo() function
            time.sleep(5)
            if driver.current_url == "https://student.bu.edu/MyBU/s/":
                print("DUO NOT NEEDED")
                pass
            else: self.duo()
            print("Login successful")
        except TimeoutException:
            print("Timed out waiting for page to load")
            driver.quit()
        
        finish = WebDriverWait(driver, 30).until(EC.presence_of_element_located(((By.CLASS_NAME, "community_navigation-tileMenuItemBanner_tileMenuItemBanner"))))

    def duo(self):
        driver = self.driver
        try:
            frame = WebDriverWait(driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "duo_iframe")))
            save = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "dampen_choice"))).click()
            passcode = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "passcode")))
            auth_buttons = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "auth-button")))
            push = auth_buttons[0].click()
        except Exception as e:
            print(e)
    
    def cookieLogin(self):
        driver = self.driver
        if os.path.exists("cookies.pkl"):
            print("Cookies exist, loading...")
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                print(cookie)
                driver.add_cookie(cookie)
            driver.refresh()
        else:
            print("Cookies do not exist, logging in...")
            self.login()
            self.getCookies()
    
    def register(self):
        driver = self.driver
        #driver.get("https://www.bu.edu/link/bin/uiscgi_studentlink.pl/{}?ModuleName=regsched.pl")
        panel = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "community_navigation-tileMenuItem_tileMenuItem")))[0].click()

        #get all hrefs urls on page
        links = driver.find_elements_by_xpath("//a[@href]")
        for link in links:
            if "reg/option/" in link.get_attribute("href") and "Fall" in link.get_attribute("href"): 
                link.click()
                break

        #select the link that contains the string 'reg/option/' and 'Fall'

if __name__ == "__main__":
    bot = Sniper()
    bot.login()
    bot.register()