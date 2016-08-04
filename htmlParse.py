'''
Created on February 10, 2016

@author: Wes Bosman
        This program takes the text from the HTML source code of a web page. 
        It then scans the text and looks for email addresses and phone numbers
        based on regular expressions. 
        It uses re.search instead of find all so it will only list the first phone number 
        and email address found on that page. 
'''
# -*- coding: utf-8 -*-
import urllib2
import re
import unittest
import urllib
import os, sys, cStringIO
#from PIL import Image
#from pytesser import *
from bs4 import BeautifulSoup

def welcome_msg():
    # Have the user enter the name of the web site
    print "+---------------------------------------------------------+"
    print "| \tWelcome, This program can parse                   |"
    print "| email addresses and phone numbers from web site URL's.  |"
    print "| Enter an HTML address ""example: google.com""               |"
    print "| \tPlease type quit to exit.                         |"                
    print "+---------------------------------------------------------+"
    
def start_webpage(website):
    if website != "quit":
        print " Parsing information from %s..." % website
        # Add http:// to the front and backslash at the end.
        web = "http://%s/" % website
        # Open up a socket connection and grab the source code.
        try:
            sock = urllib2.urlopen(web)   
            htmlSource = sock.read()
            sock.close()
        except:
            print " Sorry could not resolve web page."
    
        # Beautiful Soup makes the source code easy to read.
        # this was lxml in linux changed it in windows to html.parser
        soup = BeautifulSoup(htmlSource, "html.parser")
        
        # get all the text from the web page to find phone numbers and email
        whole_page = (soup.get_text())

        print "+---------------------------------------------------------+"
        print " Press i to find and download the URL's images"
        print " Press s to display the URL's source code"
        print " Press e to find email addresses within the URL"
        print " Press p to find phone numbers within the URL"
        print "+---------------------------------------------------------+"

        
        case = raw_input(" Enter a letter: ")
        
        if case == "i":
            get_images(soup)
        
        elif case == "s":
            get_source(soup)

        elif case == "e":
            get_email(whole_page)

        elif case == "p":
            get_phone_number(whole_page)

        else:
            print " Unknown letter entered: %s" %(case)
        
    elif website == "quit":
        print " Goodbye."
        exit(0)

def get_phone_number(whole_page):
    try:
        print "+---------------------------------------------------------+"
        phone = re.search('(\(?[0-9]{3}\)?)?(\-|\s)[0-9]{3}(\-|\s)[0-9]{4}', whole_page).group()
        print " Phone:   %s" % phone
        print "+---------------------------------------------------------+"
    except Exception, ex:
        print " No Phone Numbers Found."
        print " Exception thrown: " + str(ex)


def get_email(whole_page):
    try:
        print "+---------------------------------------------------------+"
        email = re.search('\S*@\S*', whole_page).group()
        print " Email:   %s" % email
        print "+---------------------------------------------------------+"
            
    except Exception, ex:
        print " No email found."
        print " Exception thrown: " + str(ex)


def get_source(soup):
    # This can throw a character reference error.
    print "+---------------------------------------------------------+"
    print soup.prettify()
    print "+---------------------------------------------------------+"

def get_images(soup):
    # get the images names as strings
    print "+---------------------------------------------------------+"
    print " Finding a list of images from website. "
    images = [img for img in soup.findAll('img')]
    print " Number of images found: " + (str(len(images)))
        
    html_paths = []
        
    # get the sources for the images
    image_links = [each.get('src') for each in images]
    for each in image_links:
        filename = each.split('/')[-1]
        urllib.urlretrieve(each, filename)
        html_paths.append(str(each))
        print " " + str(each)
        
        """
        filez = cStringIO.StringIO(urllib.urlopen(str(each)).read())
        open_img = Image.open(filez)
        text_from_img = image_to_string(open_img)
        text_from_img = image_file_to_string(open_img)
        print text_from_img
        """
    print "+---------------------------------------------------------+"



def start():
    web_site = raw_input(" Enter a valid HTML address: ")
    #true_web = re.match("\S+\.\S+|quit", web_site)
    # Pass the web site to the start function if it is a valid web site or if quit is entered. 
    if re.match("\S+\.\S+|quit", web_site):
        start_webpage(web_site)
    else:
        print " A valid URL was not entered. "
        start()
        
# Run the welcome function on the start of the program
welcome_msg()
# Run the start function that recursively checks for valid input before sending info to start_webpage.
start()


""" Testing Below """
#class MyTest(unittest.TestCase):
#    def test(self):
#        self.assertEqual(start_webpage("www.jakecorfield.com"), 
#                         "Website: www.jakecorfield.com", "Web site test passed.")


    
    
