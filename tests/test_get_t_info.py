import pytest

from get_t_info import(
    get_accounts,
    get_user_tariff_request,
    get_user_tariff_response,
    get_info_request,
    get_trading_schedules,
    get_currencies_response,
    get_etf_response,
    get_futures_response,
    get_shares_responces,
    get_share_by_ticker,
    get_dividends_requests,

)

# target = __import__("get_t_info.py")

def test_sum():
    assert sum([1,2,3]) == 6, "Should be 6"

def test_get_accounts():
    assert get_accounts() == True, "Should be True"


if __name__ == "__main__":
    test_sum()
    print("Test_sum is passed")






















