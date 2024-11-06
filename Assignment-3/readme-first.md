# G6 Flights - Flight Booking System

Welcome to **G6 Flights**, an online flight booking system that allows users to search for flights, register an account, book flights, select seats, and manage booking history. This guide will help you set up, install dependencies, and run the application locally for testing and development.

You can get an online preview without having to deploy locally: [Flight Booking](https://bookingflight-1024005191429.us-central1.run.app/)

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Technologies Used](#technologies-used)
- [Troubleshooting](#troubleshooting)

## Features

- User Registration and Login
- User can Logout
- Flight Search 
- Booking Process
- Seat Selection for Flights
- View Booking History
- Payment Gateway Integration
- Booking Confirmation

## Prerequisites

Before you begin, ensure you have the following installed:

- [Python 3.8+](https://www.python.org/downloads/)
- [pip (Python package installer)](https://pip.pypa.io/en/stable/installation/)
- [Node.js and npm](https://nodejs.org/) (optional, for frontend dependencies)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) (recommended for managing Python environments)

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Etern11ty/Group-6-FS.git
   cd Group-6-FS
   ```

2. **Create a Virtual Environment**:

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:
   
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Python Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   The required dependencies include Flask, Supabase Python client, and dotenv for environment variables.



## Configuration

1. **Environment Variables**:

   there is already a `key.env` file in the project root to store our environment variables. 


2. **Supabase**:

   This project uses Supabase as a backend database service. There are table `user_account`, `flight_information`, `bookinghistory`, `passenger_information`, and `seats`.

## Running the Project

1. **Run the Flask Server**:

 
   ```bash
   python Flight_booking/flightbook.py
   ```

   The application will be available at [http://127.0.0.1:8080](http://127.0.0.1:8080).

## Usage Guide

1. **Access the Homepage**:
   
   - Go to [http://127.0.0.1:8080](http://127.0.0.1:8080) to access the G6 Flights homepage.

2. **Register and Login**:
   
   - Users can register a new account or log in with existing credentials. 
   - If the login is successful, you will be redirected to the homepage, and the username will be displayed at the top-right corner.

3. **Search for Flights**:

   - Fill in the "From" and "To" fields, select the travel dates, and choose between one-way or round-trip options. Click the "Search" button to see the available flights.
   - Now our database have almost 50,000 airlines, include some flights into the United States on different dates (flight numbers are virtual), such as Paris to New York, or London to New York
   - The system will display a list of available flights matching the search criteria (if any).

4. **Viewing Booking History**
   - After logging in, click the “Booking History” link on the left-side menu to view all booked flight records.
   - If there are no booking records, the system won't display anything in the list.

5. **Book a Flight**:
   - Select the desired flight from the search results, enter passenger details, and proceed to book.

6. **View Booking History**:
   - Use the "Booking History" link to view past bookings and see details like departure time, seat selection, etc.
   - In the bookiong history, you can click the “Select Seat” link on the right to view every avaliable seats.

7. **Select a Seat**:
   - After booking a flight, use the "Go to Select Seat" button in the booking history to choose a seat for the selected flight.
   - You can select seat and click "confirm seats" to confirm your seat.
   - Once a seat is selected, it cannot be changed, and you can see a confirmation that a seat has been reserved

8. **Logout**
   - Click the “Logout” link at the top-right corner to log out. The system will redirect you to the homepage.

## Project Structure

```plaintext
Flight_booking/
    |- static/             # Static files such as CSS and images
    |- templates/          # HTML templates
    |- flightbook.py       # Main application file
    |- key.env             # Environment file containing API keys (Supabase)
    |- test_app.py         # Testing script
css/                       # CSS styling folder
images/                    # Image files used in the application
index.html                 # Homepage HTML
key.env                    # Environment file (duplicate)
requirements.txt           # Python dependencies
 
```


## Technologies Used

- **Backend**: Flask (Python), Supabase
- **Frontend**: HTML, CSS, JavaScript
- **Database**: Supabase PostgreSQL
- **Environment Management**: dotenv, virtualenv

## Troubleshooting

1. **Supabase Authentication Error**:
   - Ensure that your `.env` file contains valid `SUPABASE_URL` and `SUPABASE_KEY` values.

2. **ModuleNotFoundError for Flask or Supabase**:
   - Make sure all dependencies are installed correctly by running `pip install -r requirements.txt`.

3. **Port Conflict Error**:
   - If port `8080` is already in use, specify an alternate port when running Flask:
     ```bash
     flask run --port 5001
     ```

4. **Static Files Not Loading**:
   - Check that the `static_folder` is set correctly in your Flask app initialization.

## Additional Notes

- **Mobile Compatibility**: The project has been designed to be compatible with both desktop.
- **UI Enhancements**: The UI is styled to provide a clean and user-friendly experience. Customizations can be made to the CSS files located in `static/homepage/css` to modify the appearance.

Feel free to contribute to this project by submitting issues, suggesting new features, or creating pull requests.

