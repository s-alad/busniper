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

from bs4 import BeautifulSoup
import time
import pickle
import os
import requests
import collections ; collections.Callable = collections.abc.Callable

from course import Course

from dotenv import load_dotenv

class Sniper:
    load_dotenv()
    username = os.getenv("USER")
    password = os.getenv("PASS")
    path = os.getcwd()
    entry = "https://student.bu.edu/MyBU/s/"
    cookies = ""
    biscuits = {}

    def __init__(self):
        options = ChromeOptions()
        options.add_experimental_option("detach", True) #add expirimental option to keep window open after test is done for debugging
        options.add_argument("user-data-dir={}".format(self.path+"/profile"))
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    def headers(self):
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1?',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Cookie': self.cookies,
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

    def getCookies(self):
        driver = self.driver
        #wait until url changes to https://student.bu.edu/MyBU/s/ to save cookies
        #WebDriverWait(driver, 30).until(EC.url_changes(self.entry))
        #finish = WebDriverWait(driver, 30).until(EC.presence_of_element_located(((By.CLASS_NAME, "community_navigation-tileMenuItemBanner_tileMenuItemBanner"))))
        #save cookies to cookies.pkl
        #pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
        #for cookie in driver.get_cookies(): print(cookie)

        driver.get("https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1?ModuleName=menu.pl&NewMenu=Academics")
        time.sleep(1)
        cookies_list = driver.get_cookies()
        for cookie in cookies_list:
            self.cookies = self.cookies + cookie['name'] + '=' + cookie['value'] + '; '
            self.biscuits[cookie['name']] = cookie['value']
        print("COOKIES:", self.cookies)

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
    
    def register(self, course: Course):
        driver = self.driver
        #panel = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "community_navigation-tileMenuItem_tileMenuItem")))
        self.driver.get("https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1?ModuleName=reg/option/_start.pl&ViewSem=Fall%202023&KeySem=20243")
        self.driver.get("https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1?ModuleName=reg%2Fadd%2F_start.pl&ViewSem=Fall%202023&KeySem=20243")

        uri = "https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1?ModuleName=reg%2Fadd%2Fbrowse_schedule.pl&SearchOptionDesc=Class+Number&SearchOptionCd=S&ViewSem=Fall+2023&KeySem=20243&AddPlannerInd=&College={}&Dept={}&Course={}&Section={}".format(
            course.college,
            course.dept.lower(),
            course.course,
            course.section if course.section != None else ""
        )
        self.driver.get(uri)
        time.sleep(1)
        self.snipe(uri)
    
    def snipe(self, uri):
        r = requests.get(uri, headers=self.headers())
        print(r.status_code)
        soup = BeautifulSoup(r.content, 'html5lib')
        form = soup.find('form', attrs = {'name': 'SelectForm'})
        table = form.find('table')
        trs = table.find_all('tr')[3:]

        for tr in trs:
            tds = tr.find_all('td')
            title = tds[3].text
            seats = tds[5].text
            types = tds[7].text
            notes = tds[13].text
            print(title, seats, types, notes)

if __name__ == "__main__":
    bot = Sniper()
    bot.login()
    bot.getCookies()
    cs330 = Course("CAS", "CS", "330")
    bot.register(cs330)