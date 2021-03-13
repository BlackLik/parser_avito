import requests
import const
from bs4 import BeautifulSoup


def get_html(url, params=None):
    r = requests.get(url=url, params=params, headers=const.HEADERS,)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='iva-item-body-NPl6W')
    objects = []
    for item in items:
        if item is not None:
        objects.append({
            'title': item.find('h3', class_='title-root-395AQ iva-item-title-1Rmmj title-list-1IIB_ title-root_maxHeight-3obWc text-text-1PdBw text-size-s-1PUdo text-bold-3R9dt').get_text(strip=True),
            'price': ''.join(item.find('span', class_='price-text-1HrJ_ text-text-1PdBw text-size-s-1PUdo').get_text().split('\xa0₽')[0].split(' ')),
            'link': const.HOST + item.find('a', class_='link-link-39EVK link-design-default-2sPEv title-root-395AQ iva-item-title-1Rmmj title-list-1IIB_ title-root_maxHeight-3obWc').get('href')
        })
    for object in objects:
        print(object)


def main():
    html = get_html(const.URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error: html status not 200')


if __name__ == '__main__':
    main()
