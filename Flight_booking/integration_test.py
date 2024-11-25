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

# Test cases
def test_search_flights(flightbook):
    results = flightbook.search_flights("JFK", "LAX", "2024-12-01")
    assert len(results) == 2
    assert results[0]["flight_number"] == "FL123"

def test_select_flight(flightbook):
    flight = flightbook.select_flight("FL123")
    assert flight is not None
    assert flight["remaining_seats"] == 10

    no_seat_flight = flightbook.select_flight("FL456")
    assert no_seat_flight is None

def test_book_flight_success(flightbook):
    user_details = {"name": "John Doe", "email": "john@example.com"}
    booking = flightbook.book_flight("FL123", user_details)
    assert booking is not None
    assert booking["user"]["name"] == "John Doe"
    assert flightbook.flights[0]["remaining_seats"] == 9

def test_book_flight_no_remaining_seats(flightbook):
    """
    Test booking a flight with no remaining seats.
    """
    user_details = {"name": "Alice", "email": "alice@example.com"}
    booking = flightbook.book_flight("FL456", user_details)
    assert booking is None, "The system should return None, indicating the booking failed."
    flight = flightbook.select_flight("FL456")
    assert flight is None, "The flight has no remaining seats; select_flight should return None."

def test_search_no_flights(flightbook):
    """
    Test whether the system correctly returns an empty list when no flights match the search criteria.
    """
    results = flightbook.search_flights("JFK", "ORD", "2024-12-01")  # ORD is not a valid destination
    assert len(results) == 0, "The system should return an empty list since no flights match the criteria."

def test_book_flight_until_full(flightbook):
    """
    Test booking the same flight repeatedly until no seats are left.
    """
    user_details = {"name": "Bob", "email": "bob@example.com"}
    flight_number = "FL123"
    
    for i in range(10):  # This flight has a maximum of 10 seats
        booking = flightbook.book_flight(flight_number, user_details)
        assert booking is not None, f"The {i+1}th booking should succeed."
        assert flightbook.flights[0]["remaining_seats"] == 10 - (i + 1), f"The remaining seats should be {10 - (i + 1)}."

    booking = flightbook.book_flight(flight_number, user_details)
    assert booking is None, "The flight is fully booked, so the booking should fail."
    flight = flightbook.select_flight(flight_number)
    assert flight is None, "The flight has no remaining seats; select_flight should return None."
