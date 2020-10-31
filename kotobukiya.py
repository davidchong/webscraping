from bs4 import BeautifulSoup
import requests
import csv
import re

def scrape(url):

    #url = "http://en.kotobukiya.co.jp/product/"
    url = url
    data_all = []

    headers = {
        'User-Agent': 'Googlebot',
        'From': 'chongteakwei@gmail.com'
    }

    r = requests.get(url,headers=headers,allow_redirects=True)

    print(r.status_code)
    print(r.history)
    #print(r.url)

    soup = BeautifulSoup(r.text, 'html.parser')

    links = []
    titles = []
    contents = []

    with open('kotobukiya.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(['SKU', 'Title', 'Image', 'Manufacturer (Brand)', 'Released Date', 'Price', 'Specifications',
                         'Descriptions', 'URL'])

        for link in soup.find_all('div', class_="items clearfix"):
            a = link.find_all('a')
            for a_ in a:
                links.append(a_['href'])
                titles.append(a_['title'])
                print(a_['href'])
                print(a_['title'])

        #descriptions = soup.find_all("div", class_="hitBox")
        print("################################################################")
        des_ = []
        for url_ in enumerate(links):

            print(url_[1])
            print(titles[url_[0]])

            r_ = requests.get(url_[1], headers=headers, allow_redirects=True)
            soup = BeautifulSoup(r_.text, 'html.parser')

            sku = "koyobukiya" + url_[1][43:53]
            title = titles[url_[0]]
            print(sku)

            images = soup.find('img', {'src': re.compile('.jpg')})
            image = images['src']


            content = soup.find('div', class_='product-data shadow')
            for dd in content.find_all('dd'):
                contents.append(dd.get_text())
            #except:
            #    content = soup.find_all('div', class_='detail')
            #    for con in content:
            #        details.append(con.get_text())
            print(contents)

            if len(contents) == 6:
                manu = contents[5]
            else:
                manu = contents[6]

            date = contents[0]
            specs = contents[3]
            price = '--'
            url_ = url_[1]

            des = soup.find('p').get_text()

            try:
                writer.writerow([sku, title, image, manu, date, price,
                             specs, des, url_])
                data = [sku, title, image, manu, date, price, specs, des, url_]
            except UnicodeEncodeError:
                writer.writerow([sku, title.encode('utf-8'), image, manu.encode('utf-8'), date, price,
                             specs.encode('utf-8'), des.encode('utf-8'), url_.encode('utf-8')])
                data = [sku, title.encode('utf-8'), image, manu.encode('utf-8'), date, price,
                             specs.encode('utf-8'), des.encode('utf-8'), url_.encode('utf-8')]

            data_all.append(data)

            print("================================================================================")
            contents.clear()

    return data_all

if __name__ == "__main__":
    with open('kotobukiya__.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(['SKU', 'Title', 'Image', 'Manufacturer (Brand)', 'Released Date', 'Price', 'Specifications',
                         'Descriptions', 'URL'])

        data_all = scrape("http://en.kotobukiya.co.jp/product/")

        for info in enumerate(data_all):
            writer.writerow(info[1])

    file.close()
