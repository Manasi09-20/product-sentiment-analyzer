from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time


def get_flipkart_reviews(product_url):

    current_dir = os.path.dirname(__file__)
    driver_path = os.path.join(current_dir, "driver", "chromedriver.exe")
    service = Service(driver_path)

    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 15)

    driver.get(product_url)
    driver.maximize_window()

    # Close login popup if appears
    try:
        close_btn = wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'✕')]"))
        )
        close_btn.click()
    except:
        pass

    # Scroll to load reviews
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # Try clicking "All Reviews"
    try:
        review_button = wait.until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'reviews')]"))
        )
        driver.execute_script("arguments[0].click();", review_button)
        time.sleep(3)
    except:
        pass

    # Collect reviews
    reviews = driver.find_elements(By.XPATH, "//div[contains(@class,'t-ZTKy')]")

    review_list = []
    for r in reviews[:10]:
        review_list.append(r.text)

    driver.quit()

    return review_list