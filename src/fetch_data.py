import json
import os
from typing import Optional
from urllib.parse import unquote
from urllib.request import Request, urlopen

from urllib.error import HTTPError, URLError


DEFAULT_SYMBOLS = {
    'AAPL': 'AAPL',
    'APPLE INC': 'AAPL',
    'TSLA': 'TSLA',
    'TESLA': 'TSLA',
    'GOOGL': 'GOOGL',
    'MSFT': 'MSFT',
    'AMZN': 'AMZN',
    'META': 'META',
    'NVDA': 'NVDA',
    'NFLX': 'NFLX',
    'KPR MILL LTD': 'KPRMILL.NS',
    'KPR MILL': 'KPRMILL.NS',
    'KPRMILL': 'KPRMILL.NS',
}


def normalize_symbol(symbol: str) -> str:
    cleaned = (symbol or '').strip().upper()
    if not cleaned:
        return ''
    if cleaned in DEFAULT_SYMBOLS:
        return DEFAULT_SYMBOLS[cleaned]
    if '.' in cleaned:
        return cleaned
    if cleaned.isalnum() and len(cleaned) <= 5:
        return cleaned
    lookup = cleaned.replace(' ', '')
    if lookup in DEFAULT_SYMBOLS:
        return DEFAULT_SYMBOLS[lookup]
    return cleaned


def build_yahoo_url(symbol: str, interval: str = '1m', range: str = '1d') -> str:
    ticker = normalize_symbol(symbol)
    return f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval={interval}&range={range}'


def fetch_quote(symbol: str) -> Optional[dict]:
    ticker = normalize_symbol(symbol)
    if not ticker:
        return None

    url = build_yahoo_url(ticker)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urlopen(req, timeout=12) as response:
            payload = json.load(response)
    except (HTTPError, URLError, TimeoutError, ValueError):
        return None

    if not payload.get('chart', {}).get('result'):
        return None

    result = payload['chart']['result'][0]
    meta = result.get('meta', {})
    timestamps = result.get('timestamp', [])
    indicators = result.get('indicators', {}).get('quote', [{}])[0]

    close_prices = indicators.get('close') or []
    if not timestamps or not close_prices:
        return None

    latest_close = close_prices[-1]
    previous_close = close_prices[-2] if len(close_prices) > 1 else latest_close
    change = latest_close - previous_close if previous_close else 0
    change_percent = (change / previous_close * 100) if previous_close else 0

    return {
        'symbol': meta.get('symbol', ticker),
        'name': meta.get('shortName') or meta.get('symbol', ticker),
        'price': round(float(latest_close), 2),
        'change': round(float(change), 2),
        'changePercent': round(float(change_percent), 2),
    }


def fetch_historical_data(symbol: str, interval: str = '1d', range: str = '1mo') -> Optional[dict]:
    ticker = normalize_symbol(symbol)
    if not ticker:
        return None

    url = build_yahoo_url(ticker, interval, range)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urlopen(req, timeout=12) as response:
            payload = json.load(response)
    except (HTTPError, URLError, TimeoutError, ValueError):
        return None

    if not payload.get('chart', {}).get('result'):
        return None

    result = payload['chart']['result'][0]
    meta = result.get('meta', {})
    timestamps = result.get('timestamp', [])
    indicators = result.get('indicators', {}).get('quote', [{}])[0]

    open_prices = indicators.get('open') or []
    high_prices = indicators.get('high') or []
    low_prices = indicators.get('low') or []
    close_prices = indicators.get('close') or []
    volumes = indicators.get('volume') or []

    if not timestamps or not close_prices:
        return None

    ohlcv_data = []
    for i in range(len(timestamps)):
        if (i < len(open_prices) and i < len(high_prices) and 
            i < len(low_prices) and i < len(close_prices) and i < len(volumes)):
            ohlcv_data.append({
                'timestamp': timestamps[i],
                'open': open_prices[i],
                'high': high_prices[i],
                'low': low_prices[i],
                'close': close_prices[i],
                'volume': volumes[i]
            })

    return {
        'symbol': meta.get('symbol', ticker),
        'name': meta.get('shortName') or meta.get('symbol', ticker),
        'data': ohlcv_data
    }


def serve_quote(symbol: str) -> dict:
    quote = fetch_quote(symbol)
    if quote:
        return {'ok': True, 'quote': quote}
    return {'ok': False, 'error': 'Unable to fetch live quote for the requested symbol'}


def serve_historical(symbol: str, interval: str = '1d', range: str = '1mo') -> dict:
    data = fetch_historical_data(symbol, interval, range)
    if data:
        return {'ok': True, 'data': data}
    return {'ok': False, 'error': 'Unable to fetch historical data for the requested symbol'}


if __name__ == '__main__':
    import sys

    from http.server import BaseHTTPRequestHandler, HTTPServer

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = self.path.split('?', 1)
            path = parsed[0]
            query = {}
            if len(parsed) > 1:
                for item in parsed[1].split('&'):
                    if '=' in item:
                        key, value = item.split('=', 1)
                        query[key] = unquote(value)

            if path == '/quote':
                symbol = query.get('symbol', '')
                response = serve_quote(symbol)
                body = json.dumps(response).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(body)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(body)
                return

            if path == '/historical':
                symbol = query.get('symbol', '')
                interval = query.get('interval', '1d')
                range = query.get('range', '1mo')
                response = serve_historical(symbol, interval, range)
                body = json.dumps(response).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(body)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(body)
                return

            self.send_response(404)
            self.end_headers()

    port = int(os.environ.get('PORT', '8000'))
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f'Serving on http://127.0.0.1:{port}')
    server.serve_forever()
