import getpass
from typing import Dict, Union

import pandas as pd
import pymysql
import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL


class MySQLExecutor:
    """
    A class that provides methods to interact with a MySQL database.

    Args:
        database (str): The name of the database.
        username (str, optional): The username for the database connection. Defaults to "root".
        passwd (str, optional): The password for the database connection. Defaults to an empty string.
        host (str, optional): The host address for the database connection. Defaults to "127.0.0.1".
        port (int, optional): The port number for the database connection. Defaults to 3306.

    Attributes:
        _engine (sqlalchemy.Engine): The SQLAlchemy engine object for the database connection.

    """

    def __init__(
        self,
        database: str,
        username: str = "root",
        passwd: str = None,
        host: str = "127.0.0.1",
        port: int = 3306,
    ) -> None:

        passwd = passwd if passwd is not None else getpass.getpass("Input password: ")
        self.create_database(database, username, passwd, host, port)
        self._engine = self.get_mysql_engine(database, username, passwd, host, port)

    @staticmethod
    def get_mysql_engine(
        database: str,
        username: str = "root",
        passwd: str = None,
        host: str = "127.0.0.1",
        port: int = 3306,
    ) -> sqlalchemy.Engine:
        """
        Returns a SQLAlchemy engine for connecting to a MySQL database.

        Args:
            database (str): The name of the database to connect to.
            username (str, optional): The username for the database connection. Defaults to "root".
            passwd (str, optional): The password for the database connection. If not provided, it will prompt for input. Defaults to "".
            host (str, optional): The host address for the database connection. Defaults to "127.0.0.1".
            port (int, optional): The port number for the database connection. Defaults to 3306.

        Returns:
            sqlalchemy.Engine: The SQLAlchemy engine object for the MySQL database connection.
        """
        passwd = passwd if passwd is not None else getpass.getpass("Input password: ")
        connet_args = {
            "drivername": "mysql+pymysql",
            "username": username,
            "password": passwd,
            "host": host,
            "port": port,
            "database": database,
            "query": {},
        }

        try:
            engine = create_engine(URL(**connet_args))
        except Exception as e:
            raise Exception from e

        return engine

    def execute(
        self, query_sentence: str
    ) -> Union[None, sqlalchemy.engine.cursor.CursorResult]:
        """
        Executes the given SQL query and returns the result.

        Args:
            query_sentence (str): The SQL query to execute.

        Returns:
            Union[None, sqlalchemy.engine.cursor.CursorResult]: The result of the query execution.
                If the query is a SELECT statement, the result is returned as a CursorResult object.
                Otherwise, None is returned.

        """
        with self._engine.connect() as conn:
            res = conn.execute(text(query_sentence))
            conn.commit()
            if "select" in query_sentence.lower():
                return res.fetchall()
                # print(res.all())

    def df2sql(
        self,
        df: pd.DataFrame,
        table_name: str,
        if_exists: str = "replace",
        dtype: Dict = None,
    ) -> None:
        """
        Convert a pandas DataFrame to a SQL table.

        Args:
            df (pd.DataFrame): The DataFrame to be converted.
            table_name (str): The name of the SQL table.
            if_exists (str, optional): Action to take if the table already exists. Defaults to "replace".

        Returns:
            None
        """
        assert isinstance(df, pd.DataFrame), f"df type should be {pd.DataFrame}"
        dtype = dtype if dtype else self._dtype_dict(df)
        df.to_sql(table_name, self._engine, if_exists=if_exists, dtype=dtype)

    def _dtype_dict(self, df) -> Dict:
        """
        Returns a dictionary mapping column names to SQLAlchemy data types based on the data types of the columns in the given DataFrame.

        Parameters:
        - df: pandas.DataFrame
            The DataFrame containing the columns for which the data types need to be determined.

        Returns:
        - dict
            A dictionary mapping column names to SQLAlchemy data types.

        """
        d = {}
        for i, j in zip(df.columns, df.dtypes):
            if "object" in str(j):
                d.update({i: sqlalchemy.types.TEXT})

            if "datetime" in str(j):
                d.update({i: sqlalchemy.types.DateTime()})

            if "float" in str(j):
                d.update({i: sqlalchemy.types.Float(precision=3, asdecimal=True)})

            if "int" in str(j):
                d.update({i: sqlalchemy.types.INT()})
        return d

    def create_database(
        self,
        database: str,
        username: str = "root",
        passwd: str = "",
        host: str = "127.0.0.1",
        port: int = 3306,
    ) -> None:
        """
        Creates a new database with the given parameters.

        Args:
            database (str): The name of the database to create.
            username (str, optional): The username for the database connection. Defaults to "root".
            passwd (str, optional): The password for the database connection. Defaults to an empty string.
            host (str, optional): The host address for the database connection. Defaults to "127.0.0.1".
            port (int, optional): The port number for the database connection. Defaults to 3306.

        Returns:
            None
        """

        conn = pymysql.connect(user=username, password=passwd, host=host, port=port)
        cur = conn.cursor()

        query = f"CREATE DATABASE IF NOT EXISTS {database};"

        cur.execute(query)
        conn.commit()
        conn.close()

    def create_table(self, table_name: str, columns: str) -> None:
        """
        Create a new table in the database.

        Args:
            table_name (str): The name of the table to be created.
            columns (str): The columns and their data types for the table.

        Returns:
            None
        """
        query = f"CREATE TABLE {table_name} ({columns});"
        self.execute(query)

    def delete_table(self) -> None:
        """
        Deletes the table from the database.

        This method deletes the table from the database. It does not return any value.
        """
        pass

    def create(self, table_name: str, values: str) -> None:
        """
        Inserts a new row into the specified table with the given values.

        Args:
            table_name (str): The name of the table to insert the row into.
            values (str): The values to be inserted into the row.

        Returns:
            None
        """

        query = f"INSERT INTO {table_name} VALUES ({values})"

        self.execute(query)

    def read(
        self, table: str, limit: int = 100, column: str = "", condition: str = None
    ) -> sqlalchemy.engine.cursor.CursorResult:
        """
        Executes a SELECT query on the specified table in the database.

        Args:
            table (str): The name of the table to query.
            limit (int, optional): The maximum number of rows to retrieve. Defaults to 100.
            column (str, optional): The column(s) to select. Defaults to an empty string, which selects all columns.
            condition (str, optional): The condition to apply in the WHERE clause. Defaults to None.

        Returns:
            sqlalchemy.engine.cursor.CursorResult: The result of the query execution.
        """

        limit = "LIMIT " + str(limit) if limit else ""
        query = f"SELECT {column if column else '*'} FROM {table} {limit};"
        if condition:
            query = f"{query} WHERE {condition}"

        return self.execute(query)

    def update(
        self, data, table_name: str, column_name: str, condition: str = ""
    ) -> None:
        """
        Update the specified column in the given table with the provided data.

        Args:
            data: The data to be updated in the column.
            table_name: The name of the table to update.
            column_name: The name of the column to update.
            condition: The optional condition to filter the rows to be updated.

        Returns:
            None
        """

        query = f"UPDATE {table_name} SET {column_name} = {data}"
        if condition:
            query = f"{query} WHERE {condition}"

        self.execute(query)

    def delete(self, table_name: str, condition: str = "") -> None:
        """
        Deletes records from the specified table based on the given condition.

        Args:
            table_name (str): The name of the table to delete records from.
            condition (str, optional): The condition to filter the records to be deleted. Defaults to "".

        Returns:
            None
        """

        query = f"DELETE FROM {table_name}"
        if condition:
            query = f"{query} WHERE {condition}"

        self.execute(query)

    @property
    def engine(self) -> sqlalchemy.Engine:
        """
        Returns the SQLAlchemy engine object used for database operations.

        Returns:
            sqlalchemy.Engine: The SQLAlchemy engine object.
        """
        return self._engine
