import yaml
import os
import BeautifulSoup
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

if not os.path.isfile('latest_investments_report.csv'):
    open('latest_investments_report.csv', 'wb')

f = open('latest_investments_report.csv', 'wb')

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

driver.get(page_base + "/profile/investments")

investment_page_counter = 1
all_investment_page_data_extracted = False
        
f.write("Title,# Payments,Payments made,Payments remaining,Total invested,Total received,Total remaining,Next payment\n")

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

        loan_links = []

        for link in  driver.find_elements_by_xpath('//*/tr/td[2]/a'):
            loan_links.append(link.get_attribute("href"))

        for loan in loan_links:        

            payments = []

            driver.get(loan)
            
            loan_title = driver.find_element_by_xpath('//h1').text.split('\n')[0].strip()

            payment_rows = driver.find_elements_by_xpath('(//tbody)[2]/tr')

            for row in payment_rows:
                payments.append([column.text for column in row.find_elements_by_tag_name('td')])

            number_of_payments = len(payment_rows) - 1 
            payments_made = sum([1 for row in payments[:-1] if row[2] != '- - -'])
            payments_remaining = number_of_payments - payments_made

            total_invested = payments[-1][6]

            total_received = sum([float(row[3]) for row in payments[:-1] if row[2] != '- - -'])

            total_remaining = sum([float(row[3]) for row in payments[:-1] if row[2] == '- - -'])

            next_payment = ""

            if total_remaining > 0:
                next_payment = [row[1] for row in payments[:-1] if row[2] == '- - -'][0]

            print payments_made
            print payments

            f.write("{0},{1},{2},{3},{4},{5},{6},{7}".format(
                loan_title.replace(',','.'),
                number_of_payments,
                payments_made,
                payments_remaining,
                total_invested,
                total_received,
                total_remaining,
                next_payment
            ) + "\n")

        driver.get(page_base + "/profile/investments/page/" + str(investment_page_counter))

        WebDriverWait(driver, default_timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, "next")))

        driver.find_element_by_class_name('next').click()
        
        investment_page_counter += 1 

    except TimeoutException as e:
       print "Iterated through all investment pages"     
       break

driver.close()
f.close()
print "Completed cleanly"
