import unittest
from flightbook import app
import random



class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        # Initialize the test client before each test case
        self.tester = app.test_client()
    

    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200) 


    def test_login_page(self):
        tester = app.test_client(self)
        response = tester.get('/login_page', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login Your Account', response.data)


    def test_login_success(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(username="aaa", password="aaa"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'/static/homepage/images/Welcome%20to%20G6%20flights.png', response.data)
    
    # test right username and wrong passord
    def test_login_fail1(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(username="aaa", password="wrong"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

    # test wrong username and right passord
    def test_login_fail2(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(username="wrong", password="aaa"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

    # test wrong username and wrong passord
    def test_login_fail3(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(username="wrone", password="wrong"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)



    def test_register(self):
        tester = app.test_client(self)
        response = tester.post('/register', data=dict(
            username='test'+ str(random.randint(1, 100000)),
            password= 'password',
            confirm_password= 'password',
            email= str(random.randint(1, 100000)) + '@test.com'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'/static/homepage/images/Welcome%20to%20G6%20flights.png', response.data)

    def test_register_password_mismatch(self):
        tester = app.test_client(self)
        response = tester.post('/register', data=dict(
            username="newuser",
            password="password",
            confirm_password="wrongpassword",
            email="newuser2@gmail.com"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Passwords do not match', response.data)

    def test_register_existing_username(self):
        tester = app.test_client(self)
        response = tester.post('/register', data=dict(
            username="aaa",  
            password="password",
            confirm_password="password",
            email="newuser3@gmail.com"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username is occupied', response.data) 

    def test_register_existing_email(self):
        tester = app.test_client(self)
        response = tester.post('/register', data=dict(
            username="asdfasdfasdfasdf",
            password="password",
            confirm_password="password",
            email="aaa@example.com" 
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email is occupied', response.data) 
    

    def test_logout(self):
        tester = app.test_client(self)
        tester.post('/login', data=dict(username="aaa", password="aaa"), follow_redirects=True)
        response = tester.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login / Sign up', response.data)  
        
    def test_incomplete_passengerinfo(self):
        self.tester.post('/login', data=dict(username="aaa", password="aaa"), follow_redirects=True)
        response = self.tester.post('/passenger_info', data=dict(
            first_name_1="Jeffery",
            last_name_1="",
            email_1="Jeffery@example.com",
            phone_1="1234567890",
            dob_1="1990-01-01",
            address1_1="123 Main St",
            country_1="USA",
            city_1="New York",
            postal_code_1="10001",
            em_first_name="James",
            em_last_name="",
            em_phone="1234567890",
            em_email="James@example.com",
            bags="1"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 400)


    def test_select_seat_page_load(self):
        self.tester.post('/login', data=dict(username="aaa", password="aaa"), follow_redirects=True)
        bookingid = "5a0c7eb0-345d-428b-8e2c-e2433f4e6026"
        response = self.tester.get(f'/select_seat/{bookingid}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_seat_selection_valid(self):
        self.tester.post('/login', data=dict(username="aaa", password="aaa"), follow_redirects=True)
        bookingid = "5a0c7eb0-345d-428b-8e2c-e2433f4e6026"
        response = self.tester.post(f'/select_seat/{bookingid}', data=dict(seat_number="4A"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_seat_selection_noselection(self):
        self.tester.post('/login', data=dict(username="aaa", password="aaa"), follow_redirects=True)
        bookingid = "5a0c7eb0-345d-428b-8e2c-e2433f4e6026"
        response = self.tester.post(f'/select_seat/{bookingid}', data=dict(seat_number=""), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_payment_successful(self):
        response = self.tester.post('/process_payment', data=dict(
            payment_method="credit_card",
            card_number="1234567812345678",
            expiration_date="12/24",
            cvv="123"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_payment_failure_missing_cvv(self):
        response = self.tester.post('/process_payment', data=dict(
            payment_method="credit_card",
            card_number="1234567812345678",
            expiration_date="12/24",
            cvv=""
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)



    def test_booking_history_with_records(self):
        self.tester.post('/login', data=dict(username="aaa", password="aaa"), follow_redirects=True)
        response = self.tester.get('/booking-history', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
 


    def test_flight_search_success(self):
        response = self.tester.post('/search-results', data=dict(
            from_city="Paris",
            to_city="New York",
            travellers_class="1 Traveller",
            departure_date="2024-11-05"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Flight Search Results', response.data)


    def test_flight_search_missing_fields(self):
        response = self.tester.post('/search-results', data=dict(
            to_city="New York",
            travellers_class="1 Traveller",
            departure_date="2024-11-05"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
