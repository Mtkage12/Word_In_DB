from func import deco, Db, SearchGate

@deco
def main():
    """SampleCode
    """
    search_word = 'WWWWW'
    file = 'XXXXXX.db'
    target_database = Db(file)
    gate = SearchGate(target_database, search_word)
    print(gate.exist_word_table)


if __name__ == '__main__':
    main()
