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
pip install selenium customtkinter
```

If you prefer not to use a virtual environment:

```powershell
# Install required packages globally
pip install selenium customtkinter
```

### Chrome WebDriver Setup

1. Download the appropriate ChromeDriver from [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/#stable)
   - Make sure to match your Chrome browser version
   - Download the stable chromedriver (win64)
2. Place `chromedriver.exe` in the same directory as `main.py`

## Usage Instructions

1. Activate your virtual environment if you created one, otherwise move to step 2 (see above)
2. Run the script: `python main.py`
3. Fill in the parameters in the application:
   - To find your Chrome profile path/number, type `chrome://version` in Chrome
   - Look for "Profile Path" in the information displayed
   - Don't set attempts too frequently to avoid timing out or being banned
4. Close any running Chrome instances before starting the script
5. Click Start to begin the enrollment process

> **Note:** The script is currently configured for Fall/Winter 2024-2025. You may need to modify line 170 for different academic terms.


## Future Plans

1. Implement headless mode (running without Chrome UI)
2. Allow script to run alongside other Chrome windows
3. Change the script to check VSB instead, to automatically enroll when spaces are found

## Requirements

- Python 3.6+
- Chrome browser
- Libraries:
  - selenium
  - customtkinter
