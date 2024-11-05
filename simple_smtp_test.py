import unittest
from unittest.mock import patch, mock_open
import smtplib  # Ensure you import smtplib


def multi_mock_open(*file_contents):
    """Create a mock "open" that will mock open multiple files in sequence
    Args:
        *file_contents ([str]): a list of file contents to be returned by open
    Returns:
        (MagicMock) a mock opener that will return the contents of the first
            file when opened the first time, the second file when opened the
            second time, etc.
    """
    mock_files = [mock_open(read_data=content).return_value for content in file_contents]
    mock_opener = mock_open()
    mock_opener.side_effect = mock_files

    return mock_opener

class TestSimpleSMTP(unittest.TestCase):
    file_contents = [
        "email,name\njohn@example.com,John Doe\n",
        "Subject: Test\n\nEmail body"
        ]

    @patch("builtins.open", new_callable=lambda: multi_mock_open(*TestSimpleSMTP.file_contents))
    @patch.object(smtplib.SMTP_SSL, 'sendmail')
    def test_send_email(self, mock_sendmail, mock_open):
        print("Starting the test for sending email...")

        from simple_smtp import send_email

        send_email()

        self.assertTrue(mock_sendmail.called, "sendmail was not called")
        print("Calls to sendmail:", mock_sendmail.call_args_list)

        mock_sendmail.assert_called_once_with(
            'from@example.com',
            'john@example.com',
            'Subject: Test\n\nEmail body'
        )
        print("sendmail was called with expected parameters.")

if __name__ == "__main__":
    unittest.main()
