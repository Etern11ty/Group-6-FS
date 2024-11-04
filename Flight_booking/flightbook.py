from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv(dotenv_path="key.env")

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")


app = Flask(__name__, static_folder='static')

supabase: Client = create_client(supabase_url, supabase_key)

# test database can work or not
response = supabase.table("user_account").select("*").execute()

# test database can work or not
response2 = supabase.table("flight_information").select("*").execute()


app.secret_key = 'aa2233'

# username_list = ["aaa", "123"]
# password_list = ["aaa", "123"]
# email_list = ["aaa@gmail.com", "123@gmail.com"]


flight_list = supabase.table("flight_information").select("*").execute().data




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
    return render_template('booking_history.html')


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
    departure_date = request.form['departure_date'] or datetime.now().strftime('%Y-%m-%d')
    return_date = request.form.get('return_date') or (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

    # Fetch outbound flights with departure and destination details
    response = supabase.table("flight_information").select("flight_number, departure, destination, departure_time, arrival_time,aircraft, dest, origin") \
        .eq("departure", from_city) \
        .eq("destination", to_city) \
        .eq("date", departure_date) \
        .execute()
    matching_flights = response.data if response.data else []

    # Fetch prices and update flight data
    for flight in matching_flights:
        flight_number = flight["flight_number"]
        price_response = supabase.table("price").select("price").eq("flight_number", flight_number).execute()
        price_data = price_response.data
        flight["price"] = price_data[0]["price"] if price_data else "N/A"

    # If round trip, fetch return flights similarly
    return_flights = []
    if trip_type != "oneway":
        response_return = supabase.table("flight_information").select("flight_number, departure, destination, departure_time, arrival_time,aircraft, dest, origin") \
            .eq("departure", to_city) \
            .eq("destination", from_city) \
            .eq("date", return_date) \
            .execute()
        return_flights = response_return.data if response_return.data else []

        # Fetch prices for return flights
        for flight in return_flights:
            flight_number = flight["flight_number"]
            price_response = supabase.table("price").select("price").eq("flight_number", flight_number).execute()
            price_data = price_response.data
            flight["price"] = price_data[0]["price"] if price_data else "N/A"

    return render_template(
        'search_results.html', 
        matching_flights=matching_flights,
        return_flights=return_flights,
        travellers=travellers,
        from_city=from_city,
        to_city=to_city,
        departure_date=departure_date,
        return_date=return_date,
        trip_type=trip_type
    )

@app.route('/flight_detail', methods=['POST'])
def flight_detail():
    flight_number = request.form['flight_number']
    

    response = supabase.table("flight_information").select("*").eq("flight_number", flight_number).execute()
    flight_info = response.data[0] if response.data else None


    price_response = supabase.table("price").select("price").eq("flight_number", flight_number).execute()
    flight_price = price_response.data[0]['price'] if price_response.data else "N/A"

    return render_template('flight_detail.html', flight=flight_info, price=flight_price)

@app.route('/login', methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']

    response = supabase.table("user_account").select("*").eq("Username", username).execute()
    
    if response.data:
        user = response.data[0]
        if user["Password"] == password:
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
        
        username_check = supabase.table("user_account").select("*").eq("Username", username).execute()
        if username_check.data:
            return render_template('register.html', error="Username is occupied")
        
        email_check = supabase.table("user_account").select("*").eq("emailaddress", email).execute()
        if email_check.data:
            return render_template('register.html', error="Email is occupied")

        user_data = {
            "Username": username,
            "Password": password,
            "emailaddress": email,
            "created_time": "now()" 
        }

        supabase.table("user_account").insert(user_data).execute()

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
    if request.method == 'POST':
        # Check if all required fields are provided
        required_fields = ['first_name_1', 'last_name_1', 'email_1', 'phone_1', 'dob_1', 'address1_1', 'country_1', 'city_1', 'postal_code_1']
        for field in required_fields:
            if not request.form.get(field):
                return "Missing required field", 400  # 返回错误信息
        
        # Store passenger data in a dictionary
        passenger_data = {
            'number_of_passengers': request.form['passengers'],
            'first_name_1': request.form['first_name_1'],
            'last_name_1': request.form['last_name_1'],
            'middle_name_1': request.form.get('middle_name_1', ''),
            'id_number_1': request.form.get('id_number_1', ''),
            'email_1': request.form['email_1'],
            'phone_1': request.form['phone_1'],
            'dob_1': request.form['dob_1'],
            'address1_1': request.form['address1_1'],
            'address2_1': request.form.get('address2_1', ''),
            'country_1': request.form['country_1'],
            'city_1': request.form['city_1'],
            'postal_code_1': request.form['postal_code_1'],
            'em_first_name': request.form['em_first_name'],
            'em_last_name': request.form['em_last_name'],
            'em_phone': request.form['em_phone'],
            'em_email': request.form['em_email'],
            'bags': request.form['bags']
        }

        # Append the passenger data to the list
        passengers_data_store.append(passenger_data)

        # Print passenger data
        print("Stored Passenger Data:")
        for passenger in passengers_data_store:
            print(passenger)
        return "Passenger information submitted!"
    
    return render_template('booking.html')

@app.route('/view_passenger_data')
def view_passenger_data():
    # Return the entire list of stored passenger data
    return {"passenger_data": passengers_data_store}

if __name__ == '__main__':
    app.run(debug=True)
    
