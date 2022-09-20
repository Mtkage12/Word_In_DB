import os
import pandas as pd
from func import deco, Db, SearchGate, Table, get_now
# from feature_log import Output


@deco
def main():
    """SampleCode
    """
    search_word = 'WWWWW'
    file = 'XXXXXX.db'
    target_database = Db(file)
    gate = SearchGate(target_database, search_word)
    gate.output()


if __name__ == '__main__':
    os.chdir(os.getcwd())
    main()
