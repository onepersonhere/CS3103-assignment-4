import csv
import smtplib

def send_email():
    with open('maildata.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        with open('body.txt', 'r') as f:
            body = f.read()

        for row in reader:
            recipient_email = row['email']
            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp.login("wertkwh@gmail.com", "vjctutvxuqrwtarr")
            smtp.sendmail('from@example.com', recipient_email, body)
            smtp.quit()