from bs4 import BeautifulSoup
from django.shortcuts import render


# def parsing_news(request):
#     # parsing
#     from lxml import html
#     import requests
#     url = 'https://www.dexigner.com/design-events'
#     response = requests.get(url)
#     if response.status_code == 200:
#         tree = html.fromstring(response.content)
#         news = tree.xpath('//*[@id="agenda"]/li[*]/article/div/h3/a/text()')
#         news_ = []
#         for new in news:
#             new = new.replace('\n', '').strip()
#             if new:
#                 news_.append(new)
#         news_data = {'news': news_}
#     else:
#         news_data = {'news': 'there is no news'}
#     # end parcing
#     return news_data

import requests


def get_html(url):
    response = requests.get(url)
    return response.text


def get_dates(html):
    soup = BeautifulSoup(html, 'lxml')
    get_data_div = soup.find('div', class_='standard-body')
    return get_data_div


def get_every_date(html):
    donation_places = html.find_all('h2', class_='body-h2')
    list_auto = []

    for place in donation_places:
        try:
            link = place.find('a', class_='body-link').get("href")

        except:
            link = ""
        try:
            title = place.find('a', class_='body-link').text
        except:
            title = ''

        data = {'title': title.replace('\n', '').strip(),
                'link': link}
        list_auto.append(data)

    return list_auto


def pars():
    akg_url = 'https://www.goodhousekeeping.com/life/a34301625/where-to-donate-clothes/'
    html = get_html(akg_url)
    html = get_dates(html)
    list_ = get_every_date(html)
    return list_