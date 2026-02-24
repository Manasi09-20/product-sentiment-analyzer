from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sentiment import analyze_sentiment
import os
import time


def get_reviews(product):

    # driver path
    current_dir = os.path.dirname(__file__)
    driver_path = os.path.join(current_dir, "driver", "chromedriver.exe")
    service = Service(driver_path)

    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)

    # open flipkart
    driver.get("https://www.flipkart.com")

    # close login popup
    try:
        close_btn = wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'✕')]"))
        )
        close_btn.click()
    except:
        pass

    # search product
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    search_box.send_keys(product)
    search_box.send_keys(Keys.RETURN)

    # open first product
    products = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href,'/p/')]"))
    )
    products[0].click()

    # switch tab
    driver.switch_to.window(driver.window_handles[1])

    # try opening review page
    try:
        all_reviews = wait.until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'reviews')]"))
        )
        driver.execute_script("arguments[0].click();", all_reviews)
    except:
        print("Review button not found — collecting from product page")

    # scroll to load reviews
    for _ in range(4):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # collect reviews
    reviews = driver.find_elements(By.XPATH, "//div[contains(@class,'t-ZTKy')]")

    review_list = []
    for r in reviews[:10]:
        review_list.append(r.text)

    driver.quit()
    return review_list


# TESTING
if __name__ == "__main__":

    data = get_reviews("iphone 13")

    print("\n------ SENTIMENT RESULTS ------\n")

    if len(data) == 0:
        print("No reviews collected")
    else:
        for i, r in enumerate(data, 1):
            sentiment = analyze_sentiment(r)
            print(f"{i}. {r}")
            print("Sentiment:", sentiment, "\n")
