import pandas as pd
import math

class Stock_Info:
    def __init__(self, name):
        self.name = name
        self.df = self.read_from_csv(name)
        self.data_types = ['ROIC', 'Sales', 'EPS', 'Equity', 'FCF']
        self.big_five = {
            'ROIC': {'10y': 0, '5y': 0, 'ttm': 0},
            'Sales': {'10y': 0, '5y': 0, 'ttm': 0},
            'EPS': {'10y': 0, '5y': 0, 'ttm': 0},
            'Equity': {'10y': 0, '5y': 0, 'ttm': 0},
            'FCF': {'10y': 0, '5y': 0, 'ttm': 0},
        }
        self.sticker_price = 0
        self.MOS_price = 0

        for data_type in self.data_types:
            self.compute_data(data_type)

        current, mos = self.compute_sticker_price().values()
        self.sticker_price = "{:.3f}".format(current)
        self.MOS_price = "{:.3f}".format(mos)

    def print_big_five(self):
        print("TYPE\t\t10Y\t\t5Y\t\tTTM")
        for key, values in self.big_five.items():
            print("{}\t\t{}\t\t{}\t\t{}".format(
                key, values.get('10y'), values.get('5y'), values.get('ttm')
            ))

    def get_data(self, type, years):
        return float(self.big_five[type][years])
    
    def set_data(self, type, ten, five, one):
        data = self.big_five[type]
        data['10y'] = "{:.3f}".format(ten)
        data['5y'] = "{:.3f}".format(five)
        data['ttm'] = "{:.3f}".format(one)
        self.big_five[type] = data

    def read_from_csv(self, name='', index='Year'):
        path = 'csv/' + name + '.csv'
        try:
            f = open(path)
        except FileNotFoundError:
            print("File does not exists!")
        df = pd.read_csv(path, index_col=index)
        return df

    def compute_roic(self, roic_list):
        length = len(roic_list)
        sum = 0.0
        for roic in roic_list:
            sum += roic
        avg = sum / length
        return avg

    def compute_growth_rate(self, prev, current, years):
        if current < 0 or prev < 0:
            if current < 0: current = -current
            if prev < 0: prev = -prev
            doubles = math.log2(current / prev)
            double_years = years / doubles
            growth = 72.0 / double_years
            return growth
        else:
            doubles = math.log2(current / prev)
            double_years = years / doubles
            growth = 72.0 / double_years
            return growth

    def compute_data(self, type):
        df = self.df[type]
        ten_year = df[-11 :]
        five_year = df[-6 :]
        one_year = df[-2 :]

        result_ten = 0
        result_five = 0
        result_one = 0
        if type == 'ROIC':
            result_ten = self.compute_roic(ten_year)
            result_five = self.compute_roic(five_year)
            result_one = self.compute_roic(one_year)
        else:
            result_ten = self.compute_growth_rate(ten_year[0], ten_year[-1], 10)
            result_five = self.compute_growth_rate(five_year[0], five_year[-1], 5)
            result_one = self.compute_growth_rate(one_year[0], one_year[-1], 1)

        self.set_data(type, result_ten, result_five, result_one)

    def compute_sticker_price(self):
        # historical growth rate(equity or other if more reasonable)
        estimated_EPS_growth_rate = self.get_data('Equity', '10y')
        if (estimated_EPS_growth_rate < 0):
            sum = 0
            for data_type in self.data_types:
                sum += self.get_data(data_type, '10y')
            estimated_EPS_growth_rate = sum / len(self.data_types)
        x = 72.0 / estimated_EPS_growth_rate
        future_EPS = float(self.big_five['EPS']['ttm']) * (2**(10.0 / x))
        future_PE = 2.0 * estimated_EPS_growth_rate
        future_sticker_price = future_EPS * future_PE
        min_return_divider = 4.0 # 15% return rate assumption
        current_sticker_price = future_sticker_price / min_return_divider
        if current_sticker_price < 0:
            MOS_sticker_price = current_sticker_price * 2.0
        else:
            MOS_sticker_price = current_sticker_price / 2.0

        return {'current': current_sticker_price, 'MOS': MOS_sticker_price}

    def to_csv(self):
        pass

if __name__ == '__main__':
    name = input("Enter the stock ticker symbol(e.g. APPL): ")
    stock = Stock_Info(name)
    stock.print_big_five()
    print("Current Sticker Price: " + stock.sticker_price + " $")
    print("Current MOS Price: " + stock.MOS_price + " $")
