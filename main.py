import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from random import randrange

numOfAttempts=5
timeBetweenAttempts=1800 #this is in Seconds

service = Service(executable_path="chromedriver.exe")
myoptions = webdriver.ChromeOptions()

myoptions.add_argument(f"--user-data-dir=C:\\Users\\farha\\AppData\\Local\\Google\\Chrome\\User Data")
myoptions.add_argument("profile-directory=Profile 7")
driver = webdriver.Chrome(service=service, options=myoptions)
sleep(4)

for x in range(2):
    driver.get("https://wrem.sis.yorku.ca/Apps/WebObjects/REM.woa/wa/DirectAction/rem")
    sleep(7)
    # Only uncomment below if ur username and password isnt pre-entered by google
    # driver.find_element(By.ID, "mli").send_keys("your username")
    # sleep(5)
    # driver.find_element(By.NAME, "password").send_keys("your password.")
    # sleep(5)
    driver.find_element(By.NAME,"dologin").click()
    sleep(15)
    driver.find_element(By.NAME,'5.5.1.27.1.11.0').click()
    sleep(5)
    driver.find_element(By.XPATH, "//select[@name='5.5.1.27.1.11.0']/option[text()='FALL/WINTER 2024-2025 UNDERGRADUATE STUDENTS']").click()
    sleep(10)
    driver.find_element(By.NAME, "5.5.1.27.1.13").click()
    sleep(10)
    driver.find_element(By.NAME, "5.1.27.1.23").click()
    sleep(10)
    driver.find_element(By.NAME,'5.1.27.7.7').send_keys("T97S01")
    sleep(10)
    driver.find_element(By.NAME,'5.1.27.7.9').click()
    sleep(10)
    driver.find_element(By.NAME, '5.1.27.11.11').click()
    sleep(10)
    #At this point, you either successfully enrolled or failed to enroll.
    #Implement: break if fail message is not found
    isFound = driver.find_elements(By.XPATH, "//*[contains(text(), 'The course has not been added.')]")
    sleep(4)
    if not isFound:
        break

    driver.close()
    sleep(timeBetweenAttempts)

