from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(dotenv_path="key.env")

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")



app = Flask(__name__, static_folder='static')

supabase: Client = create_client(supabase_url, supabase_key)

# # test database can work or not
# response = supabase.table("user_account").select("*").execute()
# print(response.data) 


app.secret_key = 'aa2233'

username_list = ["aaa", "123"]
password_list = ["aaa", "123"]
email_list = ["aaa@gmail.com", "123@gmail.com"]


flight_list = [
    {"flight_number": "FL001", "departure": "Shanghai", "destination": "Toronto", "date": "2024-11-10"},
    {"flight_number": "FL002", "departure": "Beijing", "destination": "New York", "date": "2024-11-12"},
    {"flight_number": "FL003", "departure": "Tokyo", "destination": "Los Angeles", "date": "2024-11-15"},
    {"flight_number": "FL004", "departure": "Seoul", "destination": "San Francisco", "date": "2024-11-18"},
    {"flight_number": "FL005", "departure": "Paris", "destination": "London", "date": "2024-11-20"},
    {"flight_number": "FL006", "departure": "Sydney", "destination": "Melbourne", "date": "2024-11-22"},
    {"flight_number": "FL007", "departure": "Berlin", "destination": "Amsterdam", "date": "2024-11-25"},
    {"flight_number": "FL008", "departure": "Rome", "destination": "Madrid", "date": "2024-11-27"},
    {"flight_number": "FL009", "departure": "Dubai", "destination": "Doha", "date": "2024-12-01"},
    {"flight_number": "FL010", "departure": "Delhi", "destination": "Mumbai", "date": "2024-12-03"},
]




@app.route('/')
def index():
    # session['current_username'] = 'aaa'
    
    current_username = session.get('current_username', "Login / Sign up")
    return render_template('homepage.html', current_username=current_username)

    

@app.route('/flights')
def flights():
    return render_template('homepage.html')


@app.route('/booking-history')
def booking_history():
    return 'booking_history.html'


@app.route('/login_page')
def login_page():
    error = session.pop('error', None)
    return render_template('login.html', error=error)

@app.route('/cart')
def cart():
    return 'cart.html'


@app.route('/logout')
def logout():
    session.pop('current_username', None)
    return redirect(url_for('index'))



@app.route('/search-results', methods=['POST'])
def search_results():
    trip_type = request.form.get('trip')
    from_city = request.form['from_city']
    to_city = request.form['to_city']
    travellers = request.form['travellers_class']
    departure_date = request.form['departure_date']
    return_date = request.form.get('return_date', None)

    print(f"Trip Type: {trip_type}")
    print(f"From: {from_city}")
    print(f"To: {to_city}")
    print(f"Travellers: {travellers}")
    print(f"Departure Date: {departure_date}")
    print(f"Return Date: {return_date}")




    matching_flights = []
    for flight in flight_list:
        if (flight["departure"] == from_city and 
            flight["destination"] == to_city and 
            flight["date"] == departure_date):
            matching_flights.append(flight)

    if matching_flights:
        flight_info = ", ".join([f'Flight {flight["flight_number"]}' for flight in matching_flights])
        if trip_type == "oneway":
            info = f"{travellers} from {from_city} to {to_city} on {departure_date}. Matching flights: {flight_info}."
        else:
            info = f"{travellers} from {from_city} to {to_city} on {departure_date}, returning on {return_date}. Matching flights: {flight_info}."
    else:
        if trip_type == "oneway":
            info = f"No flights found for {travellers} from {from_city} to {to_city} on {departure_date}."
        else:
            info = f"No flights found for {travellers} from {from_city} to {to_city} on {departure_date} and returning on {return_date}."

    return info


@app.route('/login', methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']
    
    if username in username_list and password in password_list:
        user_index = username_list.index(username)
        if password_list[user_index] == password:

            session['current_username'] = username

            return redirect(url_for('index'))
        
    session['error'] = "Invalid username or password"  
    return redirect(url_for('login_page')) 


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']

        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match")
        elif username in username_list:
            return render_template('register.html', error="Username is occupied")
        elif email in email_list:
            return render_template('register.html', error="Email is occupied")


        username_list.append(username)
        password_list.append(password)
        email_list.append(email)

        print(username_list, password_list, email_list)

        session.pop('error', None)

        current_username = username

        session['current_username'] = current_username
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/login_1')
def login_1():
    return render_template('login.html')


# Mock backend storage, a list to store passager data
passengers_data_store = []

@app.route('/')
def home():
    return redirect(url_for('passenger_info'))
    


@app.route('/passenger_info', methods=['GET', 'POST'])
def passenger_info():


    current_username = session.get('current_username')
    if not current_username:
        return "User not authenticated", 401 
    
    if request.method == 'POST':
        # Check if all required fields are provided
        required_fields = ['first_name_1', 'last_name_1', 'email_1', 'phone_1', 'dob_1', 'address1_1', 'country_1', 'city_1', 'postal_code_1']
        for field in required_fields:
            if not request.form.get(field):
                return "Missing required field", 400  # return erro info
            
        try:
            birthday = datetime.strptime(request.form['dob_1'], "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            return "Invalid date format for birthday", 400
        
        # Store passenger data in a dictionary
        birthday = datetime.strptime(request.form['dob_1'], "%Y-%m-%d").strftime("%Y-%m-%d")
        passenger_data = {
            'username' : current_username,
            'firstname': request.form['first_name_1'],
            'lastname': request.form['last_name_1'],
            'idnumber': request.form.get('id_number_1', ''),
            'emailaddress': request.form['email_1'],
            'phone': request.form['phone_1'],
            'birthday': birthday,
            'addressline1': request.form['address1_1'],
            'addressline2': request.form.get('address2_1', ''),
            'country': request.form['country_1'],
            'city': request.form['city_1'],
            'postalcode': request.form['postal_code_1'],
            'emergfirstname': request.form['em_first_name'],
            'emerglastname': request.form['em_last_name'],
            'emergphone': request.form['em_phone'],
            'emergemailaddress': request.form['em_email'],
        }
        
                # insert passenger info into supabase
        try:
            response = supabase.table("passenger_information").upsert(passenger_data, on_conflict=["username"]).execute()
            if response.error:
                return f"Error adding passenger data: {response.error}", 500
            else:
                # Fetch the updated data from the database to display it
                updated_response = supabase.table("passenger_information").select("*").eq("username", current_username).execute()
                if updated_response.data:
                    # Pass the updated data to the template
                    updated_data = updated_response.data[0]
                    return render_template('booking.html', existing_data=updated_data)
                else:
                    return "Error retrieving updated data", 500
        except Exception as e:
            return f"Data submitted successfully!", 500

    # if GET request，return passenger info page
    try:
        response = supabase.table("passenger_information").select("*").eq("username", current_username).execute()
        if response.data:
            # If data exists, pass it to the template
            existing_data = response.data[0]  # Get the first matching row
            return render_template('booking.html', existing_data=existing_data)
        else:
            # If no existing data, render an empty form
            return render_template('booking.html', existing_data=None)
    except Exception as e:
        return f"An error occurred while fetching data: {str(e)}", 500



@app.route('/view_passenger_data')
def view_passenger_data():
    try:
        response = supabase.table("passenger_infomation").select("*").execute()
        if response.get('error'):
            return f"Error fetching passenger data: {response['error']}", 500
        else:
            return {"passenger_data": response['data']}
    except Exception as e:
        return f"An error occurred while trying to fetch data from Supabase: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
    
