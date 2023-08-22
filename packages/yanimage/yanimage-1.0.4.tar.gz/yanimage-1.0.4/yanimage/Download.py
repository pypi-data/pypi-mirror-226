import requests
from typing import List


class Download():

    def __init__(self, links: List[str], path: str, verbose: bool = False):
        self.__links = links
        self.__path = path
        self.__verbose = verbose

    def download(self) -> None:
        for i, url in enumerate(self.__links):
            image_bytes = requests.get(url).content

            with open(f'{self.__path}/{i}.jpg', 'wb') as file:
                file.write(image_bytes)

            if self.__verbose:
                print(f'Saved {i + 1} of {len(self.__links)} pictures')
