# Assignment 2: Flight Booking System 3 features in front end

## Project Overview
This is a flight booking system that offers functionalities such as user registration, login, flight search, and passenger information record.

## Environment Setup
1. **Clone the project repository**:
    ```bash
    git clone https://github.com/Etern11ty/Group-6-FS.git
    cd FlightBooking
    ```

2. **Python & Dependencies Version Requirements**
    - **Python Version**: 
      - This project is compatible with **Python 3.13** the require version is python 3.8 or later
      - You can check your Python version using:
        ```bash
        python --version
        ```
    - **Required Packages & Versions**:
      - **Flask**: 2.2.5 
      - **Pytest**: 7.4.0

3. **Create a virtual environment and install dependencies**:
    - **Create a virtual environment**:
        ```bash
        python -m venv venv
        ```
    - **Activate the virtual environment**:
        - On macOS or Linux:
            ```bash
            source venv/bin/activate
            ```
        - On Windows:
            ```bash
            venv\Scripts\activate
            ```
    - **Install dependencies**:
        ```bash
        pip install flask
        pip install pytest
        ```

## Running the Project
1. **Set environment variables and run Flask**:
    - Set environment variables:
        - On macOS or Linux:
            ```bash
            export FLASK_APP=flightbook.py
            export FLASK_ENV=development
            ```
        - On Windows (Command Prompt):
            ```bash
            set FLASK_APP=flightbook.py
            set FLASK_ENV=development
            ```
    - Run Flask:
        ```bash
        flask run
        ```
    - Open your browser and navigate to `http://127.0.0.1:5000/` to access the application.


### Post-Launch Operations

1. **Accessing the Homepage**
   - Open the browser and navigate to `http://127.0.0.1:5000/` or the URL displayed after launching the project. You should see the homepage with a welcome screen.

2. **Login/Registration**
   - **Login**:
     - Click the “Login / Sign up” link at the top-right corner and enter an existing username and password to log in.
     - Test credentials:
       - Username: `aaa`
       - Password: `aaa`
     - If the login is successful, you will be redirected to the homepage, and the username will be displayed at the top-right corner.
   - **Registration**:
     - If you want to test the registration feature, click the “Login / Sign up” link and choose the registration option.
     - Enter a new username, password, confirm the password, and enter an email address. Then, submit the registration form.
     - If the registration is successful, you will be redirected to the homepage.

3. **Flight Search**
   - In the booking form on the homepage, enter the departure city, destination city, departure date, and return date (if "Round trip" is selected).
   - Select the number of travelers and class type, then click the "Search" button.
   - The system will display a list of available flights matching the search criteria (if any).

4. **Viewing Booking History**
   - After logging in, click the “Booking History” link on the left-side menu to view all booked flight records.
   - If there are no booking records, the system will display a message indicating no data available.

5. **Logout**
   - Click the “Logout” link at the top-right corner to log out. The system will redirect you to the homepage.

### Running Test Scripts

1. **Execute all test cases**
   - After activating the virtual environment, run the following command to execute the test scripts:
     ```bash
     pytest test_app.py
     ```
   - The results will be displayed in the console, and you can take screenshots as needed to demonstrate whether the tests passed or failed.


## Running Tests
1. **Run unit tests using `unittest`**:
    ```bash
    python -m test_app.py
    ```
2. Check the terminal output for test results.

## Common Issues
- **Port 5000 already in use**:
  - If you encounter a port conflict, try running Flask on a different port:
    ```bash
    flask run --port=5001
    ```
- **Failed to install dependencies**:
  - Make sure the virtual environment is activated and retry:
    ```bash
    pip install -r requirements.txt
    ```
- **Example content of `requirements.txt`**:
    ```
    Flask
    Flask-WTF
    Flask-Login
    Flask-SQLAlchemy
    pytest
    ...
    ```
- **RuntimeError: Working outside of request context**:
  - This error typically occurs if you attempt to access session variables outside of an active request context. Make sure you're modifying session variables only within request routes.

## Folder Structure
- **`/Flight_booking/static`**: Contains static files like CSS, JavaScript, and images.
- **`/Flight_booking/templates`**: Contains HTML templates for the project.
- **`/Assignment-2`**: Contains test scripts, screenshots, and task distribution files.


## Authors
- Team Members: Zhongren Zhao, Yueyi Huang, Wanting Huang