from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Thread, Event
from selenium.webdriver.common.keys import Keys
from flightbook import app
import time
import os
import requests  # Added to check if the Flask app is up
from werkzeug.serving import make_server  # Added to run the Flask app without blocking
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


flask_ready = Event()

def generate_unique_username(base_name="testuser"):
    timestamp = int(time.time())
    return f"{base_name}_{timestamp}"

def start_flask_app():
    print("Starting Flask app...")
    server = make_server("127.0.0.1", 5000, app)
    flask_ready.set()  # Set the event after the server is ready
    server.serve_forever()

driver = webdriver.Edge()

def test_open_homepage():
    try:
        driver.get("http://127.0.0.1:5000")
        assert "Flight" in driver.title
        print("Homepage test passed.")
    except Exception as e:
        print(f"Homepage test failed: {e}")

def test_register_login_logout_registerfaild():
    try:
        driver.get("http://127.0.0.1:5000/register")
        
        unique_username = generate_unique_username()
        
        driver.find_element(By.NAME, "username").send_keys(unique_username)
        driver.find_element(By.NAME, "email").send_keys(f"{unique_username}@example.com")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.NAME, "confirm_password").send_keys("password123")
        
        driver.find_element(By.XPATH, "//button[text()='Register']").click()

        time.sleep(1)
        # Check registration success
        assert "Welcome" in driver.page_source
        print("Registration successful.")
        # Logout after registration (if automatically logged in)
        driver.get("http://127.0.0.1:5000/logout")
        time.sleep(1)

        # Register failed 

        driver.get("http://127.0.0.1:5000/register")
        
        driver.find_element(By.NAME, "username").send_keys("testuser2")
        driver.find_element(By.NAME, "email").send_keys("testuser2@example.com")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.NAME, "confirm_password").send_keys("password456")
        
        driver.find_element(By.XPATH, "//button[text()='Register']").click()
        
        time.sleep(2)
        
        assert "Passwords do not match" in driver.page_source
        print("Password mismatch test passed.")

        # Login
        driver.get("http://127.0.0.1:5000/login_page")
        driver.find_element(By.NAME, "username").send_keys(unique_username)
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.XPATH, "//button[text()='Login']").click()       
        time.sleep(1)
        
        # Check login success
        assert "Welcome" in driver.page_source
        print("Login successful.")


        # Logout
        driver.get("http://127.0.0.1:5000/logout")
        time.sleep(2)
        assert "Login" in driver.page_source
        print("Logout successful.")
        
        print("\nRegistration, registration password mismatch, login, and logout test passed.\n")

    except Exception as e:
        print(f"\nRegistration, registration password mismatch, login, and logout test failed: {e}\n")

def test_booking_process():
    try:
        driver.get("http://127.0.0.1:5000/register")
        
        unique_username = generate_unique_username()
        
        driver.find_element(By.NAME, "username").send_keys(unique_username)
        driver.find_element(By.NAME, "email").send_keys(f"{unique_username}@example.com")
        driver.find_element(By.NAME, "password").send_keys("password123")
        driver.find_element(By.NAME, "confirm_password").send_keys("password123")
        driver.find_element(By.XPATH, "//button[text()='Register']").click()

        driver.get("http://127.0.0.1:5000")
        

        # Fill in the search form
        driver.find_element(By.NAME, "from_city").send_keys("Paris")
        driver.find_element(By.NAME, "to_city").send_keys("New York")
        driver.find_element(By.NAME, "travellers_class").send_keys("1 Traveller")
        driver.find_element(By.NAME, "departure_date").send_keys("002025--31")
        
        driver.find_element(By.CLASS_NAME, "search-button").click()
        
        time.sleep(2)
        

     # Select a flight
        wait = WebDriverWait(driver, 10)
        select_buttons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "select-button")))
        if not select_buttons:
            raise Exception("No flights available to book.")
        select_buttons[0].click()
        time.sleep(2)
        print("Flight selected.")

        driver.find_element(By.XPATH, "//button[text()='Continue']").click()   
        time.sleep(2)

        driver.find_element(By.NAME, "first_name_1").send_keys("John")
        driver.find_element(By.NAME, "last_name_1").send_keys("Doe")
        driver.find_element(By.NAME, "dob_1").send_keys("001990--11--1")
        driver.find_element(By.NAME, "id_number_1").send_keys("A1234567")
        driver.find_element(By.NAME, "email_1").send_keys("johndoe@example.com")
        driver.find_element(By.NAME, "phone_1").send_keys("1234567890")

        # Address details
        driver.find_element(By.NAME, "address1_1").send_keys("123 Main St")
        driver.find_element(By.NAME, "address2_1").send_keys("Apt 4B")
        driver.find_element(By.NAME, "country_1").send_keys("USA")
        driver.find_element(By.NAME, "city_1").send_keys("New York")
        driver.find_element(By.NAME, "postal_code_1").send_keys("10001")

        # Emergency contact details
        driver.find_element(By.NAME, "em_first_name").send_keys("Jane")
        driver.find_element(By.NAME, "em_last_name").send_keys("Doe")
        driver.find_element(By.NAME, "em_phone").send_keys("0987654321")
        driver.find_element(By.NAME, "em_email").send_keys("janedoe@example.com")

        # Bag information
        driver.find_element(By.NAME, "bags").clear()  # Clear default value
        driver.find_element(By.NAME, "bags").send_keys("2")  # Set number of bags

        # Click the save and continue button
        driver.find_element(By.CSS_SELECTOR, "button.save-btn").click()

        driver.find_element(By.NAME, "payment_type").click()  # Select credit card by default
        driver.find_element(By.NAME, "card_number").send_keys("1234 5678 9123 4567")
        driver.find_element(By.NAME, "cardholder_name").send_keys("John K")
        driver.find_element(By.NAME, "expiry_date").send_keys("12/25")  # MM/YY format
        driver.find_element(By.NAME, "cvv").send_keys("123")

        driver.find_element(By.CSS_SELECTOR, "button.pay-button").click()
        print("Payment form submitted.")

        # Wait for the loading process to complete
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "loading-container"), "Processing your payment...")
        )
        print("Loading process started.")

        # Wait for redirection to the success page
        WebDriverWait(driver, 15).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Flight booked successfully")
        )
        print("Payment completed successfully.")

        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".button.history-button"))
        ).click()
        print("Clicked 'View Booking History' button.")

        time.sleep(4)

        # Verify navigation to the booking history page
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Booking History")
        )
        print("Successfully navigated to the Booking History page.")
        
        driver.get("http://127.0.0.1:5000/logout")
        time.sleep(2)
        assert "Login" in driver.page_source
        print("Logout successful.")

    except Exception as e:
        print(f"Flight booking test failed: {e}")




def test_booking_history_authenticated():
    try:
        # Step 1: Log in
        driver.get("http://127.0.0.1:5000/login_page")
        driver.find_element(By.NAME, "username").send_keys("aaa")
        driver.find_element(By.NAME, "password").send_keys("aaa")
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        time.sleep(2)
        
        # Step 2: Navigate to booking history page
        driver.get("http://127.0.0.1:5000/booking-history")
        time.sleep(2)
        assert "Booking History" in driver.page_source, "Booking History page not loaded."
        print("Booking history page loaded successfully.")
        
        # Step 3: Dynamically extract booking_id
        booking_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/select_seat/')]")
        if booking_links:
            booking_id = booking_links[0].get_attribute("href").split("/")[-1]
        else:
            raise Exception("No bookings found to select a seat.")
        
        # Step 4: Navigate to seat selection page
        driver.get(f"http://127.0.0.1:5000/select_seat/{booking_id}")
        time.sleep(2)
        assert "Select Seat" in driver.page_source, "Seat selection page not loaded."
        print("Seat selection page loaded successfully.")
        
        # Step 5: Select a seat dynamically
        available_seats = driver.find_elements(By.XPATH, "//button[contains(@class, 'seat-button') and not(contains(@class, 'occupied'))]")
        if available_seats:
            available_seats[0].click()
        else:
            raise Exception("No available seats found.")
        time.sleep(2)
        
        # Step 6: Confirm the seat selection
        confirm_button = driver.find_element(By.XPATH, "//button[text()='Confirm']")
        confirm_button.click()
        time.sleep(2)
        
        # Verify seat selection success
        assert "Seat selected successfully" in driver.page_source, "Seat selection failed."
        print("Seat selection test passed.")
    
    except Exception as e:
        print(f"Booking history and seat selection test failed: {e}")


# Start the Flask app in a separate thread
flask_thread = Thread(target=start_flask_app)
flask_thread.daemon = True
flask_thread.start()

# Wait for the Flask app to start
flask_ready.wait(timeout=10)

try:
    # Run tests
    test_open_homepage()
    test_register_login_logout_registerfaild()
    test_booking_process()


finally:
    driver.quit()
    os._exit(0)
