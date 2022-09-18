import sqlite3
import pandas as pd


def is_contain(dataframe, search_word):
    """Are keywords present in the dataframe.

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
    """Are keywords present in the series?

    Args:
        df_series (pd.Series): pandas.Series
        search_word (string): Search Word

    Returns:
        bool: exist in pd.Series -> True
              NOT exist in pd.Series -> False
    """
    df_series = df_series.astype(str)
    return f'{search_word}' in df_series.to_list()


class Read:
    """Reading Class"""
    lst_instanced = []

    def __init__(self, db_filepath: str, table_name: str):
        with sqlite3.connect(db_filepath) as conn:
            df = pd.read_sql_query(f'SELECT * from {table_name}', conn)
        conn.close()
        self.__dataframe = df
        Read.lst_instanced.append(self)

    @property
    def dataframe(self):
        return self.__dataframe


def deco(func):
    """Do start/end prints before the function.

    Args:
        func (function): function
    """
    def wrapper(*args, **kwargs):
        print('--start--')
        func(*args, **kwargs)
        print('---end---')
    return wrapper


@deco
def print_word_in_df(db_filename, search_word):
    """Output which table and column the search word is in from the database.

    Args:
        db_filename (str): Database File Paths
        search_word (str): Search Word
    """
    with sqlite3.connect(db_filename) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM sqlite_master WHERE type='table'")
        all_table_lst = [x[1] for x in cur.fetchall()]

    lst_is_exist_in_table = [l for l in all_table_lst if is_contain(
        Read(db_filename, l).dataframe, search_word) == True]
    for table in lst_is_exist_in_table:
        print(f'TableName:{table}')
        df = Read(db_filename, table).dataframe
        col_book = [col for col in df.columns if is_series_contain(
            df[col], search_word) == True]
        print(f'ColumnsName:{col_book}')
        print('_______________')


if __name__ == '__main__':
    pass
