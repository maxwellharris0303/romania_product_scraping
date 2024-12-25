from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import *
from time import sleep
import extractData


EMAIL_ADDRESS = "alexandru.szoke@cesiro.com"
PASSWORD = "Optim74361"


options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get("https://www.juguar.ro/")

WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type=\"email\"]")))

email_input = driver.find_element(By.CSS_SELECTOR, "input[type=\"email\"]")
email_input.send_keys(EMAIL_ADDRESS)
password_input = driver.find_element(By.CSS_SELECTOR, "input[type=\"password\"]")
password_input.send_keys(PASSWORD)

submit_button = driver.find_element(By.CSS_SELECTOR, "button[type=\"submit\"]")
submit_button.click()

WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[x-data=\"homeCategories()\"]")))
categories_element = driver.find_element(By.CSS_SELECTOR, "div[x-data=\"homeCategories()\"]")
all_cateogories = categories_element.find_elements(By.CSS_SELECTOR, "li[class=\"flex flex-wrap w-full\"]")
print(len(all_cateogories))

all_main_urls = []
for li_element in all_cateogories:
    all_main_urls.append(li_element.find_element(By.TAG_NAME, "a").get_attribute("href") + "?sortBy=position&perPage=100")

for main_url in all_main_urls:
    driver.get(main_url)

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class=\"flex w-8/12 md:w-18 p-1\"]")))

    all_product_urls = []
    while(True):
        product_elements = driver.find_elements(By.CSS_SELECTOR, "div[class=\"flex w-8/12 md:w-18 p-1\"]")
        print(len(product_elements))
        for product_element in product_elements:
            all_product_urls.append(product_element.find_element(By.TAG_NAME, "a").get_attribute('href'))
        try:
            next_page_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label=\"Next &raquo;\"]")
            driver.execute_script("arguments[0].scrollIntoView();", next_page_button)
            next_page_button.click()
        except:
            break
        sleep(5)
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class=\"flex w-8/12 md:w-18 p-1\"]")))

    product_options = webdriver.ChromeOptions()
    product_options.add_argument("--headless=new")
    product_driver = webdriver.Chrome(options=product_options)
    product_driver.maximize_window()
    product_driver.get("https://www.juguar.ro/")
    WebDriverWait(product_driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type=\"email\"]")))

    email_input = product_driver.find_element(By.CSS_SELECTOR, "input[type=\"email\"]")
    email_input.send_keys(EMAIL_ADDRESS)
    password_input = product_driver.find_element(By.CSS_SELECTOR, "input[type=\"password\"]")
    password_input.send_keys(PASSWORD)

    submit_button = product_driver.find_element(By.CSS_SELECTOR, "button[type=\"submit\"]")
    submit_button.click()
    WebDriverWait(product_driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[x-data=\"homeCategories()\"]")))
    for product_url in all_product_urls:
        print(product_url)
        try:
            extractData.extract_data(product_driver, product_url)
        except:
            try:
                product_driver.quit()
            except:
                pass
            product_options = webdriver.ChromeOptions()
            product_options.add_argument("--headless=new")
            product_driver = webdriver.Chrome(options=product_options)
            product_driver.maximize_window()
            product_driver.get("https://www.juguar.ro/")

            WebDriverWait(product_driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type=\"email\"]")))

            email_input = product_driver.find_element(By.CSS_SELECTOR, "input[type=\"email\"]")
            email_input.send_keys(EMAIL_ADDRESS)
            password_input = product_driver.find_element(By.CSS_SELECTOR, "input[type=\"password\"]")
            password_input.send_keys(PASSWORD)

            submit_button = product_driver.find_element(By.CSS_SELECTOR, "button[type=\"submit\"]")
            submit_button.click()
            WebDriverWait(product_driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[x-data=\"homeCategories()\"]")))

            pass



