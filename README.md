# AutoEnrollerYorku
A python selenium script which attempts to enroll in a course periodically at a user set interval.

---
### Instructions for Use

1. Download chromedriver, make sure to download the one that matches your chrome version. This will likely be the stable chromedriver win64 from [here](https://googlechromelabs.github.io/chrome-for-testing/#stable). Put the chromedriver.exe in the same directory that you place main.py in.

2. Download/import the file "main.py" from this repository.

3. install selenium, `pip install selenium` in console, as well as customtkinter `pip install customtkinter`. 

4. Run the file. fill in the parameters - 
    Type "chrome://version" into your chrome browser to find the profile number (you'll find it in the "profile path" section).
    Don't set the time between attempts too low, YorkU's REM might time you out or ban you for spamming.

5. Close google chrome if opened, start the script

Note: May have to change line 170. it is currently set for Fall/Winter 2024-2025. 

---

### Future plans

1. Allow the script to run headless, without a Chrome UI.

2. Allow the script to run while another Chrome window is open.

3. Create a script that instead checks VSB for an empty space in a course, and either alerts the user when a space is found or enrolls on its own.