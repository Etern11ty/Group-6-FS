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
    
    

    def test_login_fail(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(username="wrong", password="wrong"), follow_redirects=True)
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
            email="newuser@gmail.com"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Passwords do not match', response.data)

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
            first_name_1="John",
            last_name_1="", 
            email_1="john@example.com",
            phone_1="1234567890"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing required field', response.data) 

    def test_complete_passenger_info(self):
        tester = app.test_client(self)
        tester.post('/login', data=dict(username="aaa", password="aaa"), follow_redirects=True)  
        response = tester.post('/passenger_info', data=dict(
            passengers="1",
            first_name_1="John",
            last_name_1="Doe",
            email_1="john@example.com",
            phone_1="1234567890",
            dob_1="1990-01-01",
            address1_1="123 Main St",
            country_1="USA",
            city_1="New York",
            postal_code_1="10001",
            em_first_name="Jane",
            em_last_name="Doe",
            em_phone="1234567890",
            em_email="jane@example.com",
            bags="2"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)  
        self.assertIn(b'Passenger information submitted!', response.data)


if __name__ == "__main__":
    unittest.main()