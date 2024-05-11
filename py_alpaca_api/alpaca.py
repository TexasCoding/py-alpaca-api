import requests
import json

from py_alpaca_api.src.data_classes import AccountClass, AssetClass

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


    def get_asset(self, symbol: str):
        '''
        Get asset information
        symbol: Asset symbol
        return: AssetClass object with
        values: id, class, exchange, symbol, status, tradable, marginable, shortable, easy_to_borrow, fractionable
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
                easy_to_borrow=res['easy_to_borrow'],
                exchange=res['exchange'],
                fractionable=res['fractionable'],
                maintenance_margin_requirement=res['maintenance_margin_requirement'],
                marginable=res['marginable'],
                name=res['name'],
                shortable=res['shortable'],
                status=res['status'],
                symbol=res['symbol'],
                tradable=res['tradable']
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
                account_number=res['account_number'],
                status=res['status'],
                crypto_status=res['crypto_status'],
                options_approved_level=res['options_approved_level'],
                options_trading_level=res['options_trading_level'],
                currency=res['currency'],
                buying_power=res['buying_power'],
                regt_buying_power=res['regt_buying_power'],
                daytrading_buying_power=res['daytrading_buying_power'],
                effective_buying_power=res['effective_buying_power'],
                non_marginable_buying_power=res['non_marginable_buying_power'],
                options_buying_power=res['options_buying_power'],
                bod_dtbp=res['bod_dtbp'],
                cash=res['cash'],
                accrued_fees=res['accrued_fees'],
                pending_transfer_in=res['pending_transfer_in'],
                portfolio_value=res['portfolio_value'],
                pattern_day_trader=res['pattern_day_trader'],
                trading_blocked=res['trading_blocked'],
                transfers_blocked=res['transfers_blocked'],
                account_blocked=res['account_blocked'],
                created_at=res['created_at'],
                trade_suspended_by_user=res['trade_suspended_by_user'],
                multiplier=res['multiplier'],
                shorting_enabled=res['shorting_enabled'],
                equity=res['equity'],
                last_equity=res['last_equity'],
                long_market_value=res['long_market_value'],
                short_market_value=res['short_market_value'],
                position_market_value=res['position_market_value'],
                initial_margin=res['initial_margin'],
                maintenance_margin=res['maintenance_margin'],
                last_maintenance_margin=res['last_maintenance_margin'],
                sma=res['sma'],
                daytrade_count=res['daytrade_count'],
                balance_asof=res['balance_asof'],
                crypto_tier=res['crypto_tier'],
                intraday_adjustments=res['intraday_adjustments'],
                pending_reg_taf_fees=res['pending_reg_taf_fees']
            )
        # If response is not successful, raise an exception
        else:
            raise Exception(f'Failed to get account information. Response: {response.text}')