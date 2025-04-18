import customtkinter as ctk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep, time
import threading
import os
import datetime


class VSBCheckerApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Course Availability Checker")
        self.window.geometry("800x500")  

        # Variables
        self.is_running = False
        self.course_code = ctk.StringVar()
        self.check_interval = ctk.StringVar(value="60")  # Default check every 60 seconds
        self.session_duration = ctk.StringVar(value="15")  # Default session duration in minutes
        self.enrollment_type = ctk.StringVar(value="add")
        
        default_chrome_path = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
        self.chrome_user_data = ctk.StringVar(value=default_chrome_path)
        self.chrome_profile = ctk.StringVar(value="Profile 1")

        # Driver object
        self.driver = None
        self.session_start_time = None

        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Title
        title = ctk.CTkLabel(main_frame, text="Course Availability Checker",
                             font=("Arial", 24, "bold"))
        title.pack(pady=20)

        # Chrome Settings Frame
        chrome_frame = ctk.CTkFrame(main_frame)
        chrome_frame.pack(fill="x", padx=20, pady=10)

        # Chrome User Data Directory
        user_data_label = ctk.CTkLabel(chrome_frame, text="Chrome User Data Directory:")
        user_data_label.pack(side="left", padx=10)

        user_data_entry = ctk.CTkEntry(chrome_frame, textvariable=self.chrome_user_data, width=300)
        user_data_entry.pack(side="left", fill="x", expand=True, padx=10)

        # Chrome Profile Frame
        profile_frame = ctk.CTkFrame(main_frame)
        profile_frame.pack(fill="x", padx=20, pady=10)

        profile_label = ctk.CTkLabel(profile_frame, text="Chrome Profile:")
        profile_label.pack(side="left", padx=10)

        profile_entry = ctk.CTkEntry(profile_frame, textvariable=self.chrome_profile)
        profile_entry.pack(side="left", fill="x", expand=True, padx=10)

        # Course Code Entry
        course_frame = ctk.CTkFrame(main_frame)
        course_frame.pack(fill="x", padx=20, pady=10)

        course_label = ctk.CTkLabel(course_frame, text="Course Catalogue Number (6 characters):")
        course_label.pack(side="left", padx=10)

        course_entry = ctk.CTkEntry(course_frame, textvariable=self.course_code)
        course_entry.pack(side="left", fill="x", expand=True, padx=10)

        # Enrollment Type Selection
        type_frame = ctk.CTkFrame(main_frame)
        type_frame.pack(fill="x", padx=20, pady=10)

        type_label = ctk.CTkLabel(type_frame, text="Enrollment Type:")
        type_label.pack(side="left", padx=10)

        add_radio = ctk.CTkRadioButton(type_frame, text="Add Course",
                                       variable=self.enrollment_type, value="add")
        add_radio.pack(side="left", padx=10)

        swap_radio = ctk.CTkRadioButton(type_frame, text="Transfer Section",
                                        variable=self.enrollment_type, value="transfer")
        swap_radio.pack(side="left", padx=10)

        # Check Interval config
        interval_frame = ctk.CTkFrame(main_frame)
        interval_frame.pack(fill="x", padx=20, pady=10)

        interval_label = ctk.CTkLabel(interval_frame, text="Check Interval (seconds):")
        interval_label.pack(side="left", padx=10)

        interval_entry = ctk.CTkEntry(interval_frame, textvariable=self.check_interval)
        interval_entry.pack(side="left", padx=10)

        session_label = ctk.CTkLabel(interval_frame, text="Session Duration (minutes):")
        session_label.pack(side="left", padx=10)

        session_entry = ctk.CTkEntry(interval_frame, textvariable=self.session_duration)
        session_entry.pack(side="left", padx=10)

        # Status Display
        self.status_label = ctk.CTkLabel(main_frame, text="Ready to start",
                                         font=("Arial", 12))
        self.status_label.pack(pady=20)

        # Control Buttons
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", padx=20, pady=10)

        self.start_button = ctk.CTkButton(button_frame, text="Start Checking",
                                          command=self.start_checking)
        self.start_button.pack(side="left", padx=10, expand=True)

        self.stop_button = ctk.CTkButton(button_frame, text="Stop",
                                         command=self.stop_checking,
                                         state="disabled")
        self.stop_button.pack(side="left", padx=10, expand=True)

    def update_status(self, message):
        self.status_label.configure(text=message)
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {message}")

    def start_checking(self):
        if not self.course_code.get():
            self.update_status("Please enter a course code")
            return

        self.is_running = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")

        # Start checking process in a separate thread
        thread = threading.Thread(target=self.checking_process)
        thread.daemon = True
        thread.start()

    def stop_checking(self):
        self.is_running = False
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
        
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.update_status("Checking stopped")

    def initialize_driver(self):
        """Initialize or reinitialize the Chrome driver"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        
        service = Service(executable_path="chromedriver.exe")
        options = webdriver.ChromeOptions()

        # Use the user-provided Chrome settings
        options.add_argument(f"--user-data-dir={self.chrome_user_data.get()}")
        options.add_argument(f"profile-directory={self.chrome_profile.get()}")
        
        self.driver = webdriver.Chrome(service=service, options=options)
        self.session_start_time = time()
        self.update_status("Browser session initialized")
        return self.driver

    def check_session_expired(self):
        """Check if the current session has exceeded the time limit"""
        if not self.session_start_time:
            return True
            
        session_duration_mins = int(self.session_duration.get())
        elapsed_mins = (time() - self.session_start_time) / 60
        
        if elapsed_mins >= session_duration_mins:
            self.update_status(f"Session timeout after {elapsed_mins:.1f} minutes. Reinitializing...")
            return True
        return False

    def is_course_available(self):
        """Check if the course has available spots using BeautifulSoup"""
        try:
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Get the exact catalog number the user is looking for (e.g., G11E08)
            catalog_number = self.course_code.get()
            
            # Find all catalog numbers on the page
            catalog_elements = soup.find_all(string=lambda text: text and catalog_number in text)
            
            if not catalog_elements:
                self.update_status(f"Couldn't find catalog number {catalog_number} on the page")
                return False
                
            # For each instance of the catalog number
            for catalog_element in catalog_elements:
                # Find the parent container that has both the catalog number and the availability
                # Move up the DOM to find a common parent
                parent = catalog_element.parent
                for _ in range(4):  # Go up a few levels to find a common container
                    if parent is None:
                        break
                    parent = parent.parent
                
                if parent:
                    # Check if this section contains "Full" text
                    full_text = parent.find(string=lambda text: text and "Full" in text)
                    if not full_text:
                        self.update_status(f"Found available section with catalog {catalog_number}!")
                        return True
            
            # If we've checked all sections with our catalog number and all are full
            self.update_status(f"All sections with catalog {catalog_number} are full")
            return False
            
        except Exception as e:
            self.update_status(f"Error checking availability: {str(e)}")
            return False

    def navigate_to_vsb(self):
        """Navigate to Visual Schedule Builder and search for the course"""
        try:
            # Navigate to VSB
            self.driver.get("https://schedulebuilder.yorku.ca/vsb/")
            sleep(5)
            
            # Check if we need to login (look for login button)
            login_buttons = self.driver.find_element(By.NAME, "dologin")
            
            if login_buttons != None:
                self.update_status("Login page detected, attempting to login...")
                # Click the login button
                login_buttons.click()
                sleep(2)
                
                # Wait for authentication to complete (20 seconds)
                self.update_status("Waiting for authentication...")
                sleep(20)
            
            # Wait for the VSB interface to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "code_number"))
            )
            
            # Enter course code and search
            self.driver.find_element(By.ID, "term_2024115117").click()
            sleep(3)
            search_input = self.driver.find_element(By.ID, "code_number")
            search_input.clear()
            search_input.send_keys(self.course_code.get())
            
            search_button = self.driver.find_element(By.ID, "addCourseButton")
            search_button.click()
            
            sleep(5)
            
            self.update_status("Successfully navigated to VSB and searched for course")
            return True
        except Exception as e:
            self.update_status(f"Error navigating to VSB: {str(e)}")
            return False

    def refresh_vsb(self):
        """Refresh the VSB page to check for updated availability"""
        try:
            self.driver.refresh()
            sleep(6)
            self.update_status("VSB page refreshed")
            return True
        except Exception as e:
            self.update_status(f"Error refreshing VSB: {str(e)}")
            return False

    def attempt_enrollment(self):
        """Try to enroll in the course"""
        try:
            self.update_status("Space available! Attempting enrollment...")
            
            # Navigate to the enrollment page
            self.driver.get("https://wrem.sis.yorku.ca/Apps/WebObjects/REM.woa/wa/DirectAction/rem")
            sleep(7)
            
            # Login if necessary
            login_button = self.driver.find_elements(By.NAME, "dologin")
            if login_button:
                login_button.click()
                sleep(20)
            
            # Select term
            self.driver.find_element(By.NAME, '5.5.1.27.1.11.0').click()
            sleep(5)
            self.driver.find_element(By.XPATH,
                                    "//select[@name='5.5.1.27.1.11.0']/option[text()='SUMMER 2025']").click()
            sleep(10)
            self.driver.find_element(By.NAME, "5.5.1.27.1.13").click()
            sleep(10)

            # Select action based on enrollment type
            if self.enrollment_type.get() == "add":
                self.driver.find_element(By.NAME, "5.1.27.1.23").click()
            else:
                self.driver.find_element(By.NAME, "5.1.27.1.27").click()
            sleep(10)
            
            # Enter course code
            self.driver.find_element(By.NAME, '5.1.27.7.7').send_keys(self.course_code.get())
            sleep(10)
            self.driver.find_element(By.NAME, '5.1.27.7.9').click()
            sleep(10)
            self.driver.find_element(By.NAME, '5.1.27.11.11').click()
            sleep(10)

            # Check if enrollment was successful
            error_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'The course has not been added.')]")
            if not error_elements:
                self.update_status("Successfully enrolled! Stopping checker.")
                self.stop_checking()
                return True
            else:
                self.update_status("Enrollment attempt failed even though space was available.")
                return False
                
        except Exception as e:
            self.update_status(f"Error during enrollment: {str(e)}")
            return False

    def checking_process(self):
        """Main process to check for course availability and enroll if possible"""
        check_interval = int(self.check_interval.get())
        
        while self.is_running:
            # Initialize or reinitialize the driver if needed
            if self.check_session_expired() or not self.driver:
                if self.driver:
                    try:
                        self.driver.quit()
                    except:
                        pass
                self.initialize_driver()
                
                # Navigate to VSB and search for the course
                if not self.navigate_to_vsb():
                    sleep(30)
                    continue
            else:
                # Just refresh the page if the session is still valid
                self.refresh_vsb()
            
            # Check if the course is available
            if self.is_course_available():
                self.update_status("Course has available space!")
                
                # Attempt to enroll in the course
                enrollment_success = self.attempt_enrollment()
                
                # If enrollment failed, wait before checking VSB again
                if not enrollment_success and self.is_running:
                    self.update_status(f"Waiting {check_interval} seconds before checking availability again...")
                    sleep(check_interval)
            else:
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                elapsed_mins = (time() - self.session_start_time) / 60
                remaining_mins = int(self.session_duration.get()) - int(elapsed_mins)
                
                self.update_status(f"Course is FULL at {current_time}. Session expires in ~{remaining_mins} minutes. Checking again in {check_interval} seconds...")
                sleep(check_interval)

        # Clean up at the end
        if self.driver:
            self.driver.quit()
            self.driver = None

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = VSBCheckerApp()
    app.run()
