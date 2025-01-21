import customtkinter as ctk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import threading
import os


class CourseEnrollmentApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Course Enrollment Assistant")
        self.window.geometry("800x500")  

        # Variables
        self.is_running = False
        self.course_code = ctk.StringVar()
        self.num_attempts = ctk.StringVar(value="5")
        self.time_between = ctk.StringVar(value="1800")
        self.enrollment_type = ctk.StringVar(value="add")
        
        default_chrome_path = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
        self.chrome_user_data = ctk.StringVar(value=default_chrome_path)
        self.chrome_profile = ctk.StringVar(value="Profile 1")

        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Title
        title = ctk.CTkLabel(main_frame, text="Course Enrollment Assistant",
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

        # Attempts config
        attempts_frame = ctk.CTkFrame(main_frame)
        attempts_frame.pack(fill="x", padx=20, pady=10)

        attempts_label = ctk.CTkLabel(attempts_frame, text="Number of Attempts:")
        attempts_label.pack(side="left", padx=10)

        attempts_entry = ctk.CTkEntry(attempts_frame, textvariable=self.num_attempts)
        attempts_entry.pack(side="left", padx=10)

        time_label = ctk.CTkLabel(attempts_frame, text="Time Between (seconds):")
        time_label.pack(side="left", padx=10)

        time_entry = ctk.CTkEntry(attempts_frame, textvariable=self.time_between)
        time_entry.pack(side="left", padx=10)

        # Status Display
        self.status_label = ctk.CTkLabel(main_frame, text="Ready to start",
                                         font=("Arial", 12))
        self.status_label.pack(pady=20)

        # Control Buttons
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", padx=20, pady=10)

        self.start_button = ctk.CTkButton(button_frame, text="Start Enrollment",
                                          command=self.start_enrollment)
        self.start_button.pack(side="left", padx=10, expand=True)

        self.stop_button = ctk.CTkButton(button_frame, text="Stop",
                                         command=self.stop_enrollment,
                                         state="disabled")
        self.stop_button.pack(side="left", padx=10, expand=True)

    def update_status(self, message):
        self.status_label.configure(text=message)

    def start_enrollment(self):
        if not self.course_code.get():
            self.update_status("Please enter a course code")
            return

        self.is_running = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")

        # Start enrollment process in a separate thread
        thread = threading.Thread(target=self.enrollment_process)
        thread.daemon = True
        thread.start()

    def stop_enrollment(self):
        self.is_running = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.update_status("Enrollment stopped")

    def enrollment_process(self):
        service = Service(executable_path="chromedriver.exe")
        myoptions = webdriver.ChromeOptions()

        # Use the user-provided Chrome settings
        myoptions.add_argument(f"--user-data-dir={self.chrome_user_data.get()}")
        myoptions.add_argument(f"profile-directory={self.chrome_profile.get()}")

        attempts = int(self.num_attempts.get())
        time_between = int(self.time_between.get())

        for x in range(attempts):
            if not self.is_running:
                break

            self.update_status(f"Attempt {x + 1} of {attempts}")

            driver = webdriver.Chrome(service=service, options=myoptions)
            try:
                sleep(4)
                driver.get("https://wrem.sis.yorku.ca/Apps/WebObjects/REM.woa/wa/DirectAction/rem")
                sleep(7)
                driver.find_element(By.NAME, "dologin").click()
                sleep(20)
                driver.find_element(By.NAME, '5.5.1.27.1.11.0').click()
                sleep(5)
                driver.find_element(By.XPATH,
                                    "//select[@name='5.5.1.27.1.11.0']/option[text()='FALL/WINTER 2024-2025 UNDERGRADUATE STUDENTS']").click()
                sleep(10)
                driver.find_element(By.NAME, "5.5.1.27.1.13").click()
                sleep(10)

                # Select action based on enrollment type
                if self.enrollment_type.get() == "add":
                    driver.find_element(By.NAME, "5.1.27.1.23").click()
                else:
                    driver.find_element(By.NAME, "5.1.27.1.27").click()

                sleep(10)
                driver.find_element(By.NAME, '5.1.27.7.7').send_keys(self.course_code.get())
                sleep(10)
                driver.find_element(By.NAME, '5.1.27.7.9').click()
                sleep(10)
                driver.find_element(By.NAME, '5.1.27.11.11').click()
                sleep(10)

                isFound = driver.find_elements(By.XPATH, "//*[contains(text(), 'The course has not been added.')]")
                sleep(4)

                if not isFound:
                    self.update_status("Successfully enrolled!")
                    break
                else:
                    self.update_status(f"Enrollment failed. Waiting {time_between} seconds before next attempt...")

            except Exception as e:
                self.update_status(f"Error occurred: {str(e)}")
            finally:
                driver.close()

            if x < attempts - 1 and self.is_running:
                sleep(time_between)

        if self.is_running:
            self.stop_enrollment()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = CourseEnrollmentApp()
    app.run()