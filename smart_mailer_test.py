import unittest
from unittest.mock import patch, mock_open
import smtplib  # Ensure you import smtplib
from smart_mailer import smart_mailer


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

import unittest
from unittest.mock import patch, MagicMock, mock_open

class TestSmartMailer(unittest.TestCase):

    file_contents = ["""email,name,department_code
john@example.com,John Doe,IT
jane@example.com,Jane Smith,HR
mark@example.com,Mark Brown,IT
amy@example.com,Amy Green,Finance
""", """<html>
<body>
<h1>Hello #name#,</h1>
<p>Welcome to the #department# department update!</p>
<img src="http://yourserver.com/tracker.png" alt="." width="1" height="1">
</body>
</html>"""]

    def setUp(self):
        # Mock data
        self.subject = "Department Update"
        self.sender_email = "wertkwh@gmail.com"
        self.sender_password = "vjctutvxuqrwtarr"

    @patch("builtins.open", new_callable=lambda: multi_mock_open(*TestSmartMailer.file_contents))
    @patch.object(smtplib.SMTP_SSL, 'sendmail')
    def test_sending_emails_to_filtered_departments(self, mock_sendmail, mock_open):
        print("Starting the test for sending email...")

        # Run the smart mailer function with department filter
        smart_mailer(
            input_file="maildata.csv",
            department_code="IT",
            subject=self.subject,
            body_file="mail_body.html",
            sender_email=self.sender_email,
            sender_password=self.sender_password
        )

        self.assertTrue(mock_sendmail.called, "sendmail was not called")

        # print("Calls to sendmail:", mock_sendmail.call_args_list)

        # Verify that emails were only sent to IT department
        expected_emails = ["john@example.com", "mark@example.com"]
        sent_emails = [args[0][1] for args in mock_sendmail.call_args_list]

        self.assertCountEqual(sent_emails, expected_emails, "Should only send emails to 'IT' department")

    @patch("builtins.open", new_callable=lambda: multi_mock_open(*TestSmartMailer.file_contents))
    @patch.object(smtplib.SMTP_SSL, 'sendmail')
    def test_sending_emails_to_all_departments(self, mock_sendmail, mock_open):
        from smart_mailer import smart_mailer

        # Run the smart mailer function with "all" department code
        smart_mailer(
            input_file="maildata.csv",
            department_code="all",
            subject=self.subject,
            body_file="mail_body.html",
            sender_email=self.sender_email,
            sender_password=self.sender_password
        )

        self.assertTrue(mock_sendmail.called, "sendmail was not called")

        # Verify that emails were sent to all email addresses
        expected_emails = ["john@example.com", "jane@example.com", "mark@example.com", "amy@example.com"]
        sent_emails = [args[0][1] for args in mock_sendmail.call_args_list]

        self.assertCountEqual(sent_emails, expected_emails, "Should send emails to all departments")

    @patch("builtins.open", new_callable=lambda: multi_mock_open(*TestSmartMailer.file_contents))
    @patch.object(smtplib.SMTP_SSL, 'sendmail')
    def test_email_body_with_placeholders(self, mock_sendmail, mock_open):
        # Run the smart mailer function for "HR" department
        smart_mailer(
            input_file="maildata.csv",
            department_code="HR",
            subject=self.subject,
            body_file="mail_body.html",
            sender_email=self.sender_email,
            sender_password=self.sender_password
        )

        # Check if placeholder was replaced correctly in the body
        sent_email_content = mock_sendmail.call_args[0][2]
        self.assertIn("Hello Jane Smith", sent_email_content)
        self.assertIn("Welcome to the HR department update!", sent_email_content)

    # please run server.py on localhost before running this test case
    @patch("builtins.open", new_callable=lambda: multi_mock_open(*TestSmartMailer.file_contents))
    @patch.object(smtplib.SMTP_SSL, 'sendmail')
    @patch.dict('smart_mailer.__dict__', {"IMG_HOST": "http://localhost:5000/tracker.png"})
    def test_tracking_pixel_in_body(self, mock_sendmail, mock_open):
        # Run the smart mailer function with all departments
        smart_mailer(
            input_file="maildata.csv",
            department_code="all",
            subject=self.subject,
            body_file="mail_body.html",
            sender_email=self.sender_email,
            sender_password=self.sender_password
        )

        # Check if the tracking pixel URL is present in each sent email
        for call in mock_sendmail.call_args_list:
            sent_email_content = call[0][2]
            self.assertIn('<img src="http://localhost:5000/tracker.png"', sent_email_content)

    @patch("builtins.open", new_callable=lambda: multi_mock_open(*TestSmartMailer.file_contents))
    @patch.object(smtplib.SMTP_SSL, 'sendmail')
    def test_delay_between_emails(self, mock_sendmail, mock_open):
        # Patch time.sleep to measure call frequency
        with patch("time.sleep", return_value=None) as mock_sleep:
            smart_mailer(
                input_file="maildata.csv",
                department_code="all",
                subject=self.subject,
                body_file="mail_body.html",
                sender_email=self.sender_email,
                sender_password=self.sender_password
            )

            # Verify that sleep was called (indicating delay between emails)
            self.assertTrue(mock_sleep.call_count > 1, "Should have delay between emails")

    @patch("builtins.open", new_callable=lambda: multi_mock_open(*TestSmartMailer.file_contents))
    @patch.object(smtplib.SMTP_SSL, 'sendmail')
    def test_report_prints_email_count_by_department(self, mock_smtp, mock_open):
        # Capture printed output
        with patch("builtins.print") as mock_print:
            smart_mailer(
                input_file="maildata.csv",
                department_code="all",
                subject=self.subject,
                body_file="mail_body.html",
                sender_email=self.sender_email,
                sender_password=self.sender_password
            )

            # Verify report output
            report_lines = [call[0][0] for call in mock_print.call_args_list if "emails sent" in call[0][0]]
            self.assertIn("IT: 2 emails sent.", report_lines)
            self.assertIn("HR: 1 emails sent.", report_lines)
            self.assertIn("Finance: 1 emails sent.", report_lines)

if __name__ == "__main__":
    unittest.main()

