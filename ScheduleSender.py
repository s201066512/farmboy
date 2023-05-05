"""
Run this part every 24 hours 
I also need to check the value of latestShift and compare it to the current day
If the day of my shift is the current day, then send an email 

Run this part every hour
variable hasBeenChanged
Determine a way to tell if shift has been updated or cancelled
    I'll need to check all my shifts after the current day
    This means clicking on schedule and then figuring out which shift to 

Check if it says it has been updated or cancelled
    Set hasBeenChanged to true
If hasBeenChanged is true then send an email
    Set hasBeenChanged to false

Figure out how to send it at the right times
Do I need a loop and just use sleep() or wait()?

"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from datetime import timedelta, date
import smtplib
from email.message import EmailMessage
import re
while (True):
    # email setup
    msg = EmailMessage()
    msg['Subject'] = 'Shift Reminder'
    msg['From'] = "farmboyShiftReminder@gmail.com"
    msg['To'] = "aiden.ten30@gmail.com"

    tomorrow = date.today() + timedelta(days=1) # get current day

    # Enter email
    driver = webdriver.Firefox()
    driver.get("https://myfarmboy.ca/login/")
    email = driver.find_element(By.XPATH, "/html/body/div/div/div/div/form/div/div[1]/input")
    email.clear()
    email.send_keys("aiden.ten30@gmail.com")

    # Enter password
    password = driver.find_element(By.XPATH, "/html/body/div/div/div/div/form/div/div[2]/input")
    password.clear()
    password.send_keys("N@th@n1o")
    password.send_keys(Keys.RETURN)

    driver.implicitly_wait(10) # wait up to 10 seconds for page to load 

    latestShift = driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div/div[1]/div/div/p")
    latestShiftDay = re.findall(r'\d+', latestShift.text) # get all the numerical values 
    if latestShiftDay[0] == tomorrow: # check if I have a shift tomorrow
    # send email
        msg.set_content(latestShift.text)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("farmboyShiftReminder@gmail.com", "uittsrygrdlhouny")
        server.send_message(msg)
        server.quit()
    else:
        print("No Shift Tomorrow")

    driver.find_element(By.XPATH, "/html/body/div/div/div/nav/div/div/div[1]/div[3]/div/a[2]").click() # click on schedule
    time.sleep(10) # wait a bit
    old_shifts = re.findall(r'(\d{1,2}:\d{2} [AP]M) to (\d{1,2}:\d{2} [AP]M)', driver.page_source) # get the times
    time.sleep(3600) # wait (maybe an hour?)
    shifts = re.findall(r'(\d{1,2}:\d{2} [AP]M) to (\d{1,2}:\d{2} [AP]M)', driver.page_source) # get them again
    try:
        for x in range(len(shifts)): # loop through them
            if shifts[x] != old_shifts[x]: # see if anything was changed during that time
                print("Shift at " + str(old_shifts[x]) + " has been changed to " + str(shifts[x]))

                # if there were changes send an email with what was changed
                msg.set_content("Shift at " + str(old_shifts[x]) + " has been changed to " + str(shifts[x]))
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login("farmboyShiftReminder@gmail.com", "uittsrygrdlhouny")
                server.send_message(msg)
                server.quit()
    except IndexError:  
        print("IndexError (ignore)")

    """
    This will give me index out of bounds error if the old_shifts includes a week and shifts doesn't include that week
    I don't think that actually matters though, since after it runs again the weeks will be the same
    And then it'll be another week before that happens again. But during the week it'll work as expected
    So there might just be a slight delay
    Still need to run it constantly and figure out how I want to do that
    """
    driver.close()
    time.sleep(43200)