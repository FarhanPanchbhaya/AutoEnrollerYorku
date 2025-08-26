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

### Chrome for Testing Setup

**Important:** This script now requires Chrome for Testing instead of regular Chrome due to profile access restrictions.

1. **Download Chrome for Testing:**
   - Open terminal in the same directory you have `VSBChecker.py` in
   - `npx @puppeteer/browsers install chrome@139` into terminal 

2. **Download ChromeDriver:**
   - `npx @puppeteer/browsers install chromedriver@139` into terminal

   - Alternatively, you may download step 1 and 2 from [Chrome For Testing](https://googlechromelabs.github.io/chrome-for-testing/), but make sure you place them into the same directory.

3. **Set up Chrome for Testing Profile:**
   - Launch Chrome for Testing from the `chrome` folder that should be in the same directory as VSBChecker.py: `chrome/win64-xxx/chrome-win64/chrome.exe`
   - Log into your York University account and do the 2FA process (or just skip this and do it when you run the script the first time)

## Usage Instructions

### Course Availability Checker (VSBChecker.py)

1. Activate your virtual environment if you created one (see above)
2. Run the script: `python VSBChecker.py`
3. Fill in the parameters in the application:
   - **Chrome for Testing User Data Directory:** Usually pre-filled with the correct path (`%LOCALAPPDATA%\Google\Chrome for Testing\User Data`)
   - **Chrome for Testing Profile:** Usually "Default" (pre-filled)
   - **Course Catalogue Number:** Enter the 6-character course code
   - **Enrollment Type:** Choose "Add Course" or "Transfer Section"
   - **Check Interval:** Seconds between availability checks (default: 60)
   - **Session Duration:** Minutes before creating a new browser session (default: 15)
4. **Important:** Close any running Chrome or Chrome for Testing instances before starting the script
5. Click "Start Checking" to begin monitoring for course availability
6. The script will:
   - Check Visual Schedule Builder (VSB) for course availability
   - Refresh the browser session periodically to prevent timeouts
   - Continue checking until a spot is found or you click "Stop"
   - Attempt enrollment automatically when a spot becomes available

> **Note:** The script is currently configured for the current academic term. You may need to modify specific lines for different terms:
>
> - Line 291: Update the term ID for VSB (e.g., "term_2025102119")
> - Lines 345-347: Update the enrollment term selection [value 0 is Fall/Winter undergrad, value 1 is Grad or Osgoode students, value 2 is Summer]
> - If you need to find these lines, use Ctrl+F and search for "You may have to change" in the code file.

## Requirements

- Python 3.6+
- Chrome for Testing browser (included in project setup)
- Libraries:
  - selenium
  - beautifulsoup4
  - customtkinter

## Troubleshooting

### Common Issues:

1. **"Driver not initialized" error:** Make sure Chrome for Testing is properly set up and the profile paths are correct
2. **Login issues:** Ensure you've logged into your York accounts in Chrome for Testing and saved your credentials
3. **Course not found:** Verify the course catalogue number is correct (6 characters)
4. **Term selection issues:** Update the term IDs in the code if enrolling for a different semester

### Why Chrome for Testing?

Regular Chrome no longer allows scripts to access specific user profiles due to security restrictions. Chrome for Testing is designed specifically for automation and testing purposes, making it the required browser for this script.
