'''
This code logged into my google account and got the emails of everyone. The way it did this was actually by composing an email, typing in the persons name, 
and then pulling the first email on the drop down list that google offers. Its possibly the most inprecise solution to any problem ever but somehow it 
worked astonishingly well at the time. There is definitly a better way to do this but it felt quite creative at the time
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

username = 'exusername'
password = 'expassword'



with open('studentnames.json') as f:
    studentnamesjson = json.load(f)
with open('teachernames.json') as f:
    teachernamesjson = json.load(f)

student_names = studentnamesjson['students']
teacher_names = teachernamesjson['teachers']

people = input('students or teachers (s/t)')
if people == 's' or people == 't':
    pass
else:
    poeple = 's'

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get('https://mail.google.com/mail/u/0/#inbox')
def GetEmailsForList(input_list):
    emails = []
    timeoutprevent = 1
    fails = 0

    def sign_into_google():
        time.sleep(.5)
        username = driver.find_element_by_xpath('//input[@aria-label="Email or phone"]')
        username.send_keys(username)
        nextelement = driver.find_element_by_id("identifierNext")
        nextelement.click()
        loadcheck1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password = driver.find_element_by_name('password')
        time.sleep(1)
        password.send_keys(password)
        password.send_keys(Keys.RETURN)

    sign_into_google()
    compose_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class = "T-I T-I-KE L3"]'))
    )
    compose_button.click()


    for i in range(len(input_list)):
        timeoutprevent = 1
        skip = True
        emailTextBox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'textarea'))
        )
        emailTextBox.click()
        emailTextBox.send_keys(input_list[i])
        time.sleep(.5)
        try:
            testemail = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class = "Sr"]'))
            )
        except:
            emails.append('null')
            print('no email found')
            fails += 1
            for i in range(40):
                emailTextBox.send_keys(Keys.BACKSPACE)
            skip = False
        if skip:
            for i in range(timeoutprevent):
                try:
                    print(testemail.get_attribute('textContent'))
                    emails.append(testemail.get_attribute('textContent'))
                except:
                    timeoutprevent += 1
            for i in range(40):
                emailTextBox.send_keys(Keys.BACKSPACE)
    print('emails for ' + str(fails) + ' name(s) were not found')
    print(emails)
    driver.quit()
    return emails
if people == 's':
    studentemailsjson = {
        'studentemails': GetEmailsForList(student_names)
    }
    save = input('would you like to save this data as the current model? (y/n)')
    if save == 'y':
        with open('studentemails.json', 'w') as f:
            json.dump(studentemailsjson, f, indent=4)

if people == 't':
    teacheremailsjson = {
        'teacheremails': GetEmailsForList(teacher_names)
    }
    save = input('would you like to save this data as the current model? (y/n)')
    if save == 'y':
        with open('teacheremails.json', 'w') as f:
            json.dump(teacheremailsjson, f, indent=4)
