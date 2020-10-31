import tamashii
import goodsmile
import kotobukiya
import csv
import time

ts = time.time()
filename = "data%s.csv" % int(ts)

with open(str(filename), 'w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(['SKU', 'Title', 'Image', 'Manufacturer (Brand)', 'Released Date', 'Price', 'Specifications',
                     'Descriptions', 'URL'])

    data1 = kotobukiya.scrape("http://en.kotobukiya.co.jp/product/")
    data2 = goodsmile.scrape("https://www.goodsmile.info/en/products/released/2021")
    data3 = tamashii.scrape("https://tamashii.jp/item_announced/202010/")

    for info1 in enumerate(data1):
        writer.writerow(info1[1])

    for info2 in enumerate(data2):
        writer.writerow(info2[1])

    for info3 in enumerate(data3):
        writer.writerow(info3[1])

file.close()