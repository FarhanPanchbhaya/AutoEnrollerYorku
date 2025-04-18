# AutoEnrollerYorku

A Python script using Selenium that automatically attempts to enroll in York University courses at user-defined intervals.

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
2. Place `chromedriver.exe` in the same directory as `main.py`

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
   - Course Catalogue Number (6 characters code)
   - Check Interval (seconds between availability checks)
   - Session Duration (minutes before a new browser session is created)
4. Click "Start Checking" to begin monitoring for course availability
5. The script will:
   - Check Visual Schedule Builder (VSB) for course availability
   - Attempt enrollment automatically when a spot becomes available
   - Refresh the browser session periodically to prevent timeouts
   - Continue checking until a spot is found or you click "Stop"

> **Note:** The script is currently configured for SUMMER 2025. You may need to modify line 267 for different academic terms.

## Features

### main.py

- Automatically attempts enrollment at specified intervals
- Configurable number of attempts and interval between attempts
- Support for both adding courses and transferring sections

### VSBChecker.py

- Monitors course availability through Visual Schedule Builder
- Only attempts enrollment when a spot becomes available
- Automatically refreshes the browser session to prevent timeouts
- Provides status updates with timestamps

## Requirements

- Python 3.6+
- Chrome browser
- Libraries:
  - selenium
  - beautifulsoup4
  - customtkinter
