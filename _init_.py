from ast import Continue
from ctypes import Union
from datetime import datetime, timedelta
from typing import Optional
from numpy import rint
import openpyxl
from tinkoff.invest.services import Services
from tinkoff.invest import( 
    Client,
    RequestError,
    PortfolioResponse,
    PositionsResponse,
    CandleInterval,
    HistoricCandle,
    OperationsResponse,
    Operation,
    OperationType,
    AccessLevel,

    )
import pandas as pd
from pandas import DataFrame
from matplotlib import pyplot as plt
import ta
from ta.trend import ema_indicator
from configparser import ConfigParser
import os
from datetime import date 

# TODO: узнать почему выводится тип NonType класса
# и каким-то способом записать данные в таблицу XLSX

config = ConfigParser()
config.read("config.ini")
# print(config.sections())
RO_TOKEN = config.get('TINKOFF_INVESTOR', 'ro_token')
FA_TOKEN = config.get('TINKOFF_INVESTOR', 'fa_token')
account_id = config.get('TINKOFF_INVESTOR', 'account_id')

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# использовать при каждом запуске на M1 - arch -x86_64 python get_t_info.py  

# def get_figi_candles():
#     try:
#         with Client(FA_TOKEN) as client:
#             r = client.market_data.get_candles(
#                 figi="USD000UTSTOM",
#                 from_=datetime.utcnow() - timedelta(days=365),
#                 to=datetime.utcnow(),
#                 interval=CandleInterval.CANDLE_INTERVAL_DAY,

#             )
#             df = create_df(r.candles)
#             df['ema'] = ema_indicator(close=df['close'], window=9)
#             # print(len(r.candles))
#             print(df[['time', 'close', 'ema']].tail(30))
#             ax = df.plot(x='time', y='close')
#             df.plot(ax=ax,x='time', y='close')
#             plt.show()

#     except RequestError as e:
#         print(str(e))
#     # TODO: сделать возможность изменения интервалов
#     # внутри графическиз интерфейсов


# def create_df(candles: HistoricCandle):
#     df = DataFrame([{
#         'time': c.time,
#         'volume': c.volume,
#         'open': cast_money(c.open),
#         'close': cast_money(c.close),
#         'high': cast_money(c.high),
#         'low': cast_money(c.low),
#     } for c in candles])
#     return df

def cast_money(v):
    """
    https://tinkoff.github.io/investAPI/faq_custom_types/
    :param v: 
    :return:
    """
    return v.units + v.nano / 1e9


# get_figi_candles()

def run():
    try:
        with Client(FA_TOKEN) as client:
            Hola(client).report()
            Hola(client).write_to_file()
            # Hola(client).write_to_file()
    except RequestError as e:
        print(str(e))

class Hola:
    def __init__(self,client: Services):
        self.usdrur = None
        self.client = client
        self.accounts = []

    def report(self):
        dataframes = []
        for account_id in self.get_accounts():
            df = self.get_operations_df(account_id)
            if df is None: Continue
            dataframes.append(df)

        if len(dataframes) > 0:
            df = pd.concat(dataframes, ignore_index=True).sort_values(by='date', ascending=False)

            print(df.head(1000))
            print(len(df), df['payment'].sum())

    def get_accounts(self):
        r = self.client.users.get_accounts()
        for acc in r.accounts:
            if acc.access_level != AccessLevel.ACCOUNT_ACCESS_LEVEL_NO_ACCESS:
                self.accounts.append(acc.id)
        return self.accounts

    def get_usdrur(self):
        """Получаем курс, только если он нужен"""
        if not self.usdrur:
            u = self.client.market_data.get_last_prices(figi=['USD000UTSTOM'])
            self.usdrur = self.cast_money(u.last_prices[0].price)
        return self.usdrur

    def get_operations_df(self, account_id: str) -> Optional[DataFrame]:
        r: OperationsResponse = self.client.operations.get_operations(
            account_id=account_id,
            from_= datetime(2015, 1, 1),
            to=datetime.utcnow()
        )

        if len(r.operations) < 1: return None
        df = pd.DataFrame([self.operation_to_dict(p, account_id) for p in r.operations])
        return df

    def operation_to_dict(self, o: Operation, account_id: str) -> tuple:
        r = {
            # 'acc': account_id,
            'date': o.date,
            'type': o.type,
            'otype': o.operation_type,
            'currency': o.currency,
            'instrument_type': o.instrument_type,
            'figi': o.figi,
            'quantity': o.quantity,
            'state': o.state,
            'payment': self.cast_money(o.payment, False),
            'price': self.cast_money(o.price, False),
        }
        return r


    def cast_money(self, v, to_rub=True):
        r = v.units + v.nano / 1e9
        if to_rub and hasattr(v, 'currency') and getattr(v, 'currency') == 'usd':
            r *= self.get_usdrur()
        return r
        
    def write_to_file(self) -> list:
        # TODO: запись в Excel работает - это прекрасно 
        # доделать так чтобы печаталась вся информация
        response = self.get_operations_df(account_id)
        response = list(response)
        df1 = pd.DataFrame(response)
        excel_writer = "output.xlsx"
        # for row, data in range(0, len(response)):
        # excel_writer = "output.xlsx"
        # df1 = pd.DataFrame(response)
        # df1.to_excel(excel_writer, index=False, sheet_name="operations")
        
        
        return response

# def simple_write(path, _df):
#     _df.to_excel(path)

if __name__ == '__main__':
    # Hola(account_id).write_to_file()
    run()
    # print("---------------------------------------------------------------- '\n'")
    
