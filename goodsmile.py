from bs4 import BeautifulSoup
import requests
import csv

#url = "https://www.goodsmile.info/en/products/released/2021"

def scrape(url):
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

    links =[]
    details =[]

    with open('goodsmile.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(['SKU', 'Title', 'Image', 'Manufacturer (Brand)', 'Released Date', 'Price', 'Specifications',
                         'Descriptions', 'link'])


        for link in soup.find_all('div', class_="hitBox"):
            a = link.find('a')
            links.append(a['href'])

        print(links) # all url in the page
        print("################################################################")
        des_ = []
        for url_ in links: #url_ in the
            #special case
            if url_ == "https://www.goodsmile.info/en/product/10091/figma+Tanjiro+Kamado+DX+Edition.html":
                continue
            elif url_ == "https://www.goodsmile.info/en/product/6053/Nendoroid+Pouch+Sleeping+Bag+Yamambagiri+Kunihiro+Ver.html":
                continue
            elif url_ == "https://www.goodsmile.info/en/product/10070/Nendoroid+Pouch+Sleeping+Bag+Yamanbagiri+Chougi+Ver.html":
                continue
            elif url_ == "https://www.goodsmile.info/en/product/10044/Cyclion+Type+Lavender.html":
                continue

            print(url_)
            r_ = requests.get(url_, headers=headers, allow_redirects=True)
            soup = BeautifulSoup(r_.text, 'html.parser')

            img = soup.find('a', class_="imagebox")
            image = 'https://'+img['href'] #image url

            sku = "goodsmile"+url_[37:43].strip(" / ") #sku = site+ product id

            des = soup.find("div", class_="description")
            detail = soup.find('div', class_='detailBox') # items info

            for dd in detail.find_all('dd'): # each info in dd
                details.append(dd.get_text()) # store all dd

            if len(details) == 6:
                title = details[0]
                manu = details[1]
                price = details[3]
                date = details[4]
                specs = details[5]
            else:
                title = details[0]
                manu = details[2]
                price = details[4]
                date = details[5]
                specs = details[6]

            des = des.get_text()

            try:
               writer.writerow([sku, title, image, manu, date, price, specs, des, url_])
               data = [sku, title, image, manu, date, price, specs, des, url_]
            except UnicodeEncodeError:
                data = [sku, title.encode('utf-8'), image, manu.encode('utf-8'), date, price.encode('utf-8'),
                                specs, des.encode('utf-8'), url_]
                writer.writerow([sku, title.encode('utf-8'), image, manu.encode('utf-8'), date, price.encode('utf-8'),
                                specs, des.encode('utf-8'), url_])

            data_all.append(data)

            print("================================================================================")
            details.clear()

    return data_all

if __name__ == "__main__":
    with open('goodsnile__.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(['SKU', 'Title', 'Image', 'Manufacturer (Brand)', 'Released Date', 'Price', 'Specifications',
                         'Descriptions', 'URL'])

        data_all = scrape("https://www.goodsmile.info/en/products/released/2021")

        for info in enumerate(data_all):
            writer.writerow(info[1])

    file.close()

