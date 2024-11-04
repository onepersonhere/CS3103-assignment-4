# [Option 1] Smart Mailer Program

## Description
- The smart mailer program sends mails to a list of emails provided in a csv file using any
SMTP services of your choice **(eg. smtp.gmail.com)**. 
- The mailer should introduce some **delay between emails** to reduce spam mails. 
- Your mailer should establish an **SMTP connection** and **exchange SMTP messages** to send mail. 
- You can use any programming language to implement the smart mailer (c, c++, java, python and use any high-level API
(such as openssl API) to establish connection with the SMTP server.

## Requirements
1. The mailer should accept an **input file (maildata.csv)** with list of email ids, names,
department codes
2. The mailer should accept a **department code** and send mails only to those departments
that are in the list. 
   - If the department code is “all” then the mails should be **send to all
   email ids in the list.**
3. The mailer should accept **subject and body information** (body in HTML format) from a
text file. 
   - The body should have **placeholders** which are marked with special characters
   (such as, #name#, #department#). 
   - The **placeholders** should be replaced by **actual names** and **department names** before sending the mail.
4. The mailer sends URL of a **transparent 1x1 pixel image** (usually a .png or .gif file) in the
HTML email body. 
   - This single image should be **hosted** in a publicly accessible **HTTP/HTTPS server** of your choice. 
   - Provide some method for the user who is sending email to **view a counter value** in this server which increments each time the image is
   accessed. 
   - [Note: In this way the user can track number of recipients opened the mail].
5. The program print a report showing number of emails sent grouped by department
code.
6. UI can be GUI or CUI.
7. Your codes should be well written and well commented.