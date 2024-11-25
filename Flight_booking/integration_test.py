import unittest
from flightbook import app
import re
from flask import session

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        # Initialize the test client before each test case
        self.tester = app.test_client()
        app.testing = True
        app.config['PROPAGATE_EXCEPTIONS'] = True

    def test_full_booking_process(self):
        # Step 1: Log in as an existing user
        login_response = self.tester.post('/login', data=dict(
            username="aaa", 
            password="aaa"
        ), follow_redirects=True)
        self.assertEqual(login_response.status_code, 200)
        self.assertIn(b'Welcome', login_response.data)

        # Step 2: Search for flights
        search_data = dict(
            trip="oneway",
            from_city="Paris",
            to_city="New York",
            travellers_class="1 Traveller",
            departure_date="2024-12-01"
        )
        search_response = self.tester.post('/search-results', data=search_data, follow_redirects=True)
        self.assertEqual(search_response.status_code, 200)

        # Extract flight_number from the search results
        search_page = search_response.data.decode('utf-8')
        match = re.search(r'name="flight_number" value="(.*?)"', search_page)
        if match:
            flight_number = match.group(1)
        else:
            self.fail("No flight_number found in search results")

        # Step 3: View flight details
        flight_detail_response = self.tester.post('/flight_detail', data=dict(
            flight_number=flight_number
        ), follow_redirects=True)
        self.assertEqual(flight_detail_response.status_code, 200)
        self.assertIn(flight_number.encode(), flight_detail_response.data)

        # Step 4: Submit passenger information
        passenger_data = dict(
            first_name_1="John",
            last_name_1="Doe",
            email_1="johndoe@example.com",
            phone_1="1234567890",
            dob_1="1990-01-01",
            address1_1="123 Main St",
            country_1="USA",
            city_1="New York",
            postal_code_1="10001",
            em_first_name="Jane",
            em_last_name="Doe",
            em_phone="0987654321",
            em_email="janedoe@example.com"
        )
        passenger_info_response = self.tester.post('/passenger_info', data=passenger_data, follow_redirects=True)
        self.assertEqual(passenger_info_response.status_code, 200)
        self.assertIn(b'Payment', passenger_info_response.data)

        # Step 5: Process payment
        payment_data = dict(
            payment_method="credit_card",
            card_number="4111111111111111",
            expiration_date="12/24",
            cvv="123"
        )
        payment_response = self.tester.post('/process_payment', data=payment_data, follow_redirects=True)
        self.assertEqual(payment_response.status_code, 200)
        self.assertIn(b'Processing your payment...', payment_response.data)

        # Step 6: Finalize payment
        finalize_response = self.tester.get('/finalize_payment', follow_redirects=True)
        self.assertEqual(finalize_response.status_code, 200)
        self.assertIn(b'Flight booked successfully', finalize_response.data)

        # Step 7: Verify booking in booking history
        booking_history_response = self.tester.get('/booking-history', follow_redirects=True)
        self.assertEqual(booking_history_response.status_code, 200)
        self.assertIn(flight_number.encode(), booking_history_response.data)

if __name__ == "__main__":
    unittest.main()
