import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import platform
import uuid
import hashlib

import pywhatkit


def send_whatsapp(fullName, phone_no):
    now = datetime.now()

    # Extract the hour and minute
    current_hour = now.hour
    current_minute = now.minute
    message = f'''
Dear {fullName}
You have assigned a Lead in Property Square CRM.
Please See that.
    '''
    pywhatkit.sendwhatmsg(phone_no, message, current_hour, current_minute + 1, 15, True, 6)


def get_unique_identifier():
    # Try to get the MAC address
    mac = None
    if platform.system() == "Linux":
        try:
            with open('/sys/class/net/eth0/address') as f:
                mac = f.read().strip()
        except:
            pass

    if not mac:
        mac = ':'.join(['{:02X}'.format((uuid.getnode() >> elements) & 0xFF) for elements in range(5, -1, -1)])

    # Combine the MAC address with other system information
    system_info = platform.system() + platform.machine() + platform.processor()

    # Create a unique identifier by hashing the combined information
    unique_identifier = hashlib.sha256((mac + system_info).encode()).hexdigest()

    return unique_identifier


user_identifier = get_unique_identifier()
print(f"User's unique identifier: {user_identifier}")


def send_email(subject, to_email, data):
    message = f"""
Subject: Welcome to {data[0]} CRM - Registration Confirmation

Dear {data[1]},

We are thrilled to welcome you to the {data[0]} CRM family! Thank you for choosing us as your partner for managing and nurturing your valuable customer relationships.

Your registration to our CRM platform is now complete, and your journey towards enhanced customer engagement and growth begins here. With {data[0]} CRM, you can streamline your operations, make data-driven decisions, and provide exceptional experiences to your customers.

Here are some key details to get you started:

Username: {data[2]}
Email Address: {data[3]}
Registration Date: {data[4]}

To access your CRM account, simply click on the following link and enter your login credentials:

{data[5]}

At {data[0]}, we are committed to providing the best CRM experience for our users. Should you have any questions, encounter any issues, or need assistance with any aspect of our CRM platform, our dedicated support team is here to help you.

Stay tuned for updates, tips, and best practices on how to make the most of your CRM system by subscribing to our newsletter. We will also periodically send you valuable insights and updates to keep you informed about new features and improvements.

We are excited to partner with you and look forward to being a part of your journey to success. Your trust in us is greatly appreciated, and we are committed to delivering the highest level of service and support.

Warm regards,

Faheem
Manager
Property Square
email@gmai.com
    """
    try:
        # Your Gmail account details
        sender_email = "yaseenuom6@gmail.com"
        app_password = "yhwikrfmrvhlkyjo"

        # Create a secure SSL connection to the Gmail SMTP server
        smtp_server = "smtp.gmail.com"
        smtp_port = 465
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)

        # Login to your Gmail account
        server.login(sender_email, app_password)

        # Create the email message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject

        # Attach the message to the email
        msg.attach(MIMEText(message, "plain"))

        # Send the email
        server.sendmail(sender_email, to_email, msg.as_string())

        # Close the SMTP server
        server.quit()

        print("Email sent successfully!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def send_email_manager(subject, to_email, data):
    message = f"""
Subject: New User Registration - {data[0]} has joined Property Square CRM

Dear Faheem,

We are delighted to inform you that a new user has registered on Property Square CRM, our platform for managing customer relationships. Here are the user details:

- Username: {data[1]}
- Email: {data[2]}
- Registration Date: {data[3]}

Best regards,

Property Square CRM Team
    """
    try:
        # Your Gmail account details
        sender_email = "yaseenuom6@gmail.com"
        app_password = "yhwikrfmrvhlkyjo"

        # Create a secure SSL connection to the Gmail SMTP server
        smtp_server = "smtp.gmail.com"
        smtp_port = 465
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)

        # Login to your Gmail account
        server.login(sender_email, app_password)

        # Create the email message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject

        # Attach the message to the email
        msg.attach(MIMEText(message, "plain"))

        # Send the email
        server.sendmail(sender_email, to_email, msg.as_string())

        # Close the SMTP server
        server.quit()

        print("Email sent successfully!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

