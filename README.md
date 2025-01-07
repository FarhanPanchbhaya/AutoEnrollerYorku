# AutoEnrollerYorku
A python selenium script which attempts to enroll in a course periodically at a user set interval.

## Instructions for Use

1. Download chromedriver, make sure to download the one that matches your chrome version. (Can find a short guide on how to do this on youtube). 

2. Download/import the file "main.py" from this repository.

3. install selenium, "pip install selenium" in console, as well as customtkinter "pip install customtkinter". 

4. Run the file. fill in the parameters - 
    Type "chrome://version" into your chrome browser to find the profile number (you'll find it in the "profile path" section).
    Don't set the time between attempts too low, YorkU's REM might time you out or ban you for spamming.

5. Close google chrome if opened, start the script

