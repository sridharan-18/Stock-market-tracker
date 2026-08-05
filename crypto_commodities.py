"""
Cryptocurrency and Commodities Data Module
Supports tracking cryptocurrencies (BTC, ETH) and commodities (gold, oil).
"""

import yfinance as yf
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta


# Cryptocurrency symbols for yfinance
CRYPTO_SYMBOLS = {
    'BTC': 'BTC-USD',
    'ETH': 'ETH-USD',
    'XRP': 'XRP-USD',
    'ADA': 'ADA-USD',
    'SOL': 'SOL-USD',
    'DOGE': 'DOGE-USD',
    'DOT': 'DOT-USD',
    'MATIC': 'MATIC-USD',
    'LINK': 'LINK-USD',
    'AVAX': 'AVAX-USD'
}

# Commodity symbols for yfinance
COMMODITY_SYMBOLS = {
    'GOLD': 'GC=F',  # Gold Futures
    'SILVER': 'SI=F',  # Silver Futures
    'OIL': 'CL=F',  # Crude Oil Futures
    'NATGAS': 'NG=F',  # Natural Gas Futures
    'COPPER': 'HG=F',  # Copper Futures
    'PLATINUM': 'PL=F',  # Platinum Futures
    'CORN': 'ZC=F',  # Corn Futures
    'WHEAT': 'ZW=F',  # Wheat Futures
    'SOYBEAN': 'ZS=F',  # Soybean Futures
    'COFFEE': 'KC=F'  # Coffee Futures
}


class CryptoData:
    """
    Cryptocurrency data fetcher using yfinance.
    """
    
    def __init__(self):
        """Initialize the crypto data fetcher."""
        self.symbols = CRYPTO_SYMBOLS
    
    def get_yfinance_symbol(self, symbol: str) -> str:
        """
        Convert crypto symbol to yfinance format.
        
        Args:
            symbol: Crypto symbol (e.g., 'BTC')
            
        Returns:
            yfinance symbol (e.g., 'BTC-USD')
        """
        if symbol.upper() in self.symbols:
            return self.symbols[symbol.upper()]
        # Default format
        return f"{symbol.upper()}-USD"
    
    def fetch_crypto_data(self, symbol: str, start_date: str, end_date: str, 
                        interval: str = '1d') -> pd.DataFrame:
        """
        Fetch cryptocurrency data.
        
        Args:
            symbol: Crypto symbol
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            interval: Data interval
            
        Returns:
            DataFrame with crypto data
        """
        yf_symbol = self.get_yfinance_symbol(symbol)
        
        try:
            ticker = yf.Ticker(yf_symbol)
            data = ticker.history(start=start_date, end=end_date, interval=interval)
            return data
        except Exception as e:
            print(f"Error fetching crypto data for {symbol}: {e}")
            return pd.DataFrame()
    
    def fetch_crypto_info(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch cryptocurrency information.
        
        Args:
            symbol: Crypto symbol
            
        Returns:
            Dictionary with crypto information
        """
        yf_symbol = self.get_yfinance_symbol(symbol)
        
        try:
            ticker = yf.Ticker(yf_symbol)
            info = ticker.info
            
            crypto_info = {
                'symbol': symbol,
                'yfinance_symbol': yf_symbol,
                'name': info.get('name', 'N/A'),
                'current_price': info.get('currentPrice', 0),
                'previous_close': info.get('previousClose', 0),
                'open': info.get('open', 0),
                'high': info.get('dayHigh', 0),
                'low': info.get('dayLow', 0),
                'volume': info.get('volume', 0),
                'market_cap': info.get('marketCap', 0),
                '24h_volume': info.get('volume24Hr', 0),
                'circulating_supply': info.get('circulatingSupply', 0)
            }
            
            return crypto_info
        except Exception as e:
            print(f"Error fetching crypto info for {symbol}: {e}")
            return {'symbol': symbol, 'error': str(e)}
    
    def get_available_cryptos(self) -> List[str]:
        """Get list of available cryptocurrencies."""
        return list(self.symbols.keys())


class CommodityData:
    """
    Commodity data fetcher using yfinance.
    """
    
    def __init__(self):
        """Initialize the commodity data fetcher."""
        self.symbols = COMMODITY_SYMBOLS
    
    def get_yfinance_symbol(self, symbol: str) -> str:
        """
        Convert commodity symbol to yfinance format.
        
        Args:
            symbol: Commodity symbol (e.g., 'GOLD')
            
        Returns:
            yfinance symbol (e.g., 'GC=F')
        """
        if symbol.upper() in self.symbols:
            return self.symbols[symbol.upper()]
        # Default format for commodities
        return f"{symbol.upper()}=F"
    
    def fetch_commodity_data(self, symbol: str, start_date: str, end_date: str, 
                            interval: str = '1d') -> pd.DataFrame:
        """
        Fetch commodity data.
        
        Args:
            symbol: Commodity symbol
            start_date: Start date
            end_date: End date
            interval: Data interval
            
        Returns:
            DataFrame with commodity data
        """
        yf_symbol = self.get_yfinance_symbol(symbol)
        
        try:
            ticker = yf.Ticker(yf_symbol)
            data = ticker.history(start=start_date, end=end_date, interval=interval)
            return data
        except Exception as e:
            print(f"Error fetching commodity data for {symbol}: {e}")
            return pd.DataFrame()
    
    def fetch_commodity_info(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch commodity information.
        
        Args:
            symbol: Commodity symbol
            
        Returns:
            Dictionary with commodity information
        """
        yf_symbol = self.get_yfinance_symbol(symbol)
        
        try:
            ticker = yf.Ticker(yf_symbol)
            info = ticker.info
            
            commodity_info = {
                'symbol': symbol,
                'yfinance_symbol': yf_symbol,
                'name': info.get('name', 'N/A'),
                'current_price': info.get('currentPrice', 0),
                'previous_close': info.get('previousClose', 0),
                'open': info.get('open', 0),
                'high': info.get('dayHigh', 0),
                'low': info.get('dayLow', 0),
                'volume': info.get('volume', 0),
                'contract_size': info.get('contractSize', 0),
                'exchange': info.get('exchange', 'N/A')
            }
            
            return commodity_info
        except Exception as e:
            print(f"Error fetching commodity info for {symbol}: {e}")
            return {'symbol': symbol, 'error': str(e)}
    
    def get_available_commodities(self) -> List[str]:
        """Get list of available commodities."""
        return list(self.symbols.keys())


class MultiAssetData:
    """
    Combined data fetcher for stocks, crypto, and commodities.
    """
    
    def __init__(self):
        """Initialize the multi-asset data fetcher."""
        self.crypto_fetcher = CryptoData()
        self.commodity_fetcher = CommodityData()
    
    def fetch_asset_data(self, symbol: str, asset_type: str, start_date: str, 
                        end_date: str, interval: str = '1d') -> pd.DataFrame:
        """
        Fetch data for any asset type.
        
        Args:
            symbol: Asset symbol
            asset_type: Type of asset ('stock', 'crypto', 'commodity')
            start_date: Start date
            end_date: End date
            interval: Data interval
            
        Returns:
            DataFrame with asset data
        """
        if asset_type == 'crypto':
            return self.crypto_fetcher.fetch_crypto_data(symbol, start_date, end_date, interval)
        elif asset_type == 'commodity':
            return self.commodity_fetcher.fetch_commodity_data(symbol, start_date, end_date, interval)
        else:
            # Default to stock (yfinance)
            try:
                ticker = yf.Ticker(symbol)
                return ticker.history(start=start_date, end=end_date, interval=interval)
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")
                return pd.DataFrame()
    
    def fetch_multiple_assets(self, assets: List[Dict[str, str]], start_date: str, 
                             end_date: str, interval: str = '1d') -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple assets.
        
        Args:
            assets: List of dicts with 'symbol' and 'type' keys
            start_date: Start date
            end_date: End date
            interval: Data interval
            
        Returns:
            Dictionary with symbol as key and DataFrame as value
        """
        data_dict = {}
        
        for asset in assets:
            symbol = asset['symbol']
            asset_type = asset.get('type', 'stock')
            data = self.fetch_asset_data(symbol, asset_type, start_date, end_date, interval)
            if not data.empty:
                data_dict[symbol] = data
        
        return data_dict


def fetch_crypto_data(symbol: str, start_date: str, end_date: str, 
                     interval: str = '1d') -> pd.DataFrame:
    """Convenience function to fetch crypto data."""
    fetcher = CryptoData()
    return fetcher.fetch_crypto_data(symbol, start_date, end_date, interval)


def fetch_commodity_data(symbol: str, start_date: str, end_date: str, 
                         interval: str = '1d') -> pd.DataFrame:
    """Convenience function to fetch commodity data."""
    fetcher = CommodityData()
    return fetcher.fetch_commodity_data(symbol, start_date, end_date, interval)


def get_default_crypto_symbols() -> List[str]:
    """Get default cryptocurrency symbols."""
    return ['BTC', 'ETH']


def get_default_commodity_symbols() -> List[str]:
    """Get default commodity symbols."""
    return ['GOLD', 'OIL']
