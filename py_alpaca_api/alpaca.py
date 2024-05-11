import requests
import json

import pandas as pd

from py_alpaca_api.src.data_classes import order_class_from_dict, asset_class_from_dict, account_class_from_dict

# PyAlpacaApi class
class PyAlpacaApi:
    def __init__(self, api_key: str, api_secret: str, api_paper: bool = True):
        '''
        PyAlpacaApi class constructor
        api_key: Alpaca API Key, required
        api_secret: Alpaca API Secret, required
        api_paper: Use Alpaca Paper Trading API (default: True)
        '''
        # Check if API Key and Secret are provided
        if not api_key:
            raise ValueError('API Key is required')
        if not api_secret:
            raise ValueError('API Secret is required')
        # Set the API Key and Secret
        self.headers = {
            'APCA-API-KEY-ID': api_key,
            'APCA-API-SECRET-KEY': api_secret
        }
        # Set the API URL's
        if api_paper:
            self.trade_url  = 'https://paper-api.alpaca.markets/v2'
        else:
            self.trade_url  = 'https://api.alpaca.markets/v2'
            self.data_url   = 'https://data.alpaca.markets/v2'

    ########################################################
    #\\\\\\\\\/////////  Get Order BY id \\\\\\\///////////#
    ########################################################
    def get_order_by_id(self, order_id: str, nested: bool = False):
        '''
        Get order information by order ID
        order_id: Order ID to get information
        nested: Include nested objects (default: False)
        return: OrderClass object with order information
        Exception: Exception if failed to get order information
        '''
        # Parameters for the request
        params = {
            'nested': nested
        }
        # Alpaca API URL for order information
        url = f'{self.trade_url}/orders/{order_id}'
        # Get request to Alpaca API for order information
        response = requests.get(url, headers=self.headers, params=params)
        # Check if response is successful
        if response.status_code == 200:
            # Convert JSON response to dictionary
            res = json.loads(response.text)
            # Return order information as an OrderClass object
            return order_class_from_dict(res)
        # If response is not successful, raise an exception
        else:
            res = json.loads(response.text)
            raise ValueError(f'Failed to get order information. Response: {res["message"]}')
            
    ########################################################
    #\\\\\\\\\\\\\\\\\ Cancel Order By ID /////////////////#
    ########################################################
    def cancel_order_by_id(self, order_id: str):
        '''
        Cancel order by order ID
        order_id: Order ID to cancel
        return: Order cancellation message
        Exception: Exception if failed to cancel order
        '''
        # Alpaca API URL for canceling an order
        url = f'{self.trade_url}/orders/{order_id}'
        # Delete request to Alpaca API for canceling an order
        response = requests.delete(url, headers=self.headers)
        # Check if response is successful
        if response.status_code == 204:
            # Convert JSON response to dictionary
            return f"Order {order_id} has been cancelled"
        # If response is not successful, raise an exception
        else:
            res = json.loads(response.text)
            raise Exception(f'Failed to cancel order {order_id}, Response: {res["message"]}')

    ########################################################
    #\\\\\\\\\\\\\\\\  Cancel All Orders //////////////////#
    ########################################################
    def cancel_all_orders(self):
        '''
        Cancel all orders
        return: Number of orders cancelled
        '''
        # Alpaca API URL for canceling all orders
        url = f'{self.trade_url}/orders'
        # Delete request to Alpaca API for canceling all orders
        response = requests.delete(url, headers=self.headers)
        # Check if response is successful
        if response.status_code == 207:
            # Convert JSON response to dictionary
            res = json.loads(response.text)
            return f"{len(res)} orders have been cancelled"
        # If response is not successful, raise an exception
        else:
            res = json.loads(response.text)
            raise Exception(f'Failed to cancel orders. Response: {res["message"]}')

    ########################################################
    #\\\\\\\\\\\\\\\\  Submit Market Order ////////////////#
    ########################################################
    def market_order(self, symbol: str, qty: float=None, notional: float=None, side: str='buy', time_in_force: str = 'day', extended_hours: bool = False):
        '''
        Submit a market order
        symbol: Asset symbol to buy/sell
        qty: Quantity of asset to buy/sell (default: None)
        notional: Notional value of asset to buy/sell (default: None)
        side: Order side (buy/sell) (default: buy)
        time_in_force: Time in force options (day, gtc, opg, cls, ioc, fok) (default: day)
        extended_hours: Extended hours trading (default: False)
        return: MarketOrderClass object with
        values: id, client_order_id, created_at, submitted_at, asset_id, symbol, asset_class, notional, qty, filled_qty, filled_avg_price, 
                order_class, order_type
        Exception: Exception if failed to submit market order
        '''
        # Alpaca API URL for submitting market order
        url = f'{self.trade_url}/orders'
        # Market order payload
        payload = {
            'symbol': symbol,
            'qty': qty if qty else None,
            'notional': round(notional, 2) if notional else None,
            'side': side if side=='buy' else 'sell',
            'type': 'market',
            'time_in_force': time_in_force,
            'extended_hours': extended_hours
        }
        # Post request to Alpaca API for submitting market order
        response = requests.post(url, headers=self.headers, json=payload)
        # Check if response is successful
        if response.status_code == 200:
            # Convert JSON response to dictionary
            res = json.loads(response.text)
            # Return market order information as a MarketOrderClass object
            return order_class_from_dict(res)
        # If response is not successful, raise an exception
        else:
            res = json.loads(response.text)
            raise Exception(f'Failed to submit market order. Code: {response.status_code}, Response: {res["message"]}')
        
    #####################################################
    #\\\\\\\\\\\\\\\\\\\  Get Asset ////////////////////#
    #####################################################
    def get_asset(self, symbol: str):
        '''
        Get asset information
        symbol: Asset symbol
        return: AssetClass object with
        values: id, class, exchange, symbol, status, tradable, marginable, shortable, easy_to_borrow, fractionable
        Execption: ValueError if failed to get asset information
        '''
        # Alpaca API URL for asset information
        url = f'{self.trade_url}/assets/{symbol}'
        # Get request to Alpaca API for asset information
        response = requests.get(url, headers=self.headers)
        # Check if response is successful
        if response.status_code == 200:
            # Convert JSON response to dictionary
            res = json.loads(response.text)
            # Return asset information as an AssetClass object
            return asset_class_from_dict(res)
        # If response is not successful, raise an exception
        else:
            raise ValueError(f'Failed to get asset information. Response: {response.text}')
        
    ########################################################
    #\\\\\\\\\\\\\  Get Account Information ///////////////#
    ########################################################
    def get_account(self):
        '''
        Get account information
        return: AccountClass object with account information
        values: id, admin_configurations, user_configurations, account_number, status, crypto_status, options_approved_level, 
                options_trading_level, currency, buying_power, regt_buying_power, daytrading_buying_power, effective_buying_power, 
                non_marginable_buying_power, options_buying_power, bod_dtbp, cash, accrued_fees, pending_transfer_in, portfolio_value, 
                pattern_day_trader, trading_blocked, transfers_blocked, account_blocked, created_at, trade_suspended_by_user, multiplier, 
                shorting_enabled, equity, last_equity, long_market_value, short_market_value, position_market_value, initial_margin, 
                maintenance_margin, last_maintenance_margin, sma, daytrade_count, balance_asof, crypto_tier, intraday_adjustments, pending_reg_taf_fees  
        Exception: Exception if failed to get account information
        '''
        # Alpaca API URL for account information
        url = f'{self.trade_url}/account'
        # Get request to Alpaca API for account information
        response = requests.get(url, headers=self.headers)
        # Check if response is successful
        if response.status_code == 200:
            # Convert JSON response to dictionary
            res = json.loads(response.text)
            # Return account information as an AccountClass object
            return account_class_from_dict(res)
        # If response is not successful, raise an exception
        else:
            raise Exception(f'Failed to get account information. Response: {response.text}')