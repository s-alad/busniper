from selenium import webdriver

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

# FILE TO SAVE POTENTIALLY USEFUL CODE SNIPPETS ===================================================

def dropdown(driver, course):
    dropdown = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "College")))
    dropdown.find_element(By.XPATH, "//option[. = '{}']".format(course.college)).click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "Dept"))).send_keys(course.dept)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "Course"))).send_keys(course.course)
    if (course.section != None): WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "Section"))).send_keys(course.section)

    #get all buttons inputs with type button
    go = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//input[@type='button']")))[1].click()