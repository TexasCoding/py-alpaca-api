import requests
import json

from py_alpaca_api.src.data_classes import AccountClass, AssetClass, OrderClass

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
            return OrderClass(
                id=str(res['id']) if res['id'] else '',
                client_order_id=res['client_order_id'],
                created_at=res['created_at'].split('.')[0].replace('T', ' ') if res['created_at'] else '',
                updated_at=res['updated_at'].split('.')[0].replace('T', ' ') if res['updated_at'] else '',
                submitted_at=res['submitted_at'].split('.')[0].replace('T', ' ') if res['submitted_at'] else '',
                filled_at=res['filled_at'].split('.')[0].replace('T', ' ') if res['filled_at'] else '',
                expired_at=res['expired_at'].split('.')[0].replace('T', ' ') if res['expired_at'] else '',
                canceled_at=res['canceled_at'].split('.')[0].replace('T', ' ') if res['canceled_at'] else '',
                failed_at=res['failed_at'].split('.')[0].replace('T', ' ') if res['failed_at'] else '',
                replaced_at=res['replaced_at'].split('.')[0].replace('T', ' ') if res['replaced_at'] else '',
                replaced_by=res['replaced_by'].split('.')[0].replace('T', ' ') if res['replaced_by'] else '',
                replaces=str(res['replaces']) if res['replaces'] else '',
                asset_id=str(res['asset_id']) if res['asset_id'] else '',
                symbol=str(res['symbol']) if res['symbol'] else '',
                asset_class=str(res['asset_class']) if res['asset_class'] else '',
                notional=float(res['notional']) if res['notional'] else 0.0,
                qty=float(res['qty']) if res['qty'] else 0.0,
                filled_qty=float(res['filled_qty']) if res['filled_qty'] else 0,
                filled_avg_price=float(res['filled_avg_price']) if res['filled_avg_price'] else 0,
                order_class=str(res['order_class']) if res['order_class'] else '',
                order_type=res['order_type'],
                type=str(res['type']),
                side=str(res['side']),
                time_in_force=res['time_in_force'],
                limit_price=float(res['limit_price']) if res['limit_price'] else 0,
                stop_price=float(res['stop_price']) if res['stop_price'] else 0,
                status=res['status'],
                extended_hours=bool(res['extended_hours']),
                legs=object(res['legs']) if res['legs'] else {},
                trail_percent=float(res['trail_percent']) if res['trail_percent'] else 0,
                trail_price=float(res['trail_price']) if res['trail_price'] else 0,
                hwm=float(res['hwm']) if res['hwm'] else 0,
                subtag=res['subtag'],
                source=res['source']
            )
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
            return AssetClass(
                id=res['id'],
                asset_class=res['class'],
                easy_to_borrow=bool(res['easy_to_borrow']),
                exchange=res['exchange'],
                fractionable=bool(res['fractionable']),
                maintenance_margin_requirement=float(res['maintenance_margin_requirement']) if res['maintenance_margin_requirement'] else None,
                marginable=bool(res['marginable']),
                name=res['name'],
                shortable=bool(res['shortable']),
                status=res['status'],
                symbol=res['symbol'],
                tradable=bool(res['tradable'])
            )
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
            return AccountClass(
                id=res['id'],
                admin_configurations=res['admin_configurations'],
                user_configurations=res['user_configurations'],
                account_number=str(res['account_number']),
                status=str(res['status']),
                crypto_status=res['crypto_status'],
                options_approved_level=int(res['options_approved_level']) if res['options_approved_level'] else None,
                options_trading_level=int(res['options_trading_level']) if res['options_trading_level'] else None,
                currency=res['currency'],
                buying_power=float(res['buying_power']) if res['buying_power'] else None,
                regt_buying_power=float(res['regt_buying_power']) if res['regt_buying_power'] else None,
                daytrading_buying_power=float(res['daytrading_buying_power']) if res['daytrading_buying_power'] else None,
                effective_buying_power=float(res['effective_buying_power']) if res['effective_buying_power'] else None,
                non_marginable_buying_power=float(res['non_marginable_buying_power']) if res['non_marginable_buying_power'] else None,
                options_buying_power=float(res['options_buying_power']) if res['options_buying_power'] else None,
                bod_dtbp=float(res['bod_dtbp']) if res['bod_dtbp'] else None,
                cash=float(res['cash']) if res['cash'] else None,
                accrued_fees=float(res['accrued_fees']) if res['accrued_fees'] else None,
                pending_transfer_in=float(res['pending_transfer_in']) if res['pending_transfer_in'] else None,
                portfolio_value=float(res['portfolio_value']) if res['portfolio_value'] else None,
                pattern_day_trader=bool(res['pattern_day_trader']),
                trading_blocked=bool(res['trading_blocked']),
                transfers_blocked=bool(res['transfers_blocked']),
                account_blocked=bool(res['account_blocked']),
                created_at=res['created_at'].split('.')[0].replace('T', ' ') if res['created_at'] else None,
                trade_suspended_by_user=bool(res['trade_suspended_by_user']),
                multiplier=int(res['multiplier']) if res['multiplier'] else None,
                shorting_enabled=bool(res['shorting_enabled']),
                equity=float(res['equity']) if res['equity'] else None,
                last_equity=float(res['last_equity']) if res['last_equity'] else None,
                long_market_value=float(res['long_market_value']) if res['long_market_value'] else None,
                short_market_value=float(res['short_market_value']) if res['short_market_value'] else None,
                position_market_value=float(res['position_market_value']) if res['position_market_value'] else None,
                initial_margin=float(res['initial_margin']) if res['initial_margin'] else None,
                maintenance_margin=float(res['maintenance_margin']) if res['maintenance_margin'] else None,
                last_maintenance_margin=float(res['last_maintenance_margin']) if res['last_maintenance_margin'] else None,
                sma=float(res['sma']) if res['sma'] else None,
                daytrade_count=int(res['daytrade_count']) if res['daytrade_count'] else None,
                balance_asof=res['balance_asof'],
                crypto_tier=int(res['crypto_tier']) if res['crypto_tier'] else None,
                intraday_adjustments=int(res['intraday_adjustments']) if res['intraday_adjustments'] else None,
                pending_reg_taf_fees=float(res['pending_reg_taf_fees']) if res['pending_reg_taf_fees'] else None
            )
        # If response is not successful, raise an exception
        else:
            raise Exception(f'Failed to get account information. Response: {response.text}')