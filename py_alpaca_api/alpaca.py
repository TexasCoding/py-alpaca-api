import requests

class PyAlpacaApi:
    def __init__(self, api_key: str, api_secret: str, api_paper: bool = True):
        # Check if API Key and Secret are provided
        if not api_key:
            raise ValueError('API Key is required')
        if not api_secret:
            raise ValueError('API Secret is required')
        
        self.api_key    = api_key
        self.api_secret = api_secret
        self.api_paper  = api_paper
        
        # Set the API URL's
        if self.api_paper:
            self.trade_url  = 'https://paper-api.alpaca.markets/v2'
        else:
            self.trade_url  = 'https://api.alpaca.markets/v2'
            self.data_url   = 'https://data.alpaca.markets/v2'

    ########################################################
    #\\\\\\\\\\\\\  Get Account Information ///////////////#
    ########################################################
    def get_account(self):
        url = f'{self.trade_url}/account'
        headers = {
            'APCA-API-KEY-ID': self.api_key,
            'APCA-API-SECRET-KEY': self.api_secret
        }
        response = requests.get(url, headers=headers)
        return response.json()