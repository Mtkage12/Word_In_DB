import pandas as pd
from func import get_now

def output(dataframe, table_lst):
    with pd.ExcelWriter(f'{get_now()}.xlsx') as writer:
        for table in table_lst:
            dataframe.to_excel(writer, sheet_name=f'{table}', index=False)