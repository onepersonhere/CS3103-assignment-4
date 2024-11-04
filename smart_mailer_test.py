import unittest
from unittest.mock import patch, mock_open
import smtplib  # Ensure you import smtplib

class TestSimpleSMTP(unittest.TestCase):

    @patch.object(smtplib.SMTP_SSL, 'sendmail')  # Patch the sendmail method
    @patch("builtins.open", new_callable=mock_open, read_data="email,name\njohn@example.com,John Doe\n")  # Mock CSV data with one recipient
    def test_send_email(self, mock_open, mock_sendmail):  # mock_open and mock_sendmail are passed as arguments
        print("Starting the test for sending email...")

        # Mock the behavior of the sendmail method
        mock_sendmail.return_value = None  # Set the return value of sendmail

        # Import your function here to avoid circular imports
        from simple_smtp import send_email  # Ensure this points to your actual send_email function

        # Act: Call the function that sends the email
        send_email()  # This should invoke the sendmail method

        # Assert that sendmail was called
        self.assertTrue(mock_sendmail.called, "sendmail was not called")

        # Print the calls to sendmail for debugging
        print("Calls to sendmail:", mock_sendmail.call_args_list)

        # Check the call parameters of sendmail
        mock_sendmail.assert_called_once_with(  # Assert that sendmail was called with the correct parameters
            'from@example.com',
            'john@example.com',  # Use the email from the mocked CSV
            'Subject: Test\n\nEmail body'  # Adjust if your function has a different email body
        )
        print("sendmail was called with expected parameters.")

if __name__ == "__main__":
    unittest.main()
