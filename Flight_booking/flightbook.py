from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__, static_folder='static')

app.secret_key = 'aa2233'

username_list = ["aaa", "123"]
password_list = ["aaa", "123"]
email_list = ["aaa@gmail.com", "123@gmail.com"]


@app.route('/')
def index():
    # session['current_username'] = 'aaa'
    current_username = session.get('current_username', "Login / Sign up")
    return render_template('homepage.html', current_username=current_username)


@app.route('/process-booking', methods=['POST'])
def process_booking():
    # 获取用户提交的表单数据
    from_city = request.form.get('from_city')
    to_city = request.form.get('to_city')
    travellers_class = request.form.get('travellers_class')
    departure_date = request.form.get('departure_date')
    return_date = request.form.get('return_date')

    # 你可以在这里处理数据，例如打印到控制台或保存到数据库
    print(f"From: {from_city}")
    print(f"To: {to_city}")
    print(f"Travellers and Class: {travellers_class}")
    print(f"Departure Date: {departure_date}")
    print(f"Return Date: {return_date}")

    # 返回一个响应给用户
    return f"Booking details: From {from_city} to {to_city} for {travellers_class}, departing on {departure_date}, returning on {return_date}"


@app.route('/flights')
def flights():
    return render_template('homepage.html')


@app.route('/booking-history')
def booking_history():
    return 'booking_history.html'


@app.route('/login_page')
def login_page():
    return 'login.html'


@app.route('/cart')
def cart():
    return 'cart.html'


@app.route('/logout')
def logout():
    session.pop('current_username', None)
    return redirect(url_for('index'))



@app.route('/search-results')
def search_results():
    # 获取查询参数
    from_city = request.args.get('from')
    to_city = request.args.get('to')
    travellers = request.args.get('travellers')
    departure = request.args.get('departure')
    return_date = request.args.get('return')

    # 处理搜索逻辑并返回结果页面
    return 'searching result'

#
# @app.route('/')
# def index():
#     error = session.pop('error', None)
#     return render_template('login.html', error=error)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username in username_list and password in password_list:
        user_index = username_list.index(username)
        if password_list[user_index] == password:

            session['current_username'] = username

            return redirect(url_for('page_a'))
        
    session['error'] = "Invalid username or password"  
    return redirect(url_for('index')) 

@app.route('/page_a')
def page_a():
    return "Welcome to Page A!"

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

        return "homepage"

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

        # If there is a second passenger, add their details too
        if request.form['passengers'] == "2":
            passenger_data.update({
                'first_name_2': request.form['first_name_2'],
                'last_name_2': request.form['last_name_2'],
                'middle_name_2': request.form.get('middle_name_2', ''),
                'id_number_2': request.form.get('id_number_2', ''),
                'dob_2': request.form['dob_2'],
                'email_2': request.form.get('email_2', ''),
                'phone_2': request.form.get('phone_2', ''),
                'address1_2': request.form.get('address1_2', ''),
                'address2_2': request.form.get('address2_2', ''),
                'country_2': request.form.get('country_2', ''),
                'city_2': request.form.get('city_2', ''),
                'postal_code_2': request.form.get('postal_code_2', '')
            })
            
        # Append the passenger data to the list
        passengers_data_store.append(passenger_data)

        # Print passenger data
        print("Stored Passenger Data:")
        for passenger in passengers_data_store:
            print(passenger)
        # Save passenger data
        return "Passenger information submitted!"

    
    return render_template('booking.html')

@app.route('/view_passenger_data')
def view_passenger_data():
    # Return the entire list of stored passenger data
    return {"passenger_data": passengers_data_store}

if __name__ == '__main__':
    app.run(debug=True)
    
