# import time for sleep function needs (waits)
import time

#import selenium to communicate with web
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert

#import tkinter for better user interface (pop up message boxs)
from tkinter import *
from tkinter import messagebox

# Using Chrome to access web
driver = webdriver.Chrome()
#go to VIS
#actual code
#driver.get('http://cticprod.visibility.com/Visibility/login')
#test code
driver.get('http://ctictest.visibility.com/Visibility/login')


#login
while driver.current_url == 'http://ctictest.visibility.com/Visibility/login':
#while driver.current_url == 'http://cticprod.visibility.com/Visibility/login':
    #ask login information
    username = input("VIS Username: ")
    password = input("VIS Password: ")

    #send login info
    # Select the username box
    user_box = driver.find_element_by_id('UserName')
    # Send username information
    user_box.send_keys(username)
    # Find password box
    pass_box = driver.find_element_by_id('Password')
    # Send password
    pass_box.send_keys(password)
    # Find login button
    login_button = driver.find_elements_by_xpath('//button[text()="Login to..."]')
    #click login
    for i in login_button:
        i.click()
    #wait to be let in
    time.sleep(2.5)
    #repeat if not the right login information

# Ask for Rev and part number
#make sure input is a valid Rev
check = False
while check == False:
    rev = input("Enter the new Rev: ")
    if rev == 'I' or rev == 'O'or rev == 'Q' or rev == 'S' or rev == 'X' or rev == 'Z' or rev.isupper() == False:
        check = False
        print("That input cannot be used")
    else:
        check = True
## IDEA: add protections here for the part number to minimize possible damage by user error
while True:
    part_num = input("Enter the Part Number: ")
    #message box confirming the user has imputed the right Number
    if messagebox.askyesno("askquestion", "Is " + part_num + " the part number you want to enter?") == True:
        break
#go to parts list
#test code
driver.get('http://ctictest.visibility.com/VisEN/lookasidepart.aspx?')
#actual code
#driver.get('http://cticprod.visibility.com/VisEN/lookasidepart.aspx?')

#enter part number and search
#start with a while and try to prevent errors
#method to check for partNum_box
def partNumCheck():
    try:
        partNum_box = driver.find_element_by_id('Srch_ctrlPART_X_SEARCH')
        return True
    except:
        return False
while True:
    if partNumCheck():
        break
    else:
        time.sleep(.25)

#once it is possible find the box and send keys
partNum_box = driver.find_element_by_id('Srch_ctrlPART_X_SEARCH')
partNum_box.send_keys(part_num)
#find the search button and click
search_button = driver.find_element_by_id('lnkApply')
search_button.click()
search_button.click()

#get the number of pages to 1
#find the number of found items
#Use While and true again to prevent errors
#method to check for found_box
def foundBoxCheck():
    try:
        found_box = driver.find_element_by_id('pgng_lblRecFound')
        return True
    except:
        return False
while True:
    if foundBoxCheck():
        break
    else:
        time.sleep(.25)

#runs a loop for a short amount of time to make sure the right number is found
found_box = driver.find_element_by_id('pgng_lblRecFound')
count = 0
while True:
    if int(found_box.text) != 0 or count >= 5:
        break
    else:
        time.sleep(.25)
        count += .25
#determine how many parts were found and send that number to the rec_box
found_num = int(found_box.text)
#print(found_num)
digits = len(str(found_num))
#set number per page to the found number
rec_box = driver.find_element_by_id('pgng_txtRecOnPage')
rec_box.send_keys(Keys.BACKSPACE * 3)
rec_box.send_keys(100)
page_num = int(found_num/100 + 1)


#for loop to run through every item in list
for x in range(found_num):
    #switch page if necessary
    if (x) % 100 == 0 and x != 0:
        for i in range(99):
            listnum = x-i
            listnum_str = str(listnum)
            part = driver.find_element_by_id('grdLA_'+listnum_str)
            part.click()
        next_page = driver.find_element_by_id('pgng_btnNext')
        next_page.click()

    #click part
    listnum = x+2
    listnum_str = str(listnum)
    #method to find next part
    def partCheck():
        try:
            part = driver.find_element_by_xpath('//*[@id="grdLA_'+ str(x + 2) +'"]/div[1]')
            return True
        except:
            return False
    while True:
        if partCheck():
            break
        else:
            time.sleep(.25)
    part = driver.find_element_by_xpath('//*[@id="grdLA_'+ str(x + 2) +'"]/div[1]')
    part.click()
    #makes sure part has actually been selected by checking if it is highlighted
    while True:
        if driver.find_element_by_xpath('//*[@id="grdLA_'+ str(x + 2) +'"]/div[1]').value_of_css_property("background-color") == 'rgba(98, 163, 255, 1)':
            break
        else:
            print(driver.find_element_by_xpath('//*[@id="grdLA_'+ str(x + 2) +'"]/div[1]').get_property('title'))
            time.sleep(.25)
            part.click()
    #click actions and rev hist. to navigate to pop up to change rev
    actions_button = driver.find_elements_by_xpath('//*[@id="vlsMenu_LAUNCH1"]/span[1]')
    for i in actions_button:
        i.click()
    rev_button = driver.find_elements_by_xpath('//*[@id="vlsMenu_launchpanel1"]/div[1]')
    def revhistCheck():
        try:
            for i in rev_button:
                i.click()
            return True
        except:
            return False
            print('here')
    while True:
        if revhistCheck():
            break
        else:
            time.sleep(.25)

#checks to make sure you get the pop up window and if not after a certain ammount of time trys to click again
    timepass = 0
    while len(driver.window_handles) == 1:
        time.sleep(1)
        timepass += 1
        if timepass >= 5:
            while True:
                for i in actions_button:
                    i.click()
                if revhistCheck():
                    break
                else:
                    time.sleep(.25)

    #switch windows
    window_before = driver.window_handles[0]
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)

    #find add sign and click
    #Use while try here
    def addCheck():
        try:
            add_button = driver.find_element_by_css_selector('span.mif-plus')
            return True
        except:
            return False
    while True:
        if addCheck():
            break
        else:
            time.sleep(.25)
    add_button = driver.find_element_by_css_selector('span.mif-plus')
    add_button.click()

    #set to new rev
    """
    def revCheck():
        try:
            rev_box = driver.find_element_by_id('txtRevision')
            return True
        except:
            return False
    while True:
        if revCheck():
            break
        else:
            time.sleep(.25)
    rev_box = driver.find_element_by_id('txtRevision')
    rev_box.send_keys(rev)
    """
    #save changes
    save_button = driver.find_elements_by_xpath('//*[@id="grdRevisions_-1"]/div[1]/span[1]')
    def saveClickCheck():
        try:
            for j in save_button:
                j.click()
            return True
        except:
            return False
    while True:
        if saveClickCheck():
            break
        else:
            time.sleep(.25)
    #commented out section for testing without any rev input
    def alertCheck():
        try:
            Alert(driver).accept()
            return True
        except:
            return False
    while True:
        if alertCheck():
            break
        else:
            time.sleep(.25)
    #Alert(driver).accept()
    driver.close()
    driver.switch_to.window(window_before)
    time.sleep(1)

#messagebox responds if done
messagebox.showinfo("information","The program has finished running")
