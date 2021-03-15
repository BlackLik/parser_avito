import requests
import const
from bs4 import BeautifulSoup
import csv


def get_html(url, params=None):
    r = requests.get(url=url, params=params, headers=const.HEADERS)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='pagination-item-1WyVp')
    if pagination:
        return int(pagination[-2].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='iva-item-body-NPl6W')
    objects = []
    for item in items:
        if item.text != {}:
            price = ''.join(item.find('span', class_='price-text-1HrJ_').get_text().split('\xa0₽')[0].split(' '))
            if price == 'Ценанеуказана':
                price = 'Цена не указана'
            elif price == 'Бесплатно':
                price = 0
            else:
                price = int(price)
            objects.append({
                'title': item.find('h3', class_='title-root-395AQ').get_text(),
                'price': price,
                'link': const.HOST + item.find('a', class_='link-link-39EVK').get('href')
            })
        else:
            continue
    return objects


def save_data(items, path):
    with open(path, 'w', newline='') as file:
        writter = csv.writer(file, delimiter=';')
        writter.writerow(['Загаловок', 'Цена', 'Ссылка'])
        for item in items:
            writter.writerow([item['title'], item['price'], item['link']])


def main():
    html = get_html(const.URL)
    if html.status_code == 200:
        objects = []
        pages_count = get_pages_count(html.text)
        if pages_count >= 3:
            pages_count = 3
        for page in range(1, pages_count + 1):
            print('Сейчас страница {} из {}'.format(page, pages_count))
            html = get_html(const.URL, params={'p': page})
            objects.extend(get_content(html.text))
        save_data(objects, const.FILE)
        print("Оконченно")
        print("Всего объектов: ", len(objects))
    else:
        print('Error: html status not 200')


if __name__ == '__main__':
    main()
