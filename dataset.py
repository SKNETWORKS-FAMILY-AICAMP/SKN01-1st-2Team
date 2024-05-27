import pandas as pd

from crawler import Crawler


class Dataset:
    """
    A class representing a dataset.

    Attributes:
        crawler (Crawler): An instance of the Crawler class.
        _dataset (pandas.DataFrame): The concatenated dataset.

    Methods:
        __init__(): Initializes the Dataset object.
        get_data(): Retrieves data using the crawler.
        dataset(): Returns the concatenated dataset.

    """

    def __init__(self, sleep: int = 10):
        self.crawler = Crawler(sleep)
        self.get_data()
        self._dataset = pd.concat([*self.crawler.dataset])
        self._dataset.index = range(len(self._dataset.index))

    def get_data(self):
        """
        Retrieves data using the crawler.

        This method iterates over a range of values and calls the `get` method of the crawler.

        """
        for i in range(1, 3):
            self.crawler.get(i)

    @property
    def dataset(self):
        """
        Returns the concatenated dataset.

        Returns:
            pandas.DataFrame: The concatenated dataset.

        """
        return self._dataset


def load_dataset(sleep: int = 10) -> pd.DataFrame:
    return Dataset(sleep).dataset
