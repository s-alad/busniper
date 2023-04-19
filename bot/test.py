import json
import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class Test411withsignin():
    load_dotenv()
    username = os.getenv("USER")
    password = os.getenv("PASS")

    def setup_method(self, method):
        options = Options()
        # keep the window open after test is done for debugging.
        options.add_experimental_option("detach", True)

        # use chrome profile as a workaround for cookies
        path = os.getcwd()
        chrome_profile_path = path + "/saved-chrome-profile"
        options.add_argument("user-data-dir={}".format(chrome_profile_path))

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        self.vars = {}

    def teardown_method(self, method):
        # keep the window open after test is done for debugging.
        # self.driver.quit()
        pass

    def remember_2fa(self, wait):
        self.driver.switch_to.frame("duo_iframe")
        # wait until we can click the cancel button
        cancel_button = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".btn-cancel")))
        cancel_button.click()

        # now there's a button overlaying the "remember me" checkbox
        # we need to click it to get rid of it
        dismiss = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".medium-or-smaller")))
        dismiss.click()

        # 11 | click | name=dampen_choice |
        remember_me = wait.until(expected_conditions.element_to_be_clickable((By.NAME, "dampen_choice")))
        remember_me.click()

        # 12 | click | css=fieldset:nth-child(1) > .push-label > .auth-button |
        send_push = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR,
                                                                            "fieldset:nth-child(1) > .push-label > .auth-button")))
        send_push.click()

        # need to handle the following logic:
        # 1. we're already remembered, so we don't need to wait for 2fa

        # 2. we're not remembered, so we need to wait:
        #   a. cancel the first 2fa request
        #   b. click on the "remember me" checkbox
        #   c. click on the "send me a push" button
        #   d. wait until redirect

        self.driver.switch_to.default_content()

    def test_411withsignin(self):
        wait = WebDriverWait(self.driver, 10)  # lmfao 30 seconds timeout GOD DAMN student link is slow

        # initial exported code:
        # Test name: 411-with-signin
        # Step # | name | target | value
        # 1 | open | https://student.bu.edu/MyBU/s/ |
        self.driver.get("https://student.bu.edu/MyBU/s/")

        # self.driver.find_element(By.CSS_SELECTOR, ".comm-tile-menu__item-title-underline").click()
        wait.until(expected_conditions.presence_of_element_located((By.ID, "j_username")))
        # 3 | type | id=j_username | username
        self.driver.find_element(By.ID, "j_username").send_keys(self.username)
        # 4 | type | id=j_password | password
        self.driver.find_element(By.ID, "j_password").send_keys(self.password)
        # 5 | click | name=_eventId_proceed |
        self.driver.find_element(By.NAME, "_eventId_proceed").click()

        # after we get click sign in, two things can happen: we get redirected immediately,
        # or need to set remember-me status.
        # FIXME: Fuck this line
        time.sleep(2)
        redirect = expected_conditions.url_contains("https://student.bu.edu/MyBU/s/")(self.driver)
        duo_repeat = expected_conditions.url_contains("https://shib.bu.edu/idp/profile/SAML2")(self.driver)

        if duo_repeat:
            self.remember_2fa(wait)

        # after redirect, we don't need to interact with the ui.
        # just navigate to the registration page immediately
        self.driver.get(
            "https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1681765714?ModuleName=reg/option/_start.pl&ViewSem=Fall%202023&KeySem=20243")

        # 6 | click | linkText=Register for Class |
        register_for_class = wait.until(
            expected_conditions.element_to_be_clickable((By.LINK_TEXT, "Register for Class")))
        register_for_class.click()
        # 7 | click | name=College |
        self.driver.find_element(By.NAME, "College").click()
        # 8 | select | name=College | label=CAS
        dropdown = self.driver.find_element(By.NAME, "College")
        dropdown.find_element(By.XPATH, "//option[. = 'CAS']").click()
        # 9 | type | name=Dept | cs
        self.driver.find_element(By.NAME, "Dept").send_keys("cs")
        # 10 | type | name=Course | 411
        self.driver.find_element(By.NAME, "Course").send_keys("411")
        # 11 | click | css=td:nth-child(6) > input |
        self.driver.find_element(By.CSS_SELECTOR, "td:nth-child(6) > input").click()


if __name__ == "__main__":
    test = Test411withsignin()
    test.setup_method(None)
    test.test_411withsignin()
