import requests
import csv
import re
from bs4 import BeautifulSoup

rank_page = 'https://socialblade.com/youtube/top/50/mostviewed'
page = requests.get(rank_page, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'})
#page = urllib3.urlopen(request)

#soup = BeautifulSoup(page, 'html.parser')
soup = BeautifulSoup(page.content, 'html.parser')

channels = soup.find('div', attrs={'style': 'float: right; width: 900px;'}).find_all('div', recursive=False)[4:]

#file = open('topyoutubers.csv', 'wb')
with open('innovators.csv', 'w', newline='') as file:
    writer = csv.writer(file)

# write title row
    writer.writerow(["Username", "Uploads", "Views"])

    for channel in channels:
        username = channel.find('div', attrs={'style': 'float: left; width: 350px; line-height: 25px;'}).a.text.strip()
        uploads = channel.find('div', attrs={'style': 'float: left; width: 80px;'}).span.text.strip()
        views = channel.find_all('div', attrs={'style': 'float: left; width: 150px;'})[1].span.text.strip()

        print(username + ' ' + uploads + ' ' + views)
        #writer.writerow([username.encode('utf-8'), uploads.encode('utf-8'), views.encode('utf-8')])

        use = username.encode('utf-8')
        up = uploads.encode('utf-8')
        view = views.encode('utf-8')

        writer.writerow([str(use, encoding='utf-8'), str(up, encoding='utf-8'), str(view, encoding='utf-8')])
        #writer.writerow([username, uploads, views])

file.close()

