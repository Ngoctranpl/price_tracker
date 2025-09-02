# Import smtplib for the actual sending function
import smtplib
import os

# Import the email modules we'll need
from email.message import EmailMessage
from dotenv import load_dotenv
from email.headerregistry import Address


load_dotenv()


# Create the email message
msg = EmailMessage()
msg.set_content("""The price has dropped! 

Check the product here.

Good luck!
""")


from_addr = os.getenv('EMAIL_FROM')
to_addr = os.getenv('EMAIL_TO')


msg['Subject'] = f'The price has drop'
msg['From'] = Address('Ngoc Marcińczyk', addr_spec=from_addr)
msg['To'] = to_addr


try:
    with smtplib.SMTP(os.getenv('SMTP_HOST'), 587) as server:
        server.ehlo()       # Identify ourselves to the SMTP server and enable extended SMTP features
        server.starttls()   # Upgrade the connection to secure TLS
        server.login(from_addr, os.getenv("EMAIL_PASS"))
        server.send_message(msg)
    print("Email sent successfully.")
except Exception as e:
    print(f"Failed to send email: {e}")
