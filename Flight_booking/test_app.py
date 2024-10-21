import unittest
from flightbook import app

class FlaskTestCase(unittest.TestCase):
    
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
            username="newuser",
            password="password",
            confirm_password="password",
            email="newuser@gmail.com"
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
            username="aaa",  # 已存在的用户名
            password="password",
            confirm_password="password",
            email="newuser3@gmail.com"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username is occupied', response.data) 

    def test_register_existing_email(self):
        tester = app.test_client(self)
        response = tester.post('/register', data=dict(
            username="newuser2",
            password="password",
            confirm_password="password",
            email="aaa@gmail.com"  # 已存在的邮箱
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email is occupied', response.data) 
    

    def test_logout(self):
        tester = app.test_client(self)
        tester.post('/login', data=dict(username="aaa", password="aaa"), follow_redirects=True)
        response = tester.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login / Sign up', response.data)  

    def test_incomplete_passenger_info(self):
        tester = app.test_client(self)
        tester.post('/login', data=dict(username="aaa", password="aaa"), follow_redirects=True) 
        response = tester.post('/passenger_info', data=dict(
            passengers="1",
            first_name_1="Jeffery",
            last_name_1="",
            email_1="Jeffery@example.com",
            phone_1="1234567890",
            dob_1="1990-01-01",
            address1_1="123 Main St",
            country_1="USA",
            city_1="New York",
            postal_code_1="410700",
            em_first_name="James",
            em_last_name="",
            em_phone="1234567890",
            em_email="James@example.com",
            bags="2"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing required field', response.data) 

    def test_complete_passenger_info(self):
        tester = app.test_client(self)
        tester.post('/login', data=dict(username="aaa", password="aaa"), follow_redirects=True)  
        response = tester.post('/passenger_info', data=dict(
            passengers="1",
            first_name_1="Jeffery",
            last_name_1="Zhao",
            email_1="Jeffery@example.com",
            phone_1="1234567890",
            dob_1="1990-01-01",
            address1_1="123 Main St",
            country_1="USA",
            city_1="New York",
            postal_code_1="10001",
            em_first_name="James",
            em_last_name="Zhou",
            em_phone="1234567890",
            em_email="James@example.com",
            bags="2"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)  
        self.assertIn(b'Passenger information submitted!', response.data)

    def test_multiple_passenger_info(self):
        tester = app.test_client(self)
        tester.post('/login', data=dict(username="aaa", password="aaa"), follow_redirects=True)  
        response = tester.post('/passenger_info', data=dict(
            passengers="2",
            first_name_1="Jeffery",
            last_name_1="Zhao",
            email_1="Jeffery@example.com",
            phone_1="1234567890",
            dob_1="1990-01-01",
            address1_1="123 Main St",
            country_1="USA",
            city_1="New York",
            postal_code_1="10001",
            first_name_2="Michael",
            last_name_2="Chen",
            email_2="Michael@example.com",
            phone_2="0987654321",
            dob_2="1992-03-05",
            address1_2="456 Another St",
            country_2="USA",
            city_2="Boston",
            postal_code_2="02118",
            em_first_name="James",
            em_last_name="Zhou",
            em_phone="1234567890",
            em_email="James@example.com",
            bags="3"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)  
        self.assertIn(b'Passenger information submitted!', response.data)



if __name__ == "__main__":
    unittest.main()