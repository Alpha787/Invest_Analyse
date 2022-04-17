from datetime import date, datetime
import platform
import os
from distutils import util

from tinkoff.invest import (
    Client,
    InstrumentIdType,
    InstrumentStatus,
    CandleInterval,
    Account,
    RequestError,
    GetUserTariffRequest,
    GetUserTariffResponse,
    GetInfoRequest,
    BondsResponse,
    CurrenciesResponse,
    EtfResponse,
    FuturesResponse,
    SharesResponse,
    GetDividendsResponse,
    ShareResponse,
    PortfolioResponse,
    PositionsRequest,
    PositionsResponse,
    OperationsResponse,
    OperationsRequest,
)
import datetime
import grpc
from configparser import ConfigParser
import pandas as pd


# TODO:разобраться в работе API Тинькофф сервиса gRPC
# использовать при каждом запуске на M1
# - arch -x86_64 python get_t_info.py  


config = ConfigParser()
config.read("config.ini")
# print(config.sections())

RO_TOKEN = config.get('TINKOFF_INVESTOR', 'ro_token')
FA_TOKEN = config.get('TINKOFF_INVESTOR', 'fa_token')
account_id = config.get('TINKOFF_INVESTOR', 'account_id')
# print(account_id)
# fa_account_id = config.get('TINKOFF_INVESTOR', 'fa_account_id')


def main():
    with Client(RO_TOKEN) as client:
        figi = "BBG00T22WKV5"

        r = client.market_data.get_candles(
            figi=figi,
            from_= datetime.datetime(2022,3,25),
            to=datetime.datetime.now(),
            interval=CandleInterval.CANDLE_INTERVAL_5_MIN
        )

        print(r)      

def get_accounts():
    with Client(FA_TOKEN) as client:
        try:
            response: Account = client.users.get_accounts()
            print(response)
            print("--------------------------------")
            for account in response.accounts:
                print("\t", account.id, account.name, account.status, account.access_level.name, account.opened_date)
        except RequestError as e:
            print(str(e))
# get_accounts()

def get_user_tariff_request():
    with Client(RO_TOKEN) as client:
        try:
            response: GetUserTariffRequest = client.users.get_user_tariff()
            print(response)
        except RequestError as e:
            print(str(e))

# get_user_tariff_request()

def get_user_tariff_response():
    with Client(RO_TOKEN) as client:
        try:
            response: GetUserTariffResponse = client.users.get_user_tariff()
            print(response)
        except RequestError as e:
            print(str(e))

# get_user_tariff_response()

def get_info_request():
    with Client(RO_TOKEN) as client:
        try:
            response: GetInfoRequest = client.users.get_info()
            print(response)
        except RequestError as e:
            print(str(e))

# get_info_request()

def get_trading_schedules():
    # TODO: вывести определенное количество бондов
    # например 10, 15, 20, чтобы не выводить все 648
    with Client(RO_TOKEN) as client:
        try:
            response: BondsResponse = client.instruments.bonds()
            # print(len(response.instruments))
            for bond in response.instruments:
                print("\t",
                bond.figi,
                bond.ticker,
                bond.class_code,
                bond.isin,
                bond.lot,
                bond.currency,
                bond.klong,
                bond.kshort,
                bond.dlong,
                bond.dshort,
                bond.dlong_min,
                bond.dshort_min,
                bond.short_enabled_flag,
                bond.name,
                bond.exchange,
                bond.coupon_quantity_per_year,
                bond.maturity_date,
                bond.nominal,
                bond.state_reg_date,
                bond.placement_date,
                bond.placement_price,
                bond.aci_value,
                bond.country_of_risk,
                bond.country_of_risk_name,
                bond.sector,
                bond.issue_kind,
                bond.issue_size,
                bond.issue_size_plan,
                bond.trading_status,
                bond.otc_flag,
                bond.buy_available_flag,
                bond.sell_available_flag,
                bond.floating_coupon_flag,
                bond.perpetual_flag,
                bond.amortization_flag,
                bond.min_price_increment,
                bond.api_trade_available_flag,
                "-----------------------------"
                )
        except RequestError as e:
            print(str(e))
# get_trading_schedules()

def get_currencies_response():
    # TODO: вывести только полезные валюты
    with Client(RO_TOKEN) as client:
        try:
            response: CurrenciesResponse = client.instruments.currencies()
            # print(response)
            for currency in response.instruments:
                print(
                    "\t",
                    currency.figi,
                    currency.ticker,
                    currency.class_code,
                    currency.isin,
                    currency.lot,
                    currency.currency,
                    currency.klong,
                    currency.kshort,
                    currency.dlong,
                    currency.dshort,
                    currency.dlong_min,
                    currency.dshort_min,
                    currency.short_enabled_flag,
                    currency.name,
                    currency.exchange,
                    currency.nominal,
                    currency.country_of_risk,
                    currency.country_of_risk_name,
                    currency.trading_status,
                    currency.otc_flag,
                    currency.buy_available_flag,
                    currency.sell_available_flag,
                    currency.iso_currency_name,
                    currency.min_price_increment,
                    currency.min_price_increment,
                    currency.api_trade_available_flag,
                )
        except RequestError as e:
            print(str(e))
# get_currencies_response()

def get_etf_response():
    with Client(RO_TOKEN) as client:
        try:
            response: EtfResponse = client.instruments.etfs()
            # print(response)
            for etf in response.instruments:
                print(
                    "\t",
                    etf.figi,
                    etf.ticker,
                    etf.class_code,
                    etf.isin,
                    etf.lot,
                    etf.currency,
                    etf.klong,
                    etf.kshort,
                    etf.dlong,
                    etf.dshort,
                    etf.dlong_min,
                    etf.dshort_min,
                    etf.short_enabled_flag,
                    etf.name,
                    etf.exchange,
                    etf.fixed_commission,
                    etf.focus_type,
                    etf.released_date,
                    etf.num_shares,
                    etf.country_of_risk,
                    etf.country_of_risk_name,
                    etf.rebalancing_freq,
                    etf.trading_status,
                    etf.otc_flag,
                    etf.buy_available_flag,
                    etf.sell_available_flag,
                    etf.min_price_increment,
                    etf.api_trade_available_flag,
                )
                print(len(response.instruments))
        except RequestError as e:
            print(str(e))
# get_etf_response()

def get_futures_response():
    with Client(RO_TOKEN) as client:
        try:
            response: FuturesResponse = client.instruments.futures()
            # print(response)
            for future in response.instruments:
                print(
                    "\t",
                    future.figi,
                    future.ticker,
                    future.class_code,
                    future.lot,
                    future.currency,
                    future.klong,
                    future.kshort,
                    future.dlong,
                    future.dshort,
                    future.dlong_min,
                    future.dshort_min,
                    future.short_enabled_flag,
                    future.name,
                    future.exchange,
                    future.first_trade_date,
                    future.last_trade_date,
                    future.futures_type,
                    future.asset_type,
                    future.basic_asset,
                    future.basic_asset_size,
                    future.country_of_risk,
                    future.country_of_risk_name,
                    future.sector,
                    future.expiration_date,
                    future.trading_status,
                    future.otc_flag,
                    future.buy_available_flag,
                    future.sell_available_flag,
                    future.min_price_increment,
                    future.api_trade_available_flag,
                )

        except RequestError as e:
            print(str(e))

# get_futures_response()

def get_shares_responces():
    with Client(RO_TOKEN) as client:
        try:
            response: SharesResponse = client.instruments.shares()
            for share in response.instruments:
                print(
                    "\t",
                    share.figi,
                    share.ticker,
                    share.class_code,
                    share.lot,
                    share.currency,
                    share.klong,
                    share.kshort,
                    share.dlong,
                    share.dshort,
                    share.dlong_min,
                    share.dshort_min,
                    share.short_enabled_flag,
                    share.name,
                    share.exchange,
                    share.ipo_date,
                    share.issue_size,
                    share.country_of_risk,
                    share.country_of_risk_name,
                    share.sector,
                    share.issue_size_plan,
                    share.nominal,
                    share.trading_status,
                    share.otc_flag,
                    share.buy_available_flag,
                    share.sell_available_flag,
                    share.div_yield_flag,
                    share.share_type,
                    share.min_price_increment,
                    share.api_trade_available_flag,
                )
                print(len(response.instruments))
        except RequestError as e:
            print(str(e))

# get_shares_responces()

def get_share_by_ticker():
    with Client(RO_TOKEN) as client:
        try:
            response: ShareResponse = client.instruments.share_by(id_type="NEE")
            print(response[:3], len(response))
        except RequestError as e:
            print(str(e))

# get_share_by_ticker()

def get_dividends_requests():
    with Client(RO_TOKEN) as client:
        try:
            response: GetDividendsResponse = client.instruments.get_dividends()
            print(response)
        except RequestError as e:
            print(str(e))

# get_dividends_requests()

# positions и portfolio не доступно для Read-Only токена
def get_portfolio_response():
    with Client(FA_TOKEN) as client:
        try:
            response: PortfolioResponse = client.operations.get_portfolio(account_id=account_id)
            
            r = (
                "\t",
                response.total_amount_shares,
                response.total_amount_bonds,
                response.total_amount_etf,
                response.total_amount_currencies,
                response.total_amount_futures,
                response.expected_yield,
                response.positions,
                # "------------------------------",
            )   
            data = pd.DataFrame(r)
            data.to_excel("out_put.xlsx")
            return r
        except RequestError as e:
            print(str(e))

get_portfolio_response()

def get_positions_request():
    with Client(FA_TOKEN) as client:
        try:
            response: PositionsRequest = client.operations.get_positions(account_id=account_id)
            print(response)
        except RequestError as e:
            print(str(e))

# get_positions_request()

# Если функция будет не нужна -> удалить
def get_the_operations_request() -> dict:
    try:
        with Client(FA_TOKEN) as client:
            r: OperationsRequest = client.operations.get_operations(
                account_id=account_id,
                from_=datetime.datetime(2020, 1, 1),
                to=datetime.datetime.utcnow(),
                
            )

    except RequestError as e:
        print(str(e))






