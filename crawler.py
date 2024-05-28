import datetime
from typing import Any, List
from urllib.parse import quote_plus

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


class Crawler:
    """
    A class that represents a web crawler for car data.
    """

    def __init__(self, sleep: int = 0):
        """
        Initializes the Crawler class.
        """
        self.sleep = sleep

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--incognito")
        self.driver = webdriver.Chrome()

        self._dataset = []

    def _get_url(self, page=None) -> str:
        """
        Generates the URL for car data based on the specified page number.

        Args:
            page (int): The page number. Defaults to None.

        Returns:
            str: The generated URL.
        """
        electrical = quote_plus("전기차")
        hybrid = quote_plus("하이브리드")
        p_hybrid = quote_plus("플러그인 하이브리드")
        lpg = quote_plus("LPG")
        page = page
        url = f"https://car.encar.com/list/car?page={page}&search=%7B%22type%22%3A%22ev%22%2C%22action%22%3A%22(And.Hidden.N._.CarType.A._.(C.GreenType.Y._.(Or.EvType.{electrical}._.EvType.{hybrid}._.EvType.{p_hybrid}._.EvType.{lpg}.))_.Separation.A.)%22%2C%22title%22%3A%22%22%2C%22toggle%22%3A%7B%7D%2C%22layer%22%3A%22%22%2C%22sort%22%3A%22MobileModifiedDate%22%7D"

        return url

    def _get_source(self, page: int):
        """
        Retrieves the HTML source code of the web page.

        Returns:
            str: The HTML source code.
        """
        self.driver.maximize_window()
        self.driver.get(self._get_url(page))
        self.driver.implicitly_wait(self.sleep)
        try:
            self.driver.implicitly_wait(5)
            close_banner = self.driver.find_element(
                By.XPATH, '//*[@id="modal"]/div[2]/div/div/button[2]'
            )
            close_banner.click()
        except:
            pass
        source = self.driver.page_source
        self.driver.implicitly_wait(1)
        return source

    def _process(self, soup: BeautifulSoup, tag: str, name_tag: str) -> List[Any]:
        """
        Processes the car data from the HTML soup.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object representing the HTML soup.
            tag (str): The class name of the car data container.
            name_tag (str): The class name of the car name element.

        Returns:
            List: The processed car data as a List.
        """

        def process_year(year):
            year = datetime.datetime.strptime(year, "%y/%m")
            return year

        car_list = soup.find_all("div", {"class", f"{tag}"})

        dataset = []
        for i in range(len(car_list)):
            name = (
                car_list[i]
                .find("strong", {"class": f"{name_tag}"})
                .text.strip()
                .replace("\n", " ")
            )
            info = [x.text.strip() for x in car_list[i].find_all("li")]
            year, km, f_type, city = info[:4]

            year = process_year(year.strip("식"))
            print("year", year)
            km = int(km.strip("km").replace(",", ""))

            data = [name, year, km, f_type, city]
            print(data)
            dataset.append(data)
        return dataset

    def process(self, soup) -> List[Any]:
        """
        Processes the car data from the HTML soup.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object representing the HTML soup.

        Returns:
            List: The processed car data as a List.
        """
        try:
            big = self._process(
                soup, "ItemBigImage_car__ovlrq", "ItemBigImage_name__h0biK"
            )
            small = self._process(
                soup, "ItemSmallImage_txt_area__79qyK", "ItemSmallImage_name__6Fim0"
            )
            big = pd.DataFrame(
                big, columns=["이름", "연식", "주행거리", "종류", "지역"]
            )
            small = pd.DataFrame(
                small, columns=["이름", "연식", "주행거리", "종류", "지역"]
            )
            dataset = pd.concat([big, small], axis=0)
            dataset = dataset.index = range(len(dataset.index))
        except:
            small = self._process(
                soup, "ItemSmallImage_txt_area__79qyK", "ItemSmallImage_name__6Fim0"
            )
            small = pd.DataFrame(
                small, columns=["이름", "연식", "주행거리", "종류", "지역"]
            )
            dataset = small

        return dataset

    def get(self, page: int = 1):
        """
        Retrieves the car data from the web page.

        Args:
            page (int): The page number. Defaults to 1.
        """

        source = self._get_source(page)
        soup = BeautifulSoup(source, "html.parser")
        dataset = self.process(soup)
        self._dataset.append(dataset)

    @property
    def dataset(self):
        """
        Returns the dataset containing the car data.

        Returns:
            dict: The dataset containing the car data.
        """
        return self._dataset
