from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time

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
    username = session.get('current_username')
    if not username:
        return "User not authenticated", 401
    
    # Fetch booking history for the current user
    response = supabase.table("bookinghistory").select("*").eq("username", username).execute()
    
    if response.data:
        bookings = response.data  # User's booking history
    else:
        bookings = []
    now = datetime.now()
    return render_template('booking_history.html', bookings=bookings, now=now)


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

    flight_info['price'] = flight_price
    session['flight_info'] = flight_info

    # use flight_info = json.loads(session.get('flight_info', '{}')) to get info

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
        
        session['passenger_data'] = passenger_data
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
            return render_template('payment.html', flight = session.get('flight_info'), passenger = passenger_data)

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


@app.route('/process_payment', methods=['POST'])
def process_payment():
    return render_template('loading.html'), 200
    
@app.route('/finalize_payment')
def finalize_payment():

    time.sleep(3)

    flight_info = session.get('flight_info')
    passenger_info = session.get('passenger_data')
    
    if not flight_info or not passenger_info:
        return "Missing booking data", 400

    booking_data = {
        "username": session.get('current_username'),
        "flightnumber": flight_info.get('flight_number'),
        "purchase_time": 'now()',
        "first_name": passenger_info.get('firstname'),
        "last_name": passenger_info.get('lastname'),
        "origin": flight_info.get('departure'),
        "dest": flight_info.get('destination'),
        "origin_code": flight_info.get('origin'),
        "dest_code": flight_info.get('dest'),
        "date": flight_info.get('date'),
        "dept_time": flight_info.get('departure_time'),
        "arrive_time": flight_info.get('arrival_time'),

    }

    supabase.table("bookinghistory").insert(booking_data).execute()

    return redirect(url_for('paymentsuccess'))

@app.route('/paymentsuccess')
def paymentsuccess():
    # Retrieve necessary data from the session
    flight_info = session.get('flight_info')
    passenger_info = session.get('passenger_data')  # Assumes passenger_data includes first/last names
    
    if not flight_info or not passenger_info:
        return "Missing booking data", 400

    print("Flight info:", flight_info)
    print("Passenger info:", passenger_info)

    return render_template('paymentsuccess.html', flight_info=flight_info, passenger_info=passenger_info)

@app.route('/select_seat', methods=['GET'])
def select_seat():
    flight_number = request.args.get('flight_number')
    # 这里可以添加逻辑，例如展示选择座位的页面
    return render_template('select_seat.html', flight_number=flight_number)

@app.route('/view_booking_history')
def view_booking_history():
    return render_template('booking_history.html')

@app.route('/home')
def go_home():
    return redirect(url_for('index'))



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
    
    
@app.route('/select_seat/<string:flight_id>', methods=['GET', 'POST'])
def select_seat(flight_id):
    current_username = session.get('current_username')
    if not current_username:
        return "User not authenticated", 401

    user_seat_response = supabase.table("seats").select("*").eq("flight_id", flight_id).eq("username", current_username).execute()
    
    response = user_seat_response.data[0]
    
    if response['status'] == 'occupied':
 
        selected_seat = response['seat_number']
        return redirect(url_for('seat_confirmation', flight_id=flight_id, seat=selected_seat))

    response = supabase.table("seats").select("*").eq("flight_id", flight_id).execute()
    seats = response.data if response.data else []

    return render_template('select_seat.html', seats=seats, flight_id=flight_id)




@app.route('/confirm_seat/<string:flight_id>', methods=['GET', 'POST'])
def confirm_seat(flight_id):

    current_username = session.get('current_username')
    if not current_username:
        return "User not authenticated", 401


    if request.method == 'GET':
     
        seat_response = supabase.table("seats").select("*").eq("flight_id", flight_id).execute()
        if seat_response.error:
            return f"Error fetching seat data: {seat_response.error}", 500
        
        seats = seat_response.data if seat_response.data else []
  
        return render_template('confirm_seat.html', flight_id=flight_id, seats=seats)

    elif request.method == 'POST':
   
        selected_seat = request.form.get('seat')

        if not selected_seat:
            return "No seat selected", 400
        

        seat_response = supabase.table("seats").select("seat_number").eq("flight_id", flight_id).execute()
        
        seat_numbers = [seat['seat_number'] for seat in seat_response.data]

        
        print(seat_numbers)
        
        if selected_seat in seat_numbers:
            return "Seat is already booked. Please choose another seat.", 400


        try:
            response = supabase.table("seats").update({
                "status": "occupied",
                "seat_number": selected_seat,
            }).eq("flight_id", flight_id).eq("username", current_username).execute()

            print(f"Update Seat Response: {response}")

            if not response or not response.data:
                return "Failed to book seat. Please try again later.", 500

        except Exception as e:
            return f"An error occurred while booking the seat: {str(e)}", 500

        return redirect(url_for('seat_confirmation', flight_id=flight_id, seat=selected_seat))

@app.route('/seat_confirmation/<string:flight_id>/<string:seat>')
def seat_confirmation(flight_id, seat):
    return render_template('confirm_seat.html', flight_id=flight_id, seat=seat)





if __name__ == '__main__':
    app.run(debug=True)
    
