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
import openai_summarize
import pyperclip
import json

def run(username, password):
    data = []

    post_count = 10

    for _ in range(post_count):
        IMAGE_PATH = f"{getProjectPath.get_project_path()}\\image.jpg"
        product_link, title, description, sku, price = scraper.run_scraper()
        json_data = {}
        json_data['sku'] = sku
        json_data['title'] = title
        json_data['price'] = price
        json_data['description'] = description

        data.append(json_data)

        description = openai_summarize.summarize(description)
        if title == "no title":
            sys.exit(1)

        # EMAIL_ADDRESS = '0040741119913'
        # PASSWORD = '?BE$EgHdMQ7P64;'
        EMAIL_ADDRESS = username
        PASSWORD = password

        chrome_options = Options()
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options.add_experimental_option("prefs",prefs)

        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        driver.get("https://facebook.com")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[title=\"Allow all cookies\"]")))
        accept_cookie_button = driver.find_element(By.CSS_SELECTOR, "button[title=\"Allow all cookies\"]")
        accept_cookie_button.click()

        input_email = driver.find_element(By.CSS_SELECTOR, "input[id=\"email\"]")
        input_email.send_keys(EMAIL_ADDRESS)

        input_password = driver.find_element(By.CSS_SELECTOR, "input[id=\"pass\"]")
        input_password.send_keys(PASSWORD)

        login_button = driver.find_element(By.CSS_SELECTOR, "button[type=\"submit\"]")
        login_button.click()
        sleep(5)

        driver.get("https://facebook.com")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class=\"x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1nxh6w3 x1sibtaa x1s688f xi81zsa\"]")))
        elements = driver.find_elements(By.CSS_SELECTOR, "span[class=\"x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1nxh6w3 x1sibtaa x1s688f xi81zsa\"]")
        for element in elements:
            if element.text == "Switch to Page":
                element.click()
                break
        sleep(10)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[class=\"x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft\"]")))

        elements = driver.find_elements(By.CSS_SELECTOR, "span[class=\"x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft\"]")
        for element in elements:
            if element.text == "Photo/video":
                element.click()
                break

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xurb0ha x1sxyh0 x1gslohp x12nagc xzboxd6 x14l7nz5\"]")))
        input_file_parent = driver.find_element(By.CSS_SELECTOR, "div[class=\"x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w xurb0ha x1sxyh0 x1gslohp x12nagc xzboxd6 x14l7nz5\"]")
        input_file = input_file_parent.find_element(By.CSS_SELECTOR, ":first-child")
        input_file.send_keys(IMAGE_PATH)

        input_text = driver.find_element(By.CSS_SELECTOR, "p[class=\"xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8\"]")
        input_text.send_keys(product_link)
        input_text.send_keys(Keys.ENTER)
        input_text.send_keys(title)
        input_text.send_keys(Keys.ENTER)
        # input_text.send_keys(description)
        pyperclip.copy(description)
        input_text.send_keys(Keys.SHIFT, Keys.INSERT)

        sleep(3)
        post_button = driver.find_element(By.CSS_SELECTOR, "div[aria-label=\"Post\"]").find_element(By.TAG_NAME, 'span')
        post_button.click()
        sleep(5)
        try:
            driver.find_element(By.CSS_SELECTOR, "div[aria-label=\"Not now\"]").find_element(By.TAG_NAME, 'span').click()
        except:
            pass
        sleep(20)
        driver.quit()
    return data