import requests
from bs4 import BeautifulSoup
import json
from datetime import date
import csv
import sys
import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage
from email.headerregistry import Address
import logging


# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("tracker.log"),
        logging.StreamHandler()
    ]
)


URL = "https://www.mohito.com/pl/pl/sukienka-maxi-z-wiskozy-2-668fv-08p"
TARGET_PRICE = 249.99


def main():
    load_dotenv()
    if not os.getenv("EMAIL_FROM"):
        sys.exit("Please set EMAIL_FROM in .env file")
    if not os.getenv("EMAIL_TO"):
        sys.exit("Please set EMAIL_TO in .env file")
    if not os.getenv("EMAIL_PASS"):
        sys.exit("Please set EMAIL_PASS in .env file")
    if not os.getenv("SMTP_HOST"):
        sys.exit("Please set SMTP_HOST in .env file")    
    price, currency = get_price()
    today = date.today().strftime("%d/%m/%y")
    logging.info(f"Price on {today} is {price} {currency}")
    save(today, price, currency)
    if price < TARGET_PRICE:
        send_alert(price)


# to extract price from given website
def get_price(link=URL):
    try:
        r = requests.get(link)
        soup = BeautifulSoup(r.text, features="html.parser")
        script_tag = soup.find(type="application/ld+json")
        content = json.loads(script_tag.string)
        price = float(content["offers"]["price"])
        currency = content["offers"]["priceCurrency"]
        return price, currency

    except Exception as e:
        logging.Exception(f"Error during price extraction: {e}")
        sys.exit()


# to log the price in a CSV file
def save(date, price, currency):
    with open("price_report.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, price, currency])
        logging.info("Price is logged into price_report.csv file")


def send_alert(price):

    subject = "Price Alert!"
    text = f"The price has dropped to {price} PLN. Check the product here: {URL}"
    from_addr = os.getenv("EMAIL_FROM")
    to_addr = os.getenv("EMAIL_TO")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = Address("Ngoc Marcińczyk", addr_spec=from_addr)
    msg["To"] = to_addr
    msg["X-Mailer"] = "Ngoc notifier"  # this reduces a chance to arrive into SPAM
    msg.set_content(text)
    logging.info(f"Sending e-mail: '{subject}' from {from_addr} to {to_addr}")
    with smtplib.SMTP(os.getenv("SMTP_HOST"), 587) as s:
        s.ehlo()  # Identify ourselves to the SMTP server and enable extended SMTP features
        s.starttls()  # Upgrade the connection to secure TLS
        s.login(from_addr, os.getenv("EMAIL_PASS"))
        resp = s.send_message(msg)
        print(resp)
        s.quit()


if __name__ == "__main__":
    main()
