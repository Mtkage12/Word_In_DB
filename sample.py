import os
from func import deco, Db, SearchGate

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
