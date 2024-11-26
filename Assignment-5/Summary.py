from fpdf import FPDF

# Create a PDF instance
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Integration Test Summary and Instructions', align='C', ln=True)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

# Initialize the PDF
pdf = PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

pdf.set_font('Arial', 'B', 14)
pdf.cell(0, 10, 'Test Summary', ln=True)
pdf.set_font('Arial', '', 12)

pdf.multi_cell(0, 10, '''
IntegrationTestCase:

Full Booking Process:
This script tests the full booking process in the system. It includes:
- Logging in as an existing user.
- Searching for flights.
- Viewing flight details.
- Submitting passenger information.
- Processing payment.
- Finalizing payment.
- Verifying the booking in the booking history.

Purpose: To ensure that the entire flight booking flow works seamlessly from start to finish.

IntegrationTestLoginAndSeatSelection:
This script focuses on:
- Logging in as a mock user.
- Viewing the user's booking history.
- Simulating seat selection for a flight.
- Logging out after the process.

Purpose: To verify login functionality, the ability to view booking history, and select seats, ensuring all operations are functional.

UserRegistrationAndSearchIntegrationTest:
This script tests:
- Registering a new user.
- Logging in as the new user.
- Searching for flights with specific criteria.
- Logging out after the search.

Purpose: To ensure user registration and flight search functionality works correctly.
''')

# Add content for the test instructions
pdf.add_page()
pdf.set_font('Arial', 'B', 14)
pdf.cell(0, 10, 'Instructions for Running Integration Test Scripts', ln=True)
pdf.set_font('Arial', '', 12)

pdf.multi_cell(0, 10, '''
Prerequisites:
1. Ensure Python 3.7 or higher is installed.
2. Install the required dependencies using:
   pip install flask pytest unittest supabase fpdf

3. Configure the .env file with the following variables:
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key

4. Ensure your Supabase database contains required tables:
   - user_account
   - flight_information
   - seats
   - bookinghistory

Running Tests:
1. Navigate to the project directory:
   cd /path/to/project/Flight_booking

2. Run the tests:
   - For unittest scripts:
     python integration_test.py
   - For pytest scripts:
     pytest integration_test.py

3. Check the results in the terminal.

Common Issues:
- Missing dependencies: Reinstall with pip.
- Database connection issues: Verify .env settings.
- Port conflicts: Update the port in flightbook.py if needed.
''')



# Save PDF
pdf.output("Summary_of_Integration.pdf")
