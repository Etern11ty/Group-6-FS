import unittest
from flightbook import app
import randominfo
import random
import string

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
            username="asdfasdfasdfasdf",
            password="password",
            confirm_password="password",
            email="aaa@example.com"  # 已存在的邮箱
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email is occupied', response.data) 
    

    def test_logout(self):
        tester = app.test_client(self)
        tester.post('/login', data=dict(username="aaa", password="aaa"), follow_redirects=True)
        response = tester.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login / Sign up', response.data)  


if __name__ == "__main__":
    unittest.main()