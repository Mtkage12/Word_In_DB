import sqlite3
import pandas as pd

def is_contain(dataframe, search_word):
    return f'{search_word}' in dataframe.values

def is_series_contain(dataframe, search_word):
    return f'{search_word}' in dataframe.to_list()


class Read:
    """読み込みクラス"""
    cnt = []
    def __init__(self, db_filepath: str, table_name: str):
        with sqlite3.connect(db_filepath) as conn:
            df = pd.read_sql_query(f'SELECT * from {table_name}', conn)
        conn.close()
        self.data = df
        Read.cnt.append(self)
        
def print_word_in_df(db_filename, search_word):
    """データベースから検索ワードがどのテーブル、カラムにあるのかを出力

    Args:
        db_filename (str): データベースファイルパス
        search_word (str): 検索ワード
    """
    print('_______________')
    with sqlite3.connect(db_filename) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM sqlite_master WHERE type='table'")
        table_lst = [x[1] for x in cur.fetchall()]
    book = [l for l in table_lst if is_contain(Read(db_filename, l).data, search_word)==True]
    for b in book:
        print(f'テーブル名：{b}')
        df = Read(db_filename, b).data
        col_lst = df.columns
        col_book = [c for c in col_lst if is_series_contain(df[c], search_word)==True]
        print(f'カラム名：{col_book}')
        print('_______________')
        
if __name__ == '__main__':
    print_word_in_df('xxx.db', 'wwwww')