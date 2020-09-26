from bs4 import BeautifulSoup
import requests
import csv

#url = 'https://shopee.tw/search?keyword=PS4%20pro%20%E4%B8%BB%E6%A9%9F'
url = 'https://shopee.com.my/search?keyword=kid%20s%20toy%20car&trackingId=searchhint-1600909805-ae1705a4-fe02-11ea-ad6e-f063f958f9ed'
headers = {
    'User-Agent': 'Googlebot',
    'From': 'YOUR EMAIL ADDRESS'
}

r = requests.get(url,headers=headers,allow_redirects=True)
print(r.status_code)
print(r.history)
print(r.url)

soup = BeautifulSoup(r.text, 'html.parser')
items = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")
print(len(items))

contents = soup.find_all("div", class_="_1NoI8_ _16BAGk")
prices = soup.find_all("span", class_="_341bF0")
sold = soup.find_all("div", class_="_18SLBt")
region = soup.find_all("div", class_="_3amru2")
#all_items = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")
#links = [i.find('a').get('href') for i in all_items]

print(contents)
print(prices)
print(sold)
print(region)

with open('shopee.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(['Product Name', 'Price (RM)', 'Sold Units', 'Seller Region'])

    for c, p, s, r in zip(contents, prices, sold, region):
        con = c.contents[0]
        pri = p.contents[0]
        try:
            sol = s.contents[0].strip(' sold')
        except IndexError:
            sol = 'Nan'
        reg = r.contents[0]

        #writer.writerow([con.encode('utf-8'), pri.encode('utf-8'), sol.encode('utf-8'), reg.encode('utf-8')])
        try:
            writer.writerow([con, pri, sol, reg])
        except UnicodeEncodeError:
            writer.writerow([con.encode('utf-8'), pri, sol, reg])

file.close()
