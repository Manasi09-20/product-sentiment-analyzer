from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Path to chromedriver
service = Service("driver/chromedriver.exe")

# Start browser
driver = webdriver.Chrome(service=service)

# Open website
driver.get("https://www.google.com")

input("Press Enter to close browser...")
driver.quit()
