import requests
from bs4 import BeautifulSoup

URL = 'https://shopee.com.my/50pcs-Disposable-Three-Layer-Mask-With-Melting-Spray-Cloth-i.241269224.6125176796'

headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
page = requests.get(URL, headers)

print(page.text)

s = BeautifulSoup(page.content, features="lxml")

product_title = s.select("#productTitle")[0].get_text()

product_price = s.select("#priceblock_ourprice")[0].get_text()

print(product_title, product_price)
