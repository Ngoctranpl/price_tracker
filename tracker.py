import requests
from bs4 import BeautifulSoup
import json
from datetime import date
import csv
import sys


URL = "https://www.mohito.com/pl/pl/sukienka-maxi-z-wiskozy-2-668fv-08p"
TARGET_PRICE = 249.99


def main():
    price, currency = get_price()
    today = date.today().strftime("%d/%m/%y")
    print(f"Price on {today} is {price} {currency}")
    save(today, price, currency)
    if price < TARGET_PRICE:
        sent_alert(price)


# to extract price from given website
def get_price():
    try:
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, features="html.parser")
        script_tag = soup.find(type="application/ld+json")
        content = json.loads(script_tag.string)
        price = float(content["offers"]["price"])

        if price:
            currency = content["offers"]["priceCurrency"]

            return price, currency

    except Exception as e:
        sys.exit(f"An error occured: {e}")


# to log the price in a CSV file
def save(x, y, z):
    with open("price_report.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([x, y, z])
        print("Price is logged into price_report.csv file")


if __name__ == "__main__":
    main()
