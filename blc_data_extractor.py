import yaml
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

#navigate to investments page
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

        print "Loading investment page: " + str(investment_page_counter)

        #grab all investment links from page
        print "Grabbing all investment links from page"    

        #for each investment link

            #load up investment page
        print "Loading each loan page"

            #write out infos to txt file
        print "Writing out infos to file"

        #return to previous investment listing page
        driver.get(page_base + "/profile/investments/page/" + str(investment_page_counter))
        print "Returning to current investment listing page"
        WebDriverWait(driver, default_timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, "next")))

        driver.find_element_by_class_name('next').click()
        print "Loading investment page: " + str(investment_page_counter)

        
        investment_page_counter += 1 

    except TimeoutException as e:
       print "Iterated through all investment pages"     
       break

driver.close()
print "Completed cleanly"







