from dataset import load_dataset
from db import MySQLExecutor
from faq.runner import main

def data_to_db(database: str, table_name: str, if_exists: str = "replace") -> None:
    
    mysql = MySQLExecutor(database)
    dataset = load_dataset()
    mysql.df2sql(dataset, table_name, if_exists)

def faq_to_db(database: str, table_name: str, if_exists: str = "replace") -> None:
    df=main()
    mysql = MySQLExecutor(database)
    
    mysql.df2sql(df, table_name, if_exists)


import pandas as pd

if __name__ == "__main__":
    # data_to_db(database="encar", table_name="info")
    faq_to_db(database="encar", table_name="faq")
