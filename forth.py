from bs4 import BeautifulSoup
import requests
import csv
import pathlib

print("Please type the item you want:")
keyword = input().replace(' ','%20')
url = 'https://shopee.com.my/search?keyword={}'.format(keyword)

print("You are directing to " + url)

headers = {
    'User-Agent': 'Googlebot',
    'From': 'chongteakwei@gmail.com'
}

r = requests.get(url,headers=headers,allow_redirects=True)
'''
print(r.status_code)
print(r.history)
print(r.url)
'''
soup = BeautifulSoup(r.text, 'html.parser')
#items = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")
'''
print(len(items))
'''
contents = soup.find_all("div", class_="_1NoI8_ _16BAGk")
prices = soup.find_all("span", class_="_341bF0")
sold = soup.find_all("div", class_="_18SLBt")
region = soup.find_all("div", class_="_3amru2")
all_items = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")
links = [i.find('a').get('href') for i in all_items]
'''
print(contents)
print(prices)
print(sold)
print(region)
print(links)
'''
#print(links)
#exit()
print("loading...")

with open('shopee.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(['Product Name', 'Price (RM)', 'Sold Units', 'Seller Region', 'Links'])


    for c, p, s, r, l in zip(contents, prices, sold, region, links):
        con = c.contents[0]
        pri = p.contents[0]
        lin = 'https://shopee.tw/'+str(l)
        try:
            sol = s.contents[0].strip(' sold')

            if sol.islower() == True:
                sol = sol.strip("k")
                sol = float(sol)*1000
        except IndexError:
            sol = 'NaN'
        try:
            reg = r.contents[0]
        except IndexError:
            reg = 'Null'

        #writer.writerow([con.encode('utf-8'), pri.encode('utf-8'), sol.encode('utf-8'), reg.encode('utf-8')])
        try:
            writer.writerow([con, pri, sol, reg, lin])
        except UnicodeEncodeError:
            writer.writerow([con.encode('utf-8'), pri, sol, reg, lin.encode('utf-8')])

    print("CSV file is created with data which save at " + str(pathlib.Path().absolute()) + "\shopee.csv")

file.close()
