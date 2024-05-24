import os

import pytest

from py_alpaca_api.alpaca import PyAlpacaApi

# The following keys are for testing purposes only
# You should never hardcode your keys in your code
# Instead, you should use environment variables
# to store your keys and access them in your code
# Create a .env file in the root directory of the project for the following:
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")


@pytest.fixture
def alpaca():
    return PyAlpacaApi(api_key=api_key, api_secret=api_secret, api_paper=True)


@pytest.fixture
def watchlist(alpaca, name="test_list"):
    return alpaca.watchlist.create(
        name=name, symbols="NVDA, PYPL, NFLX, ADBE, CRM, ORCL, IBM, INTC, CSCO"
    )


def delete_all_watchlists(alpaca):
    for watchlist in alpaca.watchlist.get_all():
        alpaca.watchlist.delete(watchlist_name=watchlist.name)


#########################################
##### Test cases for Watchlist ##########
#########################################
def test_watchlist_create(alpaca):
    delete_all_watchlists(alpaca)
    watchlist = alpaca.watchlist.create(
        name="test_list", symbols="NVDA, PYPL, NFLX, ADBE, CRM"
    )
    assert watchlist.name == "test_list"
    assert len(watchlist.assets) == 5
    delete_all_watchlists(alpaca)


def test_watchlist_update(alpaca):
    delete_all_watchlists(alpaca)
    watchlist = alpaca.watchlist.create(
        name="test_list", symbols="NVDA, PYPL, NFLX, ADBE, CRM"
    )
    assert watchlist.name == "test_list"
    assert len(watchlist.assets) == 5
    alpaca.watchlist.update(
        watchlist_name=watchlist.name,
        name="test_list",
        symbols="NVDA, PYPL, NFLX, ADBE, CRM, ORCL, IBM, INTC, CSCO",
    )
    updated_watchlist = alpaca.watchlist.get_assets(
        watchlist_name=watchlist.name
    )
    assert len(updated_watchlist) == 9
    delete_all_watchlists(alpaca)


def test_watchlist_add_asset(alpaca):
    delete_all_watchlists(alpaca)
    watchlist = alpaca.watchlist.create(
        name="test_list", symbols="NVDA, PYPL, NFLX, ADBE, CRM"
    )
    assert len(alpaca.watchlist.get_assets(watchlist_name=watchlist.name)) == 5
    alpaca.watchlist.add_asset(watchlist_name=watchlist.name, symbol="AAPL")
    assert len(alpaca.watchlist.get_assets(watchlist_name=watchlist.name)) == 6
    delete_all_watchlists(alpaca)


def test_watchlist_remove_asset(alpaca):
    delete_all_watchlists(alpaca)
    watchlist = alpaca.watchlist.create(
        name="test_list", symbols="NVDA, PYPL, NFLX, ADBE, CRM"
    )
    assert len(alpaca.watchlist.get_assets(watchlist_name=watchlist.name)) == 5
    alpaca.watchlist.remove_asset(watchlist_name=watchlist.name, symbol="CRM")
    assert len(alpaca.watchlist.get_assets(watchlist_name=watchlist.name)) == 4
    delete_all_watchlists(alpaca)


def test_watchlist_name_get_assets(alpaca):
    delete_all_watchlists(alpaca)
    watchlist = alpaca.watchlist.create(
        name="test_list",
        symbols="NVDA, PYPL, NFLX, ADBE, CRM, ORCL, IBM, INTC, CSCO",
    )
    assets = alpaca.watchlist.get_assets(watchlist_name=watchlist.name)
    assert len(assets) == 9
    delete_all_watchlists(alpaca)


def test_watchlist_id_get_assets(alpaca):
    delete_all_watchlists(alpaca)
    watchlist = alpaca.watchlist.create(
        name="test_list",
        symbols="NVDA, PYPL, NFLX, ADBE, CRM, ORCL, IBM, INTC, CSCO",
    )
    assets = alpaca.watchlist.get_assets(watchlist_name=watchlist.name)
    assert len(assets) == 9
    delete_all_watchlists(alpaca)


def test_watchlist_compare_asset_counts(alpaca):
    delete_all_watchlists(alpaca)
    limit = 5
    watchlist = alpaca.watchlist.create(
        name="test_list",
        symbols="NVDA, PYPL, NFLX, ADBE, CRM, ORCL, IBM, INTC, CSCO",
    )
    assets = alpaca.watchlist.get_assets(watchlist_name=watchlist.name)
    assert len(assets) if len(assets) < limit else limit
    delete_all_watchlists(alpaca)


def test_watchlist_get_all(alpaca):
    delete_all_watchlists(alpaca)
    watchlists = 0
    while watchlists < 5:
        alpaca.watchlist.create(
            name=f"test_list_{watchlists}",
            symbols="NVDA, PYPL, NFLX, ADBE, CRM",
        )
        watchlists += 1
    watchlists = alpaca.watchlist.get_all()
    assert len(watchlists) == 5
    assert watchlists[0].name == "test_list_0"
    assert len(watchlists[0].assets) == 5
    assert watchlists[1].name == "test_list_1"
    assert len(watchlists[1].assets) == 5
    assert watchlists[2].name == "test_list_2"
    assert len(watchlists[2].assets) == 5
    assert watchlists[3].name == "test_list_3"
    assert len(watchlists[3].assets) == 5
    assert watchlists[4].name == "test_list_4"
    assert len(watchlists[4].assets) == 5
    delete_all_watchlists(alpaca)
