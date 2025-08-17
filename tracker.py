import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import csv


URL = "https://www.mohito.com/pl/pl/sukienka-maxi-z-wiskozy-2-668fv-08p"


def main():
    price = get_price()
    print(price)
    # today = today()
    # print(f"Price on {today} is {price}")
    # save(price)


def get_price():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, features="html.parser")
    script_tag = soup.find(type="application/ld+json")
    content = json.loads(script_tag.string)
    price = float(content["offers"]["price"])
    currency = content["offers"]["priceCurrency"]

    return f"{price} {currency}"


def today(): ...


if __name__ == "__main__":
    main()
