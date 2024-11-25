import pytest

# Mocking flight book system for demonstration
class FlightBook:
    def __init__(self):
        self.flights = [
            {"flight_number": "FL123", "departure": "JFK", "destination": "LAX", "date": "2024-12-01", "remaining_seats": 10},
            {"flight_number": "FL456", "departure": "JFK", "destination": "LAX", "date": "2024-12-01", "remaining_seats": 0},
        ]
        self.bookings = []

    def search_flights(self, departure, destination, date):
        return [f for f in self.flights if f["departure"] == departure and f["destination"] == destination and f["date"] == date]

    def select_flight(self, flight_number):
        for flight in self.flights:
            if flight["flight_number"] == flight_number:
                return flight if flight["remaining_seats"] > 0 else None
        return None

    def book_flight(self, flight_number, user_details):
        flight = self.select_flight(flight_number)
        if flight:
            flight["remaining_seats"] -= 1
            booking = {"flight_number": flight_number, "user": user_details}
            self.bookings.append(booking)
            return booking
        return None

# Fixtures for test setup
@pytest.fixture
def flightbook():
    return FlightBook()

# Integration Test Cases
def test_complete_booking_process_success(flightbook):
    """
    Test the complete process from searching for flights to successfully booking one.
    """
    # Step 1: Search for flights
    search_results = flightbook.search_flights("JFK", "LAX", "2024-12-01")
    assert len(search_results) > 0, "There should be at least one flight available for booking."

    # Step 2: Select a flight
    flight_to_book = flightbook.select_flight("FL123")
    assert flight_to_book is not None, "The flight should be available for booking."
    assert flight_to_book["remaining_seats"] == 10, "The flight should have 10 seats available initially."

    # Step 3: Book the flight
    user_details = {"name": "John Doe", "email": "john@example.com"}
    booking = flightbook.book_flight("FL123", user_details)
    assert booking is not None, "The booking should be successful."
    assert booking["user"]["name"] == "John Doe", "The booking should include the correct user details."
    assert flightbook.flights[0]["remaining_seats"] == 9, "The flight should now have 9 seats remaining."

def test_complete_booking_process_failure_no_seats(flightbook):
    """
    Test the complete process when attempting to book a flight with no available seats.
    """
    # Step 1: Search for flights
    search_results = flightbook.search_flights("JFK", "LAX", "2024-12-01")
    assert len(search_results) > 0, "There should be at least one flight available for booking."

    # Step 2: Attempt to select a flight with no seats
    flight_to_book = flightbook.select_flight("FL456")
    assert flight_to_book is None, "The flight should not be available for booking because there are no remaining seats."

    # Step 3: Attempt to book the flight
    user_details = {"name": "Alice", "email": "alice@example.com"}
    booking = flightbook.book_flight("FL456", user_details)
    assert booking is None, "Booking should fail as the flight has no available seats."

def test_booking_until_fully_booked(flightbook):
    """
    Test booking a flight repeatedly until all seats are taken, and ensure further bookings are blocked.
    """
    # Step 1: Search for flights
    search_results = flightbook.search_flights("JFK", "LAX", "2024-12-01")
    assert len(search_results) > 0, "There should be at least one flight available for booking."

    # Step 2: Book the flight repeatedly until it is fully booked
    user_details = {"name": "Bob", "email": "bob@example.com"}
    flight_number = "FL123"

    for i in range(10):  # This flight has a maximum of 10 seats
        booking = flightbook.book_flight(flight_number, user_details)
        assert booking is not None, f"The {i+1}th booking should succeed."
        assert flightbook.flights[0]["remaining_seats"] == 10 - (i + 1), f"The remaining seats should be {10 - (i + 1)}."

    # Step 3: Attempt to book one more seat
    booking = flightbook.book_flight(flight_number, user_details)
    assert booking is None, "The flight is fully booked, so the booking should fail."
