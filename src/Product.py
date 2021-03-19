import json
import requests
from bs4 import BeautifulSoup
from utils import *


class Product:
    DATA_PATH = "./data/products.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}

    def __init__(self, url='', target_price=None, price=None, title=''):
        self.url = url
        self.target_price = target_price
        self.price = price
        self.title = title

    def json_to_products(products):
        with open(Product.DATA_PATH) as f:
            products_json = json.load(f)

        for product_json in products_json:
            if 'URL' in product_json and 'target_price' in product_json:
                product = Product()
                product.url = product_json['URL']
                product.target_price = product_json['target_price']
                products.append(product)

    def update_products(products):
        title_html = price_html = page = None
        for product in products:
            while not title_html or not price_html:
                page = requests.get(
                    product.url, headers=Product.headers)
                soup = BeautifulSoup(page.content, "html.parser")
                title_html = soup.find(id="productTitle")
                price_html = soup.find(id="priceblock_ourprice")
            title = title_html.get_text().strip()
            price_str = price_html.get_text().strip()
            price = float_from_currency_str(price_str, '.')
            product.title = title
            product.price = price

            if page:
                page.close()

            title_html = price_html = page = None

    @staticmethod
    def get_products(products):
        Product.json_to_products(products)
        Product.update_products(products)

    @staticmethod
    def check_product_prices(products_to_buy, products):
        for product in products:
            if product.price < product.target_price:
                products_to_buy.append(product)

    @staticmethod
    def get_product_urls(product_urls, products):
        for product in products:
            product_urls.append(product.url)
