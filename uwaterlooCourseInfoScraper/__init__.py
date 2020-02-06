# -*- coding: utf-8 -*-
import requests
import csv
from bs4 import BeautifulSoup

#!######################### Get Course Prefix ##################################
# * Get prefix from: schedule of classes for undergraduate students
def getPrefix():
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
    return course_prefix

def requestCourseEnroll(sess, subject, cournum):
    if not sess or not subject or not cournum:
        print("ERROR: please input ALL of the sess, subject, cournum parameters")
        return None
    else:
        url = 'http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl'

        headers = {"Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip,deflate",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "45",
        "Origin": "http://www.adm.uwaterloo.ca",
        "Connection": "keep-alive",
        "Referer": "http://www.adm.uwaterloo.ca/infocour/CIR/SA/under.html",
        "Upgrade-Insecure-Requests": "1"}
            
        data = "level=under&sess=%s&subject=%s&cournum=%s" % (sess, subject, cournum)

        req = requests.post(url, headers=headers, data=data)

        if req.status_code == requests.codes.ok:
            print("Request successful")
            return req
        else:
            print("Request ERROR: %s" % req.status_code)
            return req