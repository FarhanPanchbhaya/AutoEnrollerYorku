# AutoEnrollerYorku
A python selenium script which attempts to enroll in a course periodically at a user set interval.


## Instructions for Use

1. Download Pycharm, VScode, or any editor where you can edit and run the code easily.

2. Download chromedriver, make sure to download the one that matches your chrome version. (Can find a short guide on how to do this on youtube). 

3. Download/import the file "main.py" from this repository.

4. install selenium, "pip install selenium" in console. Can also find a guide on youtube.

5. Open the main.py file, a few changes are required.

6. Change numOfAttempts and timeBetweenAttempts (lines 8 and 9) if so desired. Do not set the timeBetweenAttempts too low, as york's system might ban or time you out for spamming the REM.

7. In line 14, use your own username for the file path to "user data". The rest should remain the same.

8. In line 15, change the profile to whichever you use for york. This is done to bypass 2FA.

9. Change the year in line 31 if required.

10. Use EITHER line 35 or 36. 35 to add a course, 36 to transfer sections.

11. Enter your course catalogue number (the one that you would enter into REM) into line 39.

12. Close your google chrome browser if open. 
13. Run the script.
