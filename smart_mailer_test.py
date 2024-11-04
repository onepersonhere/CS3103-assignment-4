import unittest
from unittest.mock import patch
import smtplib


class TestSimpleSMTP(unittest.TestCase):

    @patch.object(smtplib.SMTP_SSL, 'sendmail')  # Patch the sendmail method
    def test_send_email(self, mock_sendmail):  # mock_sendmail is passed as an argument
        print("Starting the test for sending email...")

        # Mock the behavior of the sendmail method
        mock_sendmail.return_value = None  # You can set this to whatever is appropriate

        # Import your function here to avoid circular imports
        from simple_smtp import send_email  # Ensure this points to your actual send_email function

        # Act: Call the function that sends the email
        send_email()  # This should invoke the sendmail method

        # Assert that sendmail was called
        self.assertTrue(mock_sendmail.called, "sendmail was not called")

        # Print the calls to sendmail for debugging
        print("Calls to sendmail:", mock_sendmail.call_args_list)

        # Check the call parameters of sendmail
        mock_sendmail.assert_called_once_with(
            'from@example.com',
            'to@example.com',
            'Subject: Test\n\nEmail body'
        )
        print("sendmail was called with expected parameters.")


if __name__ == "__main__":
    unittest.main()
