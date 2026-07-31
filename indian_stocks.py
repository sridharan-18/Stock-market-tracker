"""
Indian Stock Data Integration Module
Combines Yahoo Finance (yfinance) with NSE/BSE data for Indian stocks.
"""

import yfinance as yf
import pandas as pd
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta


# Indian stock symbol mappings
NSE_SYMBOLS = {
    'RELIANCE': 'RELIANCE.NS',
    'TCS': 'TCS.NS',
    'HDFCBANK': 'HDFCBANK.NS',
    'INFY': 'INFY.NS',
    'ICICIBANK': 'ICICIBANK.NS',
    'HINDUNILVR': 'HINDUNILVR.NS',
    'ITC': 'ITC.NS',
    'SBIN': 'SBIN.NS',
    'BHARTIARTL': 'BHARTIARTL.NS',
    'KOTAKBANK': 'KOTAKBANK.NS',
    'LT': 'LT.NS',
    'AXISBANK': 'AXISBANK.NS',
    'BAJFINANCE': 'BAJFINANCE.NS',
    'MARUTI': 'MARUTI.NS',
    'HCLTECH': 'HCLTECH.NS',
    'ASIANPAINT': 'ASIANPAINT.NS',
    'SUNPHARMA': 'SUNPHARMA.NS',
    'TITAN': 'TITAN.NS',
    'DMART': 'DMART.NS',
    'WIPRO': 'WIPRO.NS'
}

BSE_SYMBOLS = {
    'RELIANCE': 'RELIANCE.BO',
    'TCS': 'TCS.BO',
    'HDFCBANK': 'HDFCBANK.BO',
    'INFY': 'INFY.BO',
    'ICICIBANK': 'ICICIBANK.BO',
    'HINDUNILVR': 'HINDUNILVR.BO',
    'ITC': 'ITC.BO',
    'SBIN': 'SBIN.BO',
    'BHARTIARTL': 'BHARTIARTL.BO',
    'KOTAKBANK': 'KOTAKBANK.BO',
    'LT': 'LT.BO',
    'AXISBANK': 'AXISBANK.BO',
    'BAJFINANCE': 'BAJFINANCE.BO',
    'MARUTI': 'MARUTI.BO',
    'HCLTECH': 'HCLTECH.BO',
    'ASIANPAINT': 'ASIANPAINT.BO',
    'SUNPHARMA': 'SUNPHARMA.BO',
    'TITAN': 'TITAN.BO',
    'DMART': 'DMART.BO',
    'WIPRO': 'WIPRO.BO'
}


class IndianStockData:
    """
    Combined data fetcher for Indian stocks using yfinance and NSE/BSE APIs.
    """
    
    def __init__(self, exchange: str = 'NSE'):
        """
        Initialize the Indian stock data fetcher.
        
        Args:
            exchange: Exchange to use ('NSE' or 'BSE')
        """
        self.exchange = exchange.upper()
        self.symbol_map = NSE_SYMBOLS if self.exchange == 'NSE' else BSE_SYMBOLS
    
    def get_yfinance_symbol(self, symbol: str) -> str:
        """
        Convert Indian stock symbol to yfinance format.
        
        Args:
            symbol: Indian stock symbol (e.g., 'RELIANCE')
            
        Returns:
            yfinance symbol (e.g., 'RELIANCE.NS')
        """
        # If already in yfinance format, return as-is
        if '.' in symbol:
            return symbol
        
        # Check if symbol exists in mapping
        if symbol.upper() in self.symbol_map:
            return self.symbol_map[symbol.upper()]
        
        # Default: append exchange suffix
        return f"{symbol.upper()}.{self.exchange}"
    
    def fetch_stock_data(self, symbol: str, start_date: str, end_date: str, 
                        interval: str = '1d') -> pd.DataFrame:
        """
        Fetch stock data using yfinance.
        
        Args:
            symbol: Stock symbol
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            interval: Data interval (1d, 1h, etc.)
            
        Returns:
            DataFrame with stock data
        """
        yf_symbol = self.get_yfinance_symbol(symbol)
        
        try:
            ticker = yf.Ticker(yf_symbol)
            data = ticker.history(start=start_date, end=end_date, interval=interval)
            
            if data.empty:
                # Try alternative symbol format
                alt_symbol = f"{symbol}.NS" if self.exchange == 'NSE' else f"{symbol}.BO"
                ticker = yf.Ticker(alt_symbol)
                data = ticker.history(start=start_date, end=end_date, interval=interval)
            
            return data
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return pd.DataFrame()
    
    def fetch_stock_info(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch stock information using yfinance.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with stock information
        """
        yf_symbol = self.get_yfinance_symbol(symbol)
        
        try:
            ticker = yf.Ticker(yf_symbol)
            info = ticker.info
            
            # Extract key information
            stock_info = {
                'symbol': symbol,
                'yfinance_symbol': yf_symbol,
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'current_price': info.get('currentPrice', 0),
                'previous_close': info.get('previousClose', 0),
                'open': info.get('open', 0),
                'high': info.get('dayHigh', 0),
                'low': info.get('dayLow', 0),
                'volume': info.get('volume', 0),
                '52_week_high': info.get('fiftyTwoWeekHigh', 0),
                '52_week_low': info.get('fiftyTwoWeekLow', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'beta': info.get('beta', 0)
            }
            
            return stock_info
        except Exception as e:
            print(f"Error fetching info for {symbol}: {e}")
            return {'symbol': symbol, 'error': str(e)}
    
    def fetch_multiple_stocks(self, symbols: List[str], start_date: str, 
                             end_date: str, interval: str = '1d') -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple stocks.
        
        Args:
            symbols: List of stock symbols
            start_date: Start date
            end_date: End date
            interval: Data interval
            
        Returns:
            Dictionary with symbol as key and DataFrame as value
        """
        data_dict = {}
        
        for symbol in symbols:
            data = self.fetch_stock_data(symbol, start_date, end_date, interval)
            if not data.empty:
                data_dict[symbol] = data
        
        return data_dict
    
    def get_nifty50_symbols(self) -> List[str]:
        """
        Get list of Nifty 50 symbols.
        
        Returns:
            List of Nifty 50 stock symbols
        """
        return list(NSE_SYMBOLS.keys())
    
    def get_sensex_symbols(self) -> List[str]:
        """
        Get list of Sensex symbols.
        
        Returns:
            List of Sensex stock symbols
        """
        return list(BSE_SYMBOLS.keys())


def fetch_indian_stock_data(symbol: str, start_date: str, end_date: str, 
                           exchange: str = 'NSE', interval: str = '1d') -> pd.DataFrame:
    """
    Convenience function to fetch Indian stock data.
    
    Args:
        symbol: Stock symbol
        start_date: Start date
        end_date: End date
        exchange: Exchange ('NSE' or 'BSE')
        interval: Data interval
        
    Returns:
        DataFrame with stock data
    """
    fetcher = IndianStockData(exchange)
    return fetcher.fetch_stock_data(symbol, start_date, end_date, interval)


def fetch_indian_stock_info(symbol: str, exchange: str = 'NSE') -> Dict[str, Any]:
    """
    Convenience function to fetch Indian stock information.
    
    Args:
        symbol: Stock symbol
        exchange: Exchange ('NSE' or 'BSE')
        
    Returns:
        Dictionary with stock information
    """
    fetcher = IndianStockData(exchange)
    return fetcher.fetch_stock_info(symbol)


def get_default_indian_stocks(exchange: str = 'NSE') -> List[str]:
    """
    Get default list of Indian stocks for dashboard.
    
    Args:
        exchange: Exchange ('NSE' or 'BSE')
        
    Returns:
        List of stock symbols
    """
    fetcher = IndianStockData(exchange)
    return fetcher.get_nifty50_symbols()[:10] if exchange == 'NSE' else fetcher.get_sensex_symbols()[:10]


# NSE API functions for additional data
def fetch_nse_index_data(index: str = 'NIFTY 50', start_date: str = None, 
                        end_date: str = None) -> pd.DataFrame:
    """
    Fetch NSE index data using yfinance.
    
    Args:
        index: Index name ('NIFTY 50', 'NIFTY BANK', etc.)
        start_date: Start date
        end_date: End date
        
    Returns:
        DataFrame with index data
    """
    index_symbols = {
        'NIFTY 50': '^NSEI',
        'NIFTY BANK': '^NSEBANK',
        'NIFTY IT': '^CNXIT',
        'NIFTY AUTO': '^CNXAUTO',
        'NIFTY FMCG': '^CNXFMCG',
        'NIFTY PHARMA': '^CNXPHARMA'
    }
    
    yf_symbol = index_symbols.get(index, '^NSEI')
    
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    try:
        ticker = yf.Ticker(yf_symbol)
        data = ticker.history(start=start_date, end=end_date, interval='1d')
        return data
    except Exception as e:
        print(f"Error fetching index data: {e}")
        return pd.DataFrame()


def fetch_nse_preopen_market() -> Dict[str, Any]:
    """
    Fetch NSE pre-open market data.
    
    Returns:
        Dictionary with pre-open market data
    """
    try:
        # NSE pre-open market API
        url = "https://www.nseindia.com/api/pre-open"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': f'API returned status code {response.status_code}'}
    except Exception as e:
        return {'error': str(e)}


def combine_yfinance_nse_data(symbol: str, start_date: str, end_date: str) -> Dict[str, Any]:
    """
    Combine data from yfinance and NSE API for comprehensive stock data.
    
    Args:
        symbol: Stock symbol
        start_date: Start date
        end_date: End date
        
    Returns:
        Combined stock data
    """
    # Fetch price data from yfinance
    fetcher = IndianStockData('NSE')
    price_data = fetcher.fetch_stock_data(symbol, start_date, end_date)
    
    # Fetch stock info from yfinance
    stock_info = fetcher.fetch_stock_info(symbol)
    
    # Try to fetch additional NSE data
    try:
        nse_data = fetch_nse_preopen_market()
    except:
        nse_data = {}
    
    return {
        'price_data': price_data,
        'stock_info': stock_info,
        'nse_data': nse_data
    }
