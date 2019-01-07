# -*- coding: utf-8 -*-

import requests
import csv
from bs4 import BeautifulSoup

# Get prefix from: schedule of classes for undergraduate students
course_prefix = []
prefix_page = requests.get('http://www.adm.uwaterloo.ca/infocour/CIR/SA/under.html')
prefix_soup = BeautifulSoup(prefix_page.text, 'html.parser')
all_select = prefix_soup.find_all('select')
second_select = all_select[1]
second_select_all_option = second_select.find_all('option')
for i in second_select_all_option:
    course_prefix.append(i.get('value'))
##############################################################################
# use prefix list from previous section, to get all undergraduate courses in UW
    
myfile = open('UWAllCourseList.csv', 'w')
f = csv.writer(myfile)
f.writerow(['Prefix of Website','Course Code', 'Course Name', 'Course Description', 'Prereq'])



ecount = 1;
for prefix in course_prefix:
    
    page = requests.get('http://www.ucalendar.uwaterloo.ca/1819/COURSE/course-'\
                        + prefix + '.html')
    
    soup = BeautifulSoup(page.text, 'html.parser')
     
    a =  soup.find_all('table')
    
    useful_table_list = a#[4:len(a)-1]
    
    for course in useful_table_list:
        try:
            code = course.find('a').get('name')
            name = course.find_all('b')[1].contents[0]
            description = course.find_all('td')[3].contents[0]
            try:
                preq = course.find_all('td')[5].contents[0].contents[0]
            except:
                preq = 'course prereq cannot be found'
            f.writerow([prefix, code, name, description, preq])
        except:
            print('page: '+ prefix +'\nerror number: '+str(ecount)+'\n')
            ecount = ecount + 1
    ecount = 1
myfile.close()