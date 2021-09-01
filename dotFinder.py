'''
This is the code that took the emails and put them in the url to scrape for the classes and save them to the json files. Once again the json files aren't 
in this repository because it has the emails and names of everyone in the school at the time
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import json


with open('studentnames.json') as f:
    student_names = json.load(f)
with open('teachernames.json') as f:
    teacher_names = json.load(f)
with open('studentemails.json') as f:
    student_emails = json.load(f)
with open('teacheremails.json') as f:
    teacher_emails = json.load(f)


student_names = student_names['students']
teacher_names = teacher_names['teachers']
student_emails = student_emails['studentemails']
teacher_emails = teacher_emails['teacheremails']

teacher_info = [[] for _ in range(len(teacher_names))]
teacher_usernames = []
student_info = [[] for _ in range(len(student_names))]
student_usernames = []
teacher_indexes = []


def getClasses(student_sample):
    DATE1 = '11/23/2020'
    DATE2 = '11/24/2020'
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    data = {}
    jsonids = []

    for q in range(len(student_sample)):
        #try:
            coursesElement = [[], [], [], [], [], []]

            driver.get(
                'https://secure.gouldacademy.org/SSMBPSchedule/MySchedule?id=' + student_sample[q][
                    1] + '&date=' + DATE1 + '&viewType=Day')
            time.sleep(5)
            try:

                print('alert accepted was tryed')
                button = driver.find_element_by_name('alert')
                button.click()
                # Switch the control to the Alert window
                obj = driver.switch_to.alert
                time.sleep(2)
                # Section 1
                # use the accept() method to accept the alert
                obj.accept()
                time.sleep(.5)
                # refresh the webpage
                driver.refresh()
                print('alert accepted')
            except:
                pass
            for i in range(3):
                links = WebDriverWait(driver, 1).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//div[@unselectable = "on"]'))
                )
                for j in range(len(links)):
                    try:
                        if links[j].get_attribute('textContent').find('[' + str(i + 1) + ']') > 0:
                            coursesElement[i] = (links[j].get_attribute('textContent'))
                            print(links[j].get_attribute('textContent'))


                    except:
                        pass

            driver.get(
                'https://secure.gouldacademy.org/SSMBPSchedule/MySchedule?id=' + student_sample[q][
                    1] + '&date=' + DATE2 + '&viewType=Day')
            for i in range(3):
                links = WebDriverWait(driver, 1).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//div[@unselectable = "on"]'))
                )
                for j in range(len(links)):
                    try:
                        if links[j].get_attribute('textContent').find('[' + str(i + 4) + ']') > 0:
                            coursesElement[i + 3] = (links[j].get_attribute('textContent'))


                    except:
                        pass
            for i in range(len(coursesElement)):
                if coursesElement[i] == []:
                    coursesElement[i] = 'free_dot'
                else:
                    coursesElement[i] = coursesElement[i][
                                        (str(coursesElement[i]).find(']')) + 2:(str(coursesElement[i]).find(':')) - 1]
            #print(coursesElement)
            student_sample[q].append(coursesElement)
            data[str(student_sample[q][0] + '.' + student_sample[q][1])] = coursesElement
            #print(coursesElement)
            jsonids.append(str(student_sample[q][0] + '.' + student_sample[q][1]))
        #except:
    #print(student_sample)
    data['jsonids'] = jsonids
    return(data)
    time.sleep(10)
    driver.quit()



def HasNumbers(input_string):
    return any(char.isdigit() for char in input_string)


for i in range(len(student_emails)):
    student_emails[i].find('@')
    student_usernames.append(student_emails[i][0:student_emails[i].find('@')])
for i in range(len(student_emails)):
    student_info[i].append(student_names[i])
    student_info[i].append(student_usernames[i])
for i in range(len(student_info)):
    if HasNumbers(student_info[len(student_info)-i-1][1]):
        pass
    else:
        student_info[len(student_info)-i-1] = 'teacher'
        teacher_indexes.append(len(student_info)-i-1)

for i in range(len(teacher_indexes)):
    del student_info[teacher_indexes[i]]

for i in range(len(teacher_info)):
    teacher_emails[i].find('@')
    teacher_usernames.append(teacher_emails[i][0:teacher_emails[i].find('@')])
for i in range(len(teacher_emails)):
    teacher_info[i].append(teacher_names[i])
    teacher_info[i].append(teacher_usernames[i])


people = input('students or teachers (s/t)')
if people == 's' or people == 't':
    pass
else:
    poeple = 's'

if people == 's':
    classjson = getClasses(student_info)
    save = input('would you like to save this data as the current model? (y/n)')
    if save == 'y':
        with open('StudentSchedules.json', 'w') as f:
            json.dump(classjson, f, indent=4)
elif people == 't':
    classjson = getClasses(teacher_info)
    save = input('would you like to save this data as the current model? (y/n)')
    if save == 'y':
        with open('TeacherSchedules.json', 'w') as f:
            json.dump(classjson, f, indent=4)
