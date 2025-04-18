# AutoEnrollerYorku

A Python script using Selenium that automatically attempts to enroll into the desired York University course when an empty space is found.

## Setup Instructions

### Setting up a Virtual Environment (optional)

```powershell
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# Install required packages
pip install -r requirements.txt
```

If you prefer not to use a virtual environment:

```powershell
# Install required packages globally
pip install -r requirements.txt
```

### Chrome WebDriver Setup

1. Download the appropriate ChromeDriver from [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/#stable)
   - Make sure to match your Chrome browser version
   - Download the stable chromedriver (win64)
2. Place `chromedriver.exe` in the same directory as `VSBChecker.py`

## Usage Instructions

### Direct Enrollment (main.py)

1. Activate your virtual environment if you created one, otherwise move to step 2 (see above)
2. Run the script: `python main.py`
3. Fill in the parameters in the application:
   - To find your Chrome profile path/number, type `chrome://version` in Chrome
   - Look for "Profile Path" in the information displayed
   - Don't set attempts too frequently to avoid timing out or being banned
4. Close any running Chrome instances before starting the script
5. Click Start to begin the enrollment process

> **Note:** The script is currently configured for Fall/Winter 2024-2025. You may need to modify line 170 for different academic terms.

### Course Availability Checker (VSBChecker.py)

1. Activate your virtual environment if you created one (see above)
2. Run the script: `python VSBChecker.py`
3. Fill in the parameters in the application:
   - To find your Chrome profile path/number, type `chrome://version` in Chrome
   - Look for "Profile Path" in the information displayed
   - Check Interval (seconds between availability checks)
   - Session Duration (minutes before a new browser session is created, leave at 15 if unsure)
4. Close any running Chrome instances before starting the script
5. Click "Start Checking" to begin monitoring for course availability
6. The script will:
   - Check Visual Schedule Builder (VSB) for course availability
   - Refresh the browser session periodically to prevent timeouts
   - Continue checking until a spot is found or you click "Stop"
   - Attempt enrollment automatically when a spot becomes available

> **Note:** The script is currently configured for Summer 2025. You need to modify line 316-317 for different academic terms. [value 0 is Fall/Winter undergrad, value 1 is Grad or Osgoode students, value 2 is Summer]


## Requirements

- Python 3.6+
- Chrome browser
- Libraries:
  - selenium
  - beautifulsoup4
  - customtkinter
