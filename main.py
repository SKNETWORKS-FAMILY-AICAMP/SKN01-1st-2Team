from dataset import load_dataset
from db import MySQLExecutor


def data_to_db(database: str, table_name: str, if_exists: str = "replace") -> None:
    mysql = MySQLExecutor(database)
    dataset = load_dataset()
    mysql.df2sql(dataset, table_name, if_exists)


if __name__ == "__main__":
    data_to_db(database="encar", table_name="info")
