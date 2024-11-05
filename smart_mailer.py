import smtplib
import csv
import time
import ssl
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import argparse

# SMTP setup (e.g., Gmail)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
IMG_HOST="https://cs3103-assignment-4.onrender.com/tracker.png"

def read_csv(file_path):
    recipients = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            recipients.append(row)
    return recipients


def replace_placeholders(body, name, department):
    body = re.sub(r"#name#", name, body)
    body = re.sub(r"#department#", department, body)
    tracker_img = f'<img src="{IMG_HOST}" style="display:none;" />'
    body += tracker_img
    return body


def send_email(smtp_server, sender_email, recipient_email, subject, body):
    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    # Attach HTML part
    html_body = MIMEText(body, "html")
    message.attach(html_body)

    smtp_server.sendmail(sender_email, recipient_email, message.as_string())


def smart_mailer(input_file, department_code, subject, body_file, sender_email, sender_password):
    # Read email data from CSV
    recipients = read_csv(input_file)

    # Read email body
    with open(body_file, "r") as f:
        body_template = f.read()

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Connect to SMTP server
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(sender_email, sender_password)

        count_by_department = {}

        for recipient in recipients:
            if department_code != "all" and recipient["department_code"] != department_code:
                continue

            # Customize the body for each recipient
            body = replace_placeholders(body_template, recipient["name"], recipient["department_code"])

            try:
                send_email(server, sender_email, recipient["email"], subject, body)
                print(f"Email sent to {recipient['email']}")

                # Update department count
                dept = recipient["department_code"]
                count_by_department[dept] = count_by_department.get(dept, 0) + 1

                # Add delay between emails
                time.sleep(2)  # Delay of 2 seconds to avoid spam detection
            except Exception as e:
                print(f"Failed to send email to {recipient['email']}: {e}")

    # Print the report
    print("\nEmails sent summary:")
    for dept, count in count_by_department.items():
        print(f"{dept}: {count} emails sent.")


if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description="Smart Mailer Program")
    parser.add_argument("--csv", required=True, help="Path to input CSV file")
    parser.add_argument("--department", required=True, help="Department code to filter (or 'all')")
    parser.add_argument("--subject", required=True, help="Subject of the email")
    parser.add_argument("--body", required=True, help="Path to email body HTML file")
    parser.add_argument("--sender_email", required=True, help="Sender's email")
    parser.add_argument("--sender_password", required=True, help="Sender's email password")

    args = parser.parse_args()

    # Run the mailer
    smart_mailer(args.csv, args.department, args.subject, args.body, args.sender_email, args.sender_password)
