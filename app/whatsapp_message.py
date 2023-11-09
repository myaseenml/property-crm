import pywhatkit
import datetime

# Get the current date and time
now = datetime.datetime.now()

# Extract the hour and minute
current_hour = now.hour
current_minute = now.minute

phone_no = "+923029770128"


def send_whatsapp(phone_no, message, current_hour, current_minute):
    pywhatkit.sendwhatmsg(phone_no, message, current_hour, current_minute + 1, 15, True, 6)

