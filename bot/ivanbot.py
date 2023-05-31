import collections
import os
import pickle
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

collections.Callable = collections.abc.Callable

from course import Course, Section

from dotenv import load_dotenv


class Sniper:
    load_dotenv()
    username = os.getenv("USER")
    password = os.getenv("PASS")
    path = os.getcwd()
    entry_link = "https://student.bu.edu/MyBU/s/"
    cookies = ""
    biscuits = {}

    def __init__(self):
        options = ChromeOptions()
        # add experimental option to keep window open after test is done for debugging
        options.add_experimental_option("detach", True)
        options.add_argument("user-data-dir={}".format(self.path + "/profile"))
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.wait_10 = WebDriverWait(self.driver, 10)
        self.wait_30 = WebDriverWait(self.driver, 30)
        self.wait = WebDriverWait(self.driver, 5)

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

    def get_cookies(self):
        driver = self.driver
        # wait until url changes to https://student.bu.edu/MyBU/s/ to save cookies
        # WebDriverWait(driver, 30).until(EC.url_changes(self.entry))
        # finish = WebDriverWait(driver, 30).until(EC.presence_of_element_located(((By.CLASS_NAME, "community_navigation-tileMenuItemBanner_tileMenuItemBanner"))))
        # save cookies to cookies.pkl
        # pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
        # for cookie in driver.get_cookies(): print(cookie)

        driver.get("https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1?ModuleName=menu.pl&NewMenu=Academics")
        time.sleep(1)
        cookies_list = driver.get_cookies()
        for cookie in cookies_list:
            self.cookies = self.cookies + cookie['name'] + '=' + cookie['value'] + '; '
            self.biscuits[cookie['name']] = cookie['value']
        print("COOKIES:", self.cookies)

    def login(self):
        driver = self.driver
        driver.get(self.entry_link)
        print("Logging in...")
        try:
            self.wait_10.until(EC.presence_of_element_located((By.ID, "j_username"))).send_keys(
                self.username)
            self.wait_10.until(EC.presence_of_element_located((By.ID, "j_password"))).send_keys(
                self.password)
            self.wait_10.until(
                EC.presence_of_element_located((By.NAME, "_eventId_proceed"))).click()

            self.wait_30.until(EC.url_changes("https://shib.bu.edu/idp/profile/SAML2/POST-SimpleSign"))
            print("switched to shibboleth")

            # check if url is now https://student.bu.edu/MyBU/s/ otherwise go to duo() function
            time.sleep(3)
            if driver.current_url == "https://student.bu.edu/MyBU/s/":
                print("DUO NOT NEEDED")
                pass
            else:
                print("DUO NEEDED")
                self.duo_remember()
            print("Login successful")
        except TimeoutException:
            print("Timed out waiting for page to load")
            driver.quit()

        self.driver.get(
            "https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1?ModuleName=reg/option/_start.pl&ViewSem=Fall%202023&KeySem=20243")

    def duo_remember(self) -> None:
        """
        This function is called when the user has duo enabled, and this session is not previously authorized.
        It will cancel the first request, and then click the "remember me" button, and then send the second request.
        There may be a way to programmatically set 2fa to remember me, but I haven't found it yet.
        :return: None
        """
        # wait for the duo wrapper to load
        self.wait_30.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "duo_iframe")))

        # cancel the current request - we want to select "remember me" first
        # however, sometimes this never happens haha. fuck you duo
        try:
            self.wait._timeout = 3
            cancel_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-cancel")))
            cancel_button.click()

            # now that we've cancelled, there's a button blocking the "remember me" button.
            # dismiss it.
            dismiss = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".medium-or-smaller")))
            dismiss.click()
        except TimeoutException as timeout:
            print("No cancel button found! Continuing...")

        # finally, click the "remember me" button
        remember_me = self.wait_10.until(EC.element_to_be_clickable((By.NAME, "dampen_choice")))
        remember_me.click()

        # send the push notification
        send_push = self.wait_10.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                   "fieldset:nth-child(1) > .push-label > .auth-button")))
        send_push.click()
        self.driver.switch_to.default_content()

    def cookie_login(self):
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
            self.get_cookies()

    def register(self, course: Course):
        driver = self.driver
        # panel = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "community_navigation-tileMenuItem_tileMenuItem")))
        self.driver.get(
            "https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1?ModuleName=reg/option/_start.pl&ViewSem=Fall%202023&KeySem=20243")
        self.driver.get(
            "https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1?ModuleName=reg%2Fadd%2F_start.pl&ViewSem=Fall%202023&KeySem=20243")

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
        soup = BeautifulSoup(r.content, 'html.parser')  # html5lib didn't work for me :(
        form = soup.find('form', attrs={'name': 'SelectForm'})
        table = form.find('table')
        trs = table.find_all('tr')[3:]

        for tr in trs:
            tds = tr.find_all('td')
            mark = tds[0].text

            section = Section(
                marktoadd=mark,
                classname=tds[2].text,
                titleinstructor=tds[3].text,
                openseats=tds[5].text,
                credithours=tds[6].text,
                classtype=tds[7].text,
                building=tds[8].text,
                room=tds[9].text,
                day=tds[10].text,
                start=tds[11].text,
                stop=tds[12].text,
                notes=tds[13].text)

            print(section, ">", section.can_add())


if __name__ == "__main__":
    bot = Sniper()
    bot.login()
    bot.get_cookies()
    cs330 = Course("CAS", "CS", "330")
    bot.register(cs330)
