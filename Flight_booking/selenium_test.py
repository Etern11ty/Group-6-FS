from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Thread, Event
from selenium.webdriver.common.keys import Keys
from flightbook import app
import time
import os
import requests  # Added to check if the Flask app is up
from werkzeug.serving import make_server  # Added to run the Flask app without blocking

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

def test_search_flights():
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
        
        # Check the results page
        assert "Paris" in driver.page_source
        assert "New York" in driver.page_source
        print("Search flights test passed.")
    except Exception as e:
        print(f"Search flights test failed: {e}")





def test_booking_history_authenticated():
    try:
        driver.get("http://127.0.0.1:5000/login_page")
        
        # Log in
        driver.find_element(By.NAME, "username").send_keys("aaa")
        driver.find_element(By.NAME, "password").send_keys("aaa")
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        
        time.sleep(2)
        
        # Navigate to booking history page
        driver.get("http://127.0.0.1:5000/booking-history")
        
        time.sleep(2)
        
        # Check booking history
        assert "Booking History" in driver.page_source
        print("Authenticated booking history test passed.")
    except Exception as e:
        print(f"Authenticated booking history test failed: {e}")

def test_booking_history_unauthenticated():
    try:
        driver.get("http://127.0.0.1:5000/logout")  # Ensure logged-out state
        driver.get("http://127.0.0.1:5000/booking-history")
        
        time.sleep(2)
        
        # Check for access denial
        assert "User not authenticated" in driver.page_source
        print("Unauthenticated booking history test passed.")
    except Exception as e:
        print(f"Unauthenticated booking history test failed: {e}")

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


    test_search_flights()


finally:
    driver.quit()
    os._exit(0)
