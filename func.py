from typing import Dict, List
import sqlite3
import pandas as pd
import datetime


def deco(func):
    """Do (start or end) prints wrap the function.

    Args:
        func (function): function
    """
    def wrapper(*args, **kwargs):
        print('--start--')
        func(*args, **kwargs)
        print('---end---')
    return wrapper


def get_now():
    """Returns the current time in 'YYYYMMDDhhmmss format'

    Returns:
        str: Current date and time (Japan)
    """
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    return now.strftime('%Y%m%d%H%M')


def is_contain(dataframe, search_word):
    """Is keyword exist in the dataframe.

    Args:
        dataframe (pd.DataFrame): pandas.DataFrame
        search_word (string): Search Word

    Returns:
        bool: exist in pd.DataFrame -> True
              NOT exist in pd.DataFrame -> False
    """
    for i in dataframe.columns:
        dataframe[f'{i}'] = dataframe[f'{i}'].astype(str)
    return f'{search_word}' in dataframe.values


def is_series_contain(df_series, search_word):
    """Is keyword exist in the series?

    Args:
        df_series (pd.Series): pandas.Series
        search_word (string): Search Word

    Returns:
        bool: exist in pd.Series -> True
              NOT exist in pd.Series -> False
    """
    df_series = df_series.astype(str)
    return f'{search_word}' in df_series.to_list()


class Table:
    """Reading Class"""

    def __init__(self, db_filepath: str, table_name: str):
        with sqlite3.connect(db_filepath) as conn:
            df = pd.read_sql_query(f'SELECT * from {table_name}', conn)
        conn.close()
        for i in df.columns:
            df[f'{i}'] = df[f'{i}'].astype(str)
        self.__dataframe = df

    @property
    def dataframe(self):
        return self.__dataframe


class Db:
    """Database Class"""

    def __init__(self, file_name) -> None:
        self.__file_name: str = file_name
        self.__table_lst: List[str] = self.get_all_tables()

    def get_all_tables(self):
        """Extract all tables in DB

        Returns:
            List: all tables
        """
        with sqlite3.connect(self.__file_name) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM sqlite_master WHERE type='table'")
            return [x[1] for x in cur.fetchall()]

    @property
    def file_name(self):
        return self.__file_name

    @property
    def table_lst(self):
        return self.__table_lst


class SearchGate:
    """Let the database pass through the search character gate
    """

    def __init__(self, db: Db, search_word: str):
        self.__search_word = search_word
        self.__exist_word_table = self.get_exist_table_info(db)
        self.__db = db

    def get_exist_table_info(self, db: Db) -> Dict[str, List]:
        """Returns table information that exists.

        Args:
            db (Db): str

        Returns:
            Dict[str, List]: {table_name: [column_name,..]}
        """
        book = {}
        lst_is_exist_in_table = [l for l in db.table_lst if is_contain(
            Table(db.file_name, l).dataframe, self.__search_word) == True]
        for table in lst_is_exist_in_table:
            df = Table(db.file_name, table).dataframe
            value = [col for col in df.columns if is_series_contain(
                df[col], self.__search_word) == True]
            book.setdefault(table, value)
        return book

    def output(self):
        """Export to ExcelFille

        Outputs:
            ExcelFile: Sheets that filtered export to ExcelFile.
        """
        with pd.ExcelWriter(f'{get_now()}.xlsx') as writer:
            for k, v in self.exist_word_table.items():
                df = Table(self.db.file_name, k).dataframe.copy()
                buf = df[df[f'{v[0]}'] == f'{self.__search_word}'].copy()
                buf.to_excel(writer, sheet_name=f'{k}', index=False)
        return None

    @property
    def search_word(self):
        return self.__search_word

    @property
    def exist_word_table(self):
        return self.__exist_word_table

    @property
    def db(self):
        return self.__db


if __name__ == '__main__':
    pass
