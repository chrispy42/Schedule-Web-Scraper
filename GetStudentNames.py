'''
This code got the names of the students by logging into my google account and scraping from the mailing list my shcool uses to send school wide emails
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import json

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

emailusername = 'exusername'
emailpassword = 'expassword'
student_names = []
#get to groups page
driver.get('https://groups.google.com/a/gouldacademy.org/forum/#!members/students-l')
'''
signin = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "gb_70"))
)
signin.click()
'''
loadcheck0 = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Email or phone"]'))
)
time.sleep(.5)
username = driver.find_element_by_xpath('//input[@aria-label="Email or phone"]')
username.send_keys(emailusername)
nextelement = driver.find_element_by_id("identifierNext")
nextelement.click()
loadcheck1= WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "password"))
)
password = driver.find_element_by_name('password')
time.sleep(1)
password.send_keys(emailpassword)
password.send_keys(Keys.RETURN)
loadcheck2= WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "lbMVLc"))
)
for i in range(3):
    time.sleep(1)
    nameElements = driver.find_elements_by_class_name('LnLepd')
    for i in range(len(nameElements)):
        student_names.append(nameElements[i].text)
    nextclick = driver.find_element_by_xpath('//div[@aria-label="Next page"]')
    nextclick.click()
    time.sleep(2)

print(str(len(student_names)) + ' results were found')
for i in range(len(student_names)):
    #student_names[i] = student_names[i][:student_names[i].find('joined')]
    #student_names[i] = student_names[i][0:len(student_names[i])-1]
    pass
print(student_names)
driver.quit()

studentjson = {
    'students': student_names
}

save = input('would you like to save this data as the current model? (y/n)')
if save == 'y':
    with open('studentnames.json', 'w') as f:
        json.dump(studentjson, f, indent=4)
