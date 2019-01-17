# -*- coding: utf-8 -*-

########################## Version 2 Update Note ##################################
# 1. Version 2 added antireq and coreq, both are definitely needed for my future  #
#    study sequence planning.                                                     #
# 2. Changed the info collection for prereq from a set index (i.e. index number 5)#
#    into searching by for loop, for prereq, antireq, and coreq                   #
# Version 3 Plan: Get which course prefix belong to which faculty by scraping this#
# this website: https://ugradcalendar.uwaterloo.ca/page/Course-Descriptions-Index #
###################################################################################

import requests
import csv
from bs4 import BeautifulSoup

########################## Get Course Prefix ##################################
# Get prefix from: schedule of classes for undergraduate students
course_prefix = []

# Access the course prefix website
prefix_page = requests.get('http://www.adm.uwaterloo.ca/infocour/CIR/SA/under.html')

# Parse the accessed website page
prefix_soup = BeautifulSoup(prefix_page.text, 'html.parser')

# Since all prefix are under select tag in HTML, scrap the information by the select tag.
all_select = prefix_soup.find_all('select')
second_select = all_select[1]
second_select_all_option = second_select.find_all('option')
for i in second_select_all_option:
    course_prefix.append(i.get('value'))


##################### Record All Undergrad Course Info ################################
# use prefix list from previous section, to get all undergraduate courses in UW

# Write column headers into the Excel file
myfile = open('UWAllCourseList_v2.csv', 'w')
f = csv.writer(myfile)
f.writerow(['Prefix of Website','Course Code', 'Course Name', 'Course Description', 'Prereq','Antireq','Coreq'])

# ecount: the number of exceptions
ecount = 0

# Loop through all UW course website by course prefix
for prefix in course_prefix:
    print("Prefix '"+prefix+"' starts")

    # Access the current prefix course web page
    page = requests.get('http://www.ucalendar.uwaterloo.ca/1819/COURSE/course-'\
                        + prefix + '.html')
    soup = BeautifulSoup(page.text, 'html.parser')

    # Get all course table tag by BeautifulSoup parsing
    a = soup.find_all('table')
    useful_table_list = a#[4:len(a)-1]

    # Get and record course information by looping though the list of course table tag
    for course in useful_table_list:
        preq = 'None'
        anti = 'None'
        coreq = 'None'
        try:
            code = course.find('a').get('name')
            #print(code + ' starts')
            name = course.find_all('b')[1].contents[0]
            description = course.find_all('td')[3].contents[0]
            td_lst = course.find_all('td')
            for i in range(len(td_lst)):
                if i >= 4:
                    try:
                        if 'Prereq:' in td_lst[i].contents[0].contents[0]:
                            preq = td_lst[i].contents[0].contents[0]
                    except:
                        preq = 'ERROR!!!'
                    try:
                        if 'Antireq:' in td_lst[i].contents[0].contents[0]:
                            anti = td_lst[i].contents[0].contents[0]
                    except:
                        anti = 'ERROR!!!'
                    try:
                        if 'Coreq:' in td_lst[i].contents[0].contents[0]:
                            coreq = td_lst[i].contents[0].contents[0]
                    except:
                        preq = 'ERROR!!!'
                    
            #print("prefix: "+prefix+'\n'+"code: "+code+'\n'+"preq: "+preq+'\n'+"anti: "+anti+'\n'+"coreq: "+coreq+'\n'+"desc"+description
            f.writerow([prefix, code, name, description, preq, anti, coreq])
        except:
            ecount += 1

# Prints out the progress
print('total useless data = ' + str(ecount))
print('Work Done')
myfile.close()
