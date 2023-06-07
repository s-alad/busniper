from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# FILE TO SAVE POTENTIALLY USEFUL CODE SNIPPETS ===================================================

class Utils:

    def dropdown(driver, course):
        dropdown = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "College")))
        dropdown.find_element(By.XPATH, "//option[. = '{}']".format(course.college)).click()

        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "Dept"))).send_keys(course.dept)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "Course"))).send_keys(course.course)
        if (course.section != None): WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "Section"))).send_keys(course.section)

        go = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//input[@type='button']")))[1].click()