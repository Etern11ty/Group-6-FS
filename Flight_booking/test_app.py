import unittest
from flightbook import app
import random
from flask import session
from unittest.mock import patch, MagicMock
import os


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        # Initialize the test client before each test case
        self.tester = app.test_client()
        app.testing = True
        app.config['PROPAGATE_EXCEPTIONS'] = True
        self.tester = app.test_client()

    

    @patch("flightbook.app.run")
    @patch("os.environ.get")
    def test_port_config(self, mock_environ_get, mock_run):
        mock_environ_get.return_value = "8080"
        port = int(os.environ.get("PORT", 8080))
        app.run(host="0.0.0.0", port=port)

        mock_run.assert_called_once_with(host="0.0.0.0", port=8080)

    

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

    @patch('flightbook.supabase')
    def test_flight_detail(self, mock_supabase):
        # 模拟请求表单数据
        flight_number = 'AB123'
        
        # 模拟 flight_information 表的返回数据
        mock_flight_response = MagicMock()
        mock_flight_response.data = [{'flight_number': flight_number, 'destination': 'New York', 'departure': 'Paris'}]
        mock_flight_response.error = None
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_flight_response

        # 模拟 price 表的返回数据
        mock_price_response = MagicMock()
        mock_price_response.data = [{'flight_number': flight_number, 'price': 500}]
        mock_price_response.error = None
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_price_response

        # 发送 POST 请求到 /flight_detail
        response = self.tester.post('/flight_detail', data={'flight_number': flight_number}, follow_redirects=True)
        
        # 检查响应状态码和 session 数据
        self.assertEqual(response.status_code, 200)
        with self.tester.session_transaction() as sess:
            flight_info = sess.get('flight_info')
            self.assertIsNotNone(flight_info)
            self.assertEqual(flight_info['flight_number'], flight_number)
            self.assertEqual(flight_info['price'], 500)

    @patch('flightbook.supabase')
    def test_passenger_info_upsert_success(self, mock_supabase):
        with self.tester.session_transaction() as sess:
            sess['current_username'] = 'test_user'
        data = {
            'first_name_1': 'John', 'last_name_1': 'Doe', 'email_1': 'johndoe@example.com',
            'phone_1': '1234567890', 'dob_1': '1990-01-01', 'address1_1': '123 Test St',
            'country_1': 'USA', 'city_1': 'Test City', 'postal_code_1': '10001',
            'em_first_name': 'Jane', 'em_last_name': 'Doe', 'em_phone': '0987654321', 'em_email': 'janedoe@example.com'
        }
        mock_upsert_response = MagicMock()
        mock_upsert_response.error = None
        mock_supabase.table.return_value.upsert.return_value.execute.return_value = mock_upsert_response
        mock_select_response = MagicMock()
        mock_select_response.data = [{'username': 'test_user', 'firstname': 'John', 'lastname': 'Doe'}]
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_select_response
        response = self.tester.post('/passenger_info', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John', response.data)

    @patch('flightbook.supabase')
    def test_passenger_info_upsert_failure(self, mock_supabase):
        with self.tester.session_transaction() as sess:
            sess['current_username'] = 'test_user'
        data = {
            'first_name_1': 'John', 'last_name_1': 'Doe', 'email_1': 'johndoe@example.com',
            'phone_1': '1234567890', 'dob_1': '1990-01-01', 'address1_1': '123 Test St',
            'country_1': 'USA', 'city_1': 'Test City', 'postal_code_1': '10001',
            'em_first_name': 'Jane', 'em_last_name': 'Doe', 'em_phone': '0987654321', 'em_email': 'janedoe@example.com'
        }
        mock_upsert_response = MagicMock()
        mock_upsert_response.error = 'Mocked Error'
        mock_supabase.table.return_value.upsert.return_value.execute.return_value = mock_upsert_response
        response = self.tester.post('/passenger_info', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Error adding passenger data: Mocked Error', response.data)
        
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


    def test_unlogin_passengerinfo(self):
        self.tester.post('/login', data=dict(username="", password=""), follow_redirects=True)
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
        self.assertIn(b'User not authenticated', response.data) 

    def test_complete_passengerinfo(self):
        with self.tester.session_transaction() as sess:
            sess['flight_info'] = {'price': 100}  
        self.tester.post('/login', data=dict(username="aaa", password="aaa"), follow_redirects=True)
        response = self.tester.post('/passenger_info', data=dict(
            first_name_1="Jeffery",
            last_name_1="Zhao",
            email_1="Jeffery@example.com",
            phone_1="1234567890",
            id_number_1 = '111',
            dob_1="1990-01-01",
            address1_1="123 Main St",
            country_1="USA",
            city_1="New York",
            postal_code_1="10001",
            em_first_name="James",
            em_last_name="Qin",
            em_phone="1234567890",
            em_email="James@example.com",
            bags="1"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Total:', response.data) 

    def test_invalid_passengerdob(self):
        with self.tester.session_transaction() as sess:
            sess['flight_info'] = {'price': 100} 
        self.tester.post('/login', data=dict(username="aaa", password="aaa"), follow_redirects=True)
        response = self.tester.post('/passenger_info', data=dict(
            first_name_1="Jeffery",
            last_name_1="Zhao",
            email_1="Jeffery@example.com",
            phone_1="1234567890",
            id_number_1 = '111',
            dob_1="199000-01-01",
            address1_1="123 Main St",
            country_1="USA",
            city_1="New York",
            postal_code_1="10001",
            em_first_name="James",
            em_last_name="Qin",
            em_phone="1234567890",
            em_email="James@example.com",
            bags="1"
        ), follow_redirects=True)
        self.assertIn(b'Invalid date format for birthday', response.data) 


    @patch('flightbook.supabase')
    def test_passenger_info_upsert_error(self, mock_supabase):
        """测试 upsert 时返回错误信息"""
        with self.tester.session_transaction() as sess:
            sess['current_username'] = 'test_user'
        
        # 模拟 upsert 返回错误
        mock_upsert_response = MagicMock()
        mock_upsert_response.error = 'Mocked Error'
        mock_supabase.table.return_value.upsert.return_value.execute.return_value = mock_upsert_response

        response = self.tester.post('/passenger_info', data={
            'first_name_1': 'John', 'last_name_1': 'Doe', 'email_1': 'johndoe@example.com',
            'phone_1': '1234567890', 'dob_1': '1990-01-01', 'address1_1': '123 Test St',
            'country_1': 'USA', 'city_1': 'Test City', 'postal_code_1': '10001',
            'em_first_name': 'Jane', 'em_last_name': 'Doe', 'em_phone': '0987654321', 'em_email': 'janedoe@example.com'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Error adding passenger data: Mocked Error', response.data)


    @patch('flightbook.supabase')
    def test_passenger_info_select_error(self, mock_supabase):
        """测试从数据库中获取乘客信息时返回错误"""
        with self.tester.session_transaction() as sess:
            sess['current_username'] = 'test_user'

        # 模拟数据库查询返回错误
        mock_select_response = MagicMock()
        mock_select_response.data = None
        mock_select_response.error = 'Mocked Select Error'
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_select_response

        response = self.tester.get('/passenger_info', follow_redirects=True)
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'error', response.data)


    @patch('flightbook.supabase')
    def test_fetch_passenger_info_error(self, mock_supabase):
        """测试从数据库中获取乘客信息页面时返回错误"""
        with self.tester.session_transaction() as sess:
            sess['current_username'] = 'test_user'

        # 模拟数据库查询返回错误
        mock_select_response = MagicMock()
        mock_select_response.error = 'Mocked Fetch Error'
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_select_response

        response = self.tester.get('/passenger_info', follow_redirects=True)
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'An error occurred while fetching data: Mocked Fetch Error', response.data)

        


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


    @patch('flightbook.supabase')
    def test_finalize_payment_success(self, mock_supabase):
        # 模拟 session 数据
        with self.tester.session_transaction() as sess:
            sess['current_username'] = 'test_user'
            sess['flight_info'] = {
                'flight_number': 'AB123',
                'departure': 'Paris',
                'destination': 'New York',
                'origin': 'CDG',
                'dest': 'JFK',
                'date': '2024-12-01',
                'departure_time': '10:00',
                'arrival_time': '13:00'
            }
            sess['passenger_data'] = {
                'firstname': 'John',
                'lastname': 'Doe'
            }

        # 模拟 Supabase 插入操作
        mock_insert_response = MagicMock()
        mock_insert_response.error = None
        mock_supabase.table.return_value.insert.return_value.execute.return_value = mock_insert_response

        # 发送 GET 请求到 /finalize_payment
        response = self.tester.get('/finalize_payment', follow_redirects=True)

        # 检查响应状态码和重定向目标
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Flight booked successfully', response.data)  # 假设 paymentsuccess 页面包含 "Payment Success"

        # 验证数据是否正确插入
        mock_supabase.table.assert_called_with("bookinghistory")
        mock_supabase.table.return_value.insert.assert_called()
        booking_data = mock_supabase.table.return_value.insert.call_args[0][0]  # 获取插入的数据

        # 检查插入的 booking_data 是否包含正确的字段
        self.assertEqual(booking_data['username'], 'test_user')
        self.assertEqual(booking_data['flightnumber'], 'AB123')
        self.assertEqual(booking_data['first_name'], 'John')
        self.assertEqual(booking_data['last_name'], 'Doe')
        self.assertEqual(booking_data['origin'], 'Paris')
        self.assertEqual(booking_data['dest'], 'New York')
        self.assertEqual(booking_data['origin_code'], 'CDG')
        self.assertEqual(booking_data['dest_code'], 'JFK')
        self.assertEqual(booking_data['date'], '2024-12-01')
        self.assertEqual(booking_data['dept_time'], '10:00')
        self.assertEqual(booking_data['arrive_time'], '13:00')



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


    def test_flight_search_missing_fields(self):
        response = self.tester.post('/search-results', data=dict(
            to_city="New York",
            travellers_class="1 Traveller",
            departure_date="2024-11-05"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    @patch('flightbook.supabase')
    def test_confirm_seat_get_success(self, mock_supabase):
        with self.tester.session_transaction() as sess:
            sess['current_username'] = 'test_user'
        
        # 模拟 Supabase 的 select 返回值
        mock_seat_response = MagicMock()
        mock_seat_response.data = [{'seat_number': '4A', 'status': 'available'}]
        mock_seat_response.error = None
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_seat_response

        response = self.tester.get('/confirm_seat/123', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Seat Booking Successfully', response.data) 

    @patch('flightbook.supabase')
    def test_confirm_seat_post_success(self, mock_supabase):
        with self.tester.session_transaction() as sess:
            sess['current_username'] = 'test_user'
        
        # 模拟座位未被预订
        mock_seat_response = MagicMock()
        mock_seat_response.data = []
        mock_seat_response.error = None
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_seat_response
        
        # 模拟座位更新成功
        mock_update_response = MagicMock()
        mock_update_response.data = [{'seat_number': '4A', 'status': 'occupied'}]
        mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = mock_update_response

        response = self.tester.post('/confirm_seat/123', data={'seat': '4A'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Seat Booking Successfully', response.data)

    @patch('flightbook.supabase')
    def test_confirm_seat_post_seat_already_booked(self, mock_supabase):
        with self.tester.session_transaction() as sess:
            sess['current_username'] = 'test_user'
        
        # 模拟座位已被预订
        mock_seat_response = MagicMock()
        mock_seat_response.data = [{'seat_number': '4A', 'status': 'occupied'}]
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_seat_response

        response = self.tester.post('/confirm_seat/123', data={'seat': '4A'}, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Seat is already booked. Please choose another seat.', response.data)

    @patch('flightbook.supabase')
    def test_confirm_seat_post_no_seat_selected(self, mock_supabase):
        with self.tester.session_transaction() as sess:
            sess['current_username'] = 'test_user'

        response = self.tester.post('/confirm_seat/123', data={'seat': ''}, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'No seat selected', response.data)



    def test_finalize_payment_missing_booking_data(self):
        # Clear session data
        with self.tester.session_transaction() as sess:
            sess.pop('flight_info', None)
            sess.pop('passenger_data', None)

        response = self.tester.get('/finalize_payment', follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing booking data', response.data)

    @patch('flightbook.supabase')
    def test_passenger_info_get_exception(self, mock_supabase):
        with self.tester.session_transaction() as sess:
            sess['current_username'] = 'test_user'

        # Simulate an exception when fetching data
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = Exception('Database Error')

        response = self.tester.get('/passenger_info')
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'An error occurred while fetching data: Database Error', response.data)


    @patch('flightbook.supabase')
    def test_passenger_info_get_no_data(self, mock_supabase):
        with self.tester.session_transaction() as sess:
            sess['current_username'] = 'test_user'

        # Simulate no data returned
        mock_response = MagicMock()
        mock_response.data = []
        mock_response.error = None
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

        response = self.tester.get('/passenger_info')
        self.assertEqual(response.status_code, 200)
        # Adjust based on what your template displays when there's no data
        self.assertIn(b'Passenger Information', response.data)



    def test_passenger_info_missing_required_fields(self):
        with self.tester.session_transaction() as sess:
            sess['current_username'] = 'test_user'
        
        data = {
            # Missing 'first_name_1'
            'last_name_1': 'Doe',
            'email_1': 'johndoe@example.com',
            'phone_1': '1234567890',
            'dob_1': '1990-01-01',
            'address1_1': '123 Test St',
            'country_1': 'USA',
            'city_1': 'Test City',
            'postal_code_1': '10001',
            'em_first_name': 'Jane',
            'em_last_name': 'Doe',
            'em_phone': '0987654321',
            'em_email': 'janedoe@example.com'
        }

        response = self.tester.post('/passenger_info', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing required field', response.data)

    def test_passenger_info_invalid_date_format(self):
        with self.tester.session_transaction() as sess:
            sess['current_username'] = 'test_user'
        
        data = {
            'first_name_1': 'John',
            'last_name_1': 'Doe',
            'email_1': 'johndoe@example.com',
            'phone_1': '1234567890',
            'dob_1': 'invalid-date',
            'address1_1': '123 Test St',
            'country_1': 'USA',
            'city_1': 'Test City',
            'postal_code_1': '10001',
            'em_first_name': 'Jane',
            'em_last_name': 'Doe',
            'em_phone': '0987654321',
            'em_email': 'janedoe@example.com'
        }

        response = self.tester.post('/passenger_info', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid date format for birthday', response.data)



    def test_paymentsuccess_missing_booking_data(self):
        # Clear session data
        with self.tester.session_transaction() as sess:
            sess.pop('flight_info', None)
            sess.pop('passenger_data', None)

        response = self.tester.get('/paymentsuccess', follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing booking data', response.data)



    @patch('flightbook.supabase')
    def test_confirm_seat_exception(self, mock_supabase):
        with self.tester.session_transaction() as sess:
            sess['current_username'] = 'test_user'

        # Mock the select chain
        mock_select = MagicMock()
        mock_select.eq.return_value = mock_select  # First eq()
        mock_select.eq.return_value = mock_select  # Second eq()
        mock_select.execute.return_value.data = []
        mock_supabase.table.return_value.select.return_value = mock_select

        # Mock the update chain
        mock_update = MagicMock()
        mock_update.eq.return_value = mock_update  # First eq()
        mock_update.eq.return_value = mock_update  # Second eq()
        mock_update.execute.side_effect = Exception('Database Error')
        mock_supabase.table.return_value.update.return_value = mock_update

        response = self.tester.post('/confirm_seat/123', data={'seat': '4A'}, follow_redirects=False)
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'An error occurred while booking the seat: Database Error', response.data)



    def test_booking_history_unauthenticated(self):
        # Ensure no user is logged in
        with self.tester.session_transaction() as sess:
            sess.pop('current_username', None)

        response = self.tester.get('/booking-history', follow_redirects=True)
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'User not authenticated', response.data)


    @patch('flightbook.supabase')
    def test_booking_history_no_bookings(self, mock_supabase):
        with self.tester.session_transaction() as sess:
            sess['current_username'] = 'test_user'

        # Simulate no bookings returned
        mock_response = MagicMock()
        mock_response.data = []
        mock_response.error = None
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

        response = self.tester.get('/booking-history', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Adjust the assertion based on your template
        self.assertIn(b'You have no bookings.', response.data)


    def test_select_seat_unauthenticated(self):
        # Ensure no user is logged in
        with self.tester.session_transaction() as sess:
            sess.pop('current_username', None)

        response = self.tester.get('/select_seat/123', follow_redirects=True)
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'User not authenticated', response.data)



    @patch('flightbook.supabase')
    def test_select_seat_already_occupied(self, mock_supabase):
        with self.tester.session_transaction() as sess:
            sess['current_username'] = 'test_user'

        # Mock the select chain
        mock_select = MagicMock()
        mock_select.eq.return_value = mock_select  # First eq()
        mock_select.eq.return_value = mock_select  # Second eq()
        mock_select.execute.return_value.data = [{'status': 'occupied', 'seat_number': '4A', 'flight_id': 'flight123'}]
        mock_supabase.table.return_value.select.return_value = mock_select

        response = self.tester.get('/select_seat/booking123', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/seat_confirmation/booking123/4A', response.headers['Location'])



    def test_home_redirects_to_passenger_info(self):
        response = self.tester.get('/home_redirect', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/passenger_info', response.headers['Location'],'/')
        

    def test_view_booking_history_page(self):
        response = self.tester.get('/view_booking_history')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Booking History', response.data)  # Adjust based on your template


    def test_go_home_redirects_to_index(self):
        response = self.tester.get('/home', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/')
        
    def test_register_page_load(self):
        response = self.tester.get('/register')
        self.assertEqual(response.status_code, 200)
        
    @patch('flightbook.supabase')
    def test_passenger_info_existing_data(self, mock_supabase):
        # Set up session to include current username
        with self.tester.session_transaction() as sess:
            sess['current_username'] = 'test_user'

        # Mock Supabase response to simulate existing data
        mock_response = MagicMock()
        mock_response.data = [{
            'username': 'test_user',
            'firstname': 'John',
            'lastname': 'Doe',
            'emailaddress': 'johndoe@example.com'
        }]
        mock_response.error = None
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

        # Perform the GET request to `/passenger_info`
        response = self.tester.get('/passenger_info')

        # Assertions to ensure lines 276-277 are covered
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John', response.data)
        self.assertIn(b'Doe', response.data)
        


if __name__ == "__main__":
    unittest.main()
