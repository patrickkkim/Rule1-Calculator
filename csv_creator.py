import pandas as pd

if __name__ == '__main__':
    data_types = ['ROIC', 'Sales', 'EPS', 'Equity', 'FCF']
    big_five = {}

    for data_type in data_types:
        data_str = input(data_type + ": ")
        data_list = data_str.split()
        for i, data in enumerate(data_list):
            data_list[i] = data.replace('%', '').replace('$', '').replace(',', '')
        big_five[data_type] = data_list

    result = pd.DataFrame.from_dict(big_five)
    result.to_csv("result/result.csv")