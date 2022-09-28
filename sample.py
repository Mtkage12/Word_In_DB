import os
from func import deco, Db, SearchGate


@deco
def main():
    """SampleCode
    """
    search_word = '1000'
    file = 'XXXX.db'
    target_database = Db(file)
    gate = SearchGate(target_database, search_word)
    print(gate.exist_word_table)
    print(os.getcwd())
    if gate.len > 0:
        gate.output()
    else:
        print('no data')


if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    main()
