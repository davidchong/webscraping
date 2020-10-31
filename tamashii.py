from bs4 import BeautifulSoup
import requests
import csv
import re

def scrape(url):

    #url = "https://tamashii.jp/item_announced"
    #url = "https://tamashii.jp/item_announced/202010/"
    url = url
    data_all = []

    headers = {
        'User-Agent': 'Googlebot',
        'From': 'chongteakwei@gmail.com'
    }

    r = requests.get(url,headers=headers, allow_redirects=True)

    print(r.status_code) #200 means never been redirected,access granted
    print(r.history)
    print(r.url)

    soup = BeautifulSoup(r.text, 'html.parser')
    brands = soup.find_all("span", class_="brand")
    items = soup.find_all("span", class_="item_name")
    prices = soup.find_all("p", class_="price")
    dates = soup.find_all("p", class_="date")
    images = soup.find_all('img', {'src':re.compile('.jpg')})
    links =[]

    for ul in soup.find_all('ul', class_='product_search_list'):
         for li in ul.find_all('li'):
            a = li.find('a')
            links.append(a['href'])

    #print("loading...")

    with open('tamashii.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(['SKU','Title', 'Image','Manufacturer (Brand)', 'Released Date', 'Price', 'Specifications',
                         'Descriptions'])

        url2 = "https://tamashii.jp"

        for b, i, p, img, d, link in zip(brands, items, prices, images, dates, links):
            title = i.contents[0]
            price = p.contents[0]
            date = d.contents[0]
            url_ = url2+link[:]
            sku = url2[8:16]+link[6:11]
            image = url2+img['src']
            manu = b.contents[0]

            r_ = requests.get(url_, headers=headers, allow_redirects=True) #go to second later
            soup_ = BeautifulSoup(r_.text, 'html.parser')

            print(url_)

            infos = soup_.find_all('div', id='item_detail')
            for info in infos:
                try:
                    specs = info.find('p').get_text()
                except:
                    specs = 'No specifications provided.' # no specifications provided

            dess = soup_.find_all('div', class_='upper_detail')
            for text in dess:
                des = text.find('p').get_text()

            try:
                print(des)
            except:
                des = "No descriptions provided."

            try:
                writer.writerow([sku, title, image, manu, date, price, specs, des, url_])
                data = [sku, title, image, manu, date, price, specs, des, url_]
            except UnicodeEncodeError:
                writer.writerow([sku, title.encode('utf-8'), image, manu.encode('utf-8'), date.encode('utf-8'), price.encode('utf-8'), specs.encode('utf-8'), des.encode('utf-8'), url_])
                data = [sku, title.encode('utf-8'), image, manu.encode('utf-8'), date.encode('utf-8'), price.encode('utf-8'), specs.encode('utf-8'), des.encode('utf-8'), url_]

            data_all.append(data)

    return data_all

if __name__ == "__main__":
    with open('tamashii__.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(['SKU', 'Title', 'Image', 'Manufacturer (Brand)', 'Released Date', 'Price', 'Specifications',
                         'Descriptions', 'URL'])

        data_all = scrape("https://tamashii.jp/item_announced/202010/")

        for info in enumerate(data_all):
            writer.writerow(info[1])

    file.close()
