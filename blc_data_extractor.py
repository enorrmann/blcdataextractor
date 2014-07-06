import yaml
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

default_timeout = 10

f = open('config.yaml')
env = yaml.load(f)
username = env["username"]
password = env["password"]
page_base = "https://bitlendingclub.com"

if not os.path.isfile('latest_investments_report.txt'):
    open('latest_investments_report.txt', 'w')

f = open('latest_investments_report.txt', 'a')

driver = webdriver.Chrome()

driver.get(page_base)

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

print "Loading first investments page"
driver.get(page_base + "/profile/investments")

investment_page_counter = 1
all_investment_page_data_extracted = False

while True:
    try:
        if not WebDriverWait(driver, default_timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, "next"))):
            # break if on last page (no more next links)
            if investment_page_counter > 1 or all_investment_page_data_extracted:
                break
            else:
                all_investment_page_data_extracted = True

        if investment_page_counter > 1:
            print "Loading investment page: " + str(investment_page_counter) 

        print "Grabbing all loan links from page"    

        loan_links = []

        for link in  driver.find_elements_by_xpath('//*/tr/td[2]/a'):
            loan_links.append(link.get_attribute("href"))

        for loan in loan_links:        

            print "Loading loan page: " + loan
            driver.get(loan)
            
            print driver.find_element_by_tag_name('h1').text
 
            print driver.find_element_by_class_name('last-row').text

            print "Writing out infos to file"
            f.write(driver.find_element_by_tag_name('h1').text + '\n')
            

        print "Returning to current investment listing page"
        driver.get(page_base + "/profile/investments/page/" + str(investment_page_counter))

        WebDriverWait(driver, default_timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, "next")))

        print "Loading investment page: " + str(investment_page_counter)
        driver.find_element_by_class_name('next').click()

        
        investment_page_counter += 1 

    except TimeoutException as e:
       print "Iterated through all investment pages"     
       break

driver.close()
f.close()
print "Completed cleanly"







