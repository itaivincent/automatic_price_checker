import requests
from bs4 import BeautifulSoup
import unicodedata
from pprint import pprint

from send_email import sendmails

HEADERS = ({'User-Agent':
            'Mozilla/82.0 (Windows NT 6.1)  Chrome/90.0.4430.212',
            'Accept-Language': 'en-US, en;q=0.5'})


def get_product_info(url):
    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.content, features="lxml")

    try:
        title = soup.find(id='productTitle').get_text().strip()
        price_str = soup.find(id='priceblock_ourprice').get_text()
    except:
        return None, None, None
    try:
        soup.select('#availability .a-color-success')[0].get_text().strip()
        available = True
    except:
        available = False

    try:
        price = unicodedata.normalize("NFKD", price_str)
        price = price.replace(',', '.').replace('$', '')
        price = float(price)
    except:
        return None, None, None

    return title, price, available


if __name__ == '__main__':
    url = "https://www.amazon.com/Sony-Noise-Cancelling-Headphones-WH1000XM3/dp/B07G4MNFS1/ref=sxin_10_trr_12097479011_0?crid=36LWN2KO1B868&cv_ct_cx=sony+headphones&dchild=1&keywords=sony+headphones&pd_rd_i=B07G4MNFS1&pd_rd_r=072e0225-2fc3-474d-a7b1-63388759c175&pd_rd_w=IhCkE&pd_rd_wg=7Ja7z&pf_rd_p=9e83fe05-f489-4685-b4af-0db60cbe7c15&pf_rd_r=DZ5PXRZ492TRKNJBCZ8G&qid=1622410639&sprefix=sony+head%2Caps%2C457&sr=1-1-5519553e-2baa-451e-af83-b0156e5c6669"
    products = [(url, 350)]

    products_below_limit = []
    for product_url, limit in products:
        title, price, available = get_product_info(product_url)
        if title is not None and price < limit and available:
            products_below_limit.append((url, title, price))


    if products_below_limit:
        message = "Subject: Price below limit!\n\n"
        message += "Your tracked products are given below!\n\n"

        for url, title, price in products_below_limit:
            # message += f"{title}\n"
            message += f"Price: {price}\n"
            message += f"{url}\n\n"

            message += "Your tracked products are given below!\n\n"



        sendmails(message)
