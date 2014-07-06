import yaml
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

default_timeout = 10

f = open('config.yaml')
env = yaml.load(f)
username = env["username"]
password = env["password"]

driver = webdriver.Chrome()

driver.get("https://bitlendingclub.com")

driver.find_element_by_id("login-button").click()

WebDriverWait(driver, default_timeout).until(
        EC.visibility_of_element_located((By.NAME, "email"))
    )

driver.find_element_by_name('email').send_keys(username)
driver.find_element_by_name('password').send_keys(password)
driver.find_element_by_name('password').send_keys(Keys.RETURN)

WebDriverWait(driver, default_timeout).until(
        EC.visibility_of_element_located((By.NAME, "code"))
    )

driver.find_element_by_name('code').send_keys(raw_input("Please enter your 2FA code: "))
driver.find_element_by_name('code').send_keys(Keys.RETURN)

WebDriverWait(driver, default_timeout).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "name-title"))
    )

print "Dashboard loaded"

driver.close()
