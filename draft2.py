import smtplib
import os

from dotenv import load_dotenv
from email.message import EmailMessage
from email.headerregistry import Address

load_dotenv()

def NotifyByMail(subject, text):
    from_addr = os.getenv('EMAIL_FROM')
    to_addr = os.getenv('EMAIL_TO')
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = Address('Ngoc Marcińczyk', addr_spec=from_addr)
    msg['To'] = to_addr
    msg['X-Mailer'] = 'Ngoc notifier'  # this reduces a chance to arrive into SPAM
    msg.set_content(text)
    print(f"Sending e-mail: '{subject}' from {from_addr} to {to_addr}")
    with smtplib.SMTP(os.getenv('SMTP_HOST'), 587) as s:
        s.ehlo()       # Identify ourselves to the SMTP server and enable extended SMTP features
        s.starttls()   # Upgrade the connection to secure TLS
        s.login(from_addr, os.getenv('EMAIL_PASS'))
        resp = s.send_message(msg)
        print(resp)
        s.quit()


def main():
    NotifyByMail("Hello Ngọc", """This will be your new e-mail address to send notifications using Python!

Ask your husband for credentials and a safe way to handle them in the code.

Best regards,
Your new e-mail address
""")


if __name__ == '__main__':
    main()