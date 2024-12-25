from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from time import sleep
import scraper
import sys
import getProjectPath
import getFileNames
import openai_summarize
import pyperclip

post_count = 10
for _ in range(post_count):
    product_link, title, description = scraper.run_scraper()
    description = openai_summarize.summarize(description)
    if title == "no title":
        sys.exit(1)

    USERNAME = 'cosmincovaciu1'
    PASSWORD = 'Instagram121.'

    chrome_options = Options()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get("https://instagram.com")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class=\"_a9-- _ap36 _a9_0\"]")))
    accept_cookie_button = driver.find_element(By.CSS_SELECTOR, "button[class=\"_a9-- _ap36 _a9_0\"]")
    accept_cookie_button.click()
    sleep(5)
    input_username = driver.find_element(By.CSS_SELECTOR, "input[name=\"username\"]")
    input_username.send_keys(USERNAME)

    input_password = driver.find_element(By.CSS_SELECTOR, "input[name=\"password\"]")
    input_password.send_keys(PASSWORD)

    login_button = driver.find_element(By.CSS_SELECTOR, "button[type=\"submit\"]")
    login_button.click()
    sleep(5)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class=\"x1lliihq x193iq5w x6ikm8r x10wlt62 xlyipyv xuxw1ft\"]")))
    elements = driver.find_elements(By.CSS_SELECTOR, "span[class=\"x1lliihq x193iq5w x6ikm8r x10wlt62 xlyipyv xuxw1ft\"]")
    for element in elements:
        if element.text == "Create":
            element.click()
            break

    sleep(5)

    file_names = getFileNames.get_file_names('assets')
    print(file_names)
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type=\"file\"]")
    file_input.send_keys(f"{getProjectPath.get_project_path()}\\assets\\{file_names[0]}")
    file_names = file_names[1:]

    for file_name in file_names:
        open_media_gallery_button = driver.find_element(By.CSS_SELECTOR, "svg[aria-label=\"Open media gallery\"]")
        open_media_gallery_button.click()
        sleep(2)
        file_input = driver.find_element(By.CSS_SELECTOR, "input[type=\"file\"]")
        file_input.send_keys(f"{getProjectPath.get_project_path()}\\assets\\{file_name}")
        sleep(2)
        # open_media_gallery_button = driver.find_element(By.CSS_SELECTOR, "svg[aria-label=\"Open media gallery\"]")
        # open_media_gallery_button.click()
        driver.find_element(By.CSS_SELECTOR, "div[class=\"_ac7a\"]").click()
        sleep(2)

    next_button = driver.find_element(By.CSS_SELECTOR, "div[class=\"_ac7b _ac7d\"]")
    next_button.click()
    sleep(3)
    next_button = driver.find_element(By.CSS_SELECTOR, "div[class=\"_ac7b _ac7d\"]")
    next_button.click()
    sleep(5)

    input_text = driver.find_element(By.CSS_SELECTOR, "div[aria-label=\"Write a caption...\"]")
    input_text.send_keys(Keys.ENTER)
    input_text.send_keys(product_link)
    input_text.send_keys(Keys.ENTER)
    input_text.send_keys(title)
    input_text.send_keys(Keys.ENTER)
    pyperclip.copy(description)
    input_text.send_keys(Keys.SHIFT, Keys.INSERT)
    sleep(3)

    share_button = driver.find_element(By.CSS_SELECTOR, "div[class=\"_ac7b _ac7d\"]")
    share_button.click()
    sleep(15)
    driver.quit()

