import requests
from bs4 import BeautifulSoup
import re
from typing import List


class UrlImage():

    def __init__(self, search: str, value: int = 30, iw: int = None,
                 ih: int = None):
        self.__search = search
        self.__value = value
        self.__iw = iw
        self.__ih = ih
        self.__url = []

    def parse(self) -> List[str]:
        j = 0
        i = 0
        status = True
        self.__image_link = []
        self.__image_link2 = []
        self.__links = []

        while status:
            url = f'https://yandex.ru/images/search?from=tabbar&\
text={self.__search}&p={i}&isize=eq&iw={self.__iw}&ih={self.__ih}'

            responce = requests.get(url).text
            soup = BeautifulSoup(responce, 'lxml')
            block = soup.find("div", class_='serp-controller__content')
            self.__all_image = block.find_all(
                "div", class_='serp-item__preview')

            for image in self.__all_image:
                if j < self.__value:
                    self.__image_link.append(image.find('a').get('href'))
                    self.__image_link2.append(image.find(
                        'img', class_='serp-item__thumb justifier__thumb').get(
                            'src'))
                    j += 1
                else:
                    status = False
                    break
            i += 1

        for i in self.__check():
            self.__links.append(i.replace('//avatars', 'https://avatars'))

        return self.__links

    def __check(self):
        image_link = self.__image_link
        image_link2 = self.__image_link2
        for i in range(len(image_link)):
            url_image = re.split('img_url=|&from', image_link[i])

            normal_link = url_image[1].replace('%3A', ':')\
                .replace(r'%2F', '/').replace('%25', '%')\
                .replace('%28', '(').replace('%29', ')')

            is_image = requests.get(normal_link).status_code

            if is_image == 200:
                self.__url.append(normal_link)

            else:
                self.__url.append(image_link2[i])

        return self.__url
