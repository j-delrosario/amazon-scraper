from Product import Product
from mail import *
import sys


def run(email):
    products = []
    products_to_buy = []

    Product.get_products(products)
    Product.check_product_prices(products_to_buy, products)

    if len(products_to_buy) > 0:
        product_urls = []
        Product.get_product_urls(product_urls, products_to_buy)

        send_mail(product_urls, email)

    print("No products have fallen in price")


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        run(arg)
