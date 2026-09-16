import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
import os
from indian_stocks import (
    IndianStockData,
    fetch_indian_stock_data,
    fetch_indian_stock_info,
    get_default_indian_stocks,
    fetch_nse_index_data,
    combine_yfinance_nse_data
)
from crypto_commodities import (
    CryptoData,
    CommodityData,
    MultiAssetData,
    fetch_crypto_data,
    fetch_commodity_data,
    get_default_crypto_symbols,
    get_default_commodity_symbols
)
from portfolio_tracker import PortfolioTracker

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions=True)

# Initialize portfolio tracker
portfolio_tracker = PortfolioTracker()

# Default stocks (mixed US and Indian)
DEFAULT_STOCKS = ['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'RELIANCE', 'TCS', 'HDFCBANK', 'INFY']

# Indian stocks for quick selection
INDIAN_STOCKS = ['RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK', 'HINDUNILVR', 'ITC', 'SBIN']

# Crypto symbols
CRYPTO_SYMBOLS = ['BTC', 'ETH']

# Commodity symbols
COMMODITY_SYMBOLS = ['GOLD', 'OIL']

# Exchange options
EXCHANGE_OPTIONS = [
    {'label': 'US Stocks (NYSE/NASDAQ)', 'value': 'US'},
    {'label': 'NSE (National Stock Exchange)', 'value': 'NSE'},
    {'label': 'BSE (Bombay Stock Exchange)', 'value': 'BSE'},
    {'label': 'Cryptocurrencies', 'value': 'CRYPTO'},
    {'label': 'Commodities', 'value': 'COMMODITY'}
]


# Technical Indicator Functions
def calculate_sma(data, period):
    """Calculate Simple Moving Average"""
    return data.rolling(window=period).mean()


def calculate_ema(data, period):
    """Calculate Exponential Moving Average"""
    return data.ewm(span=period, adjust=False).mean()


def calculate_rsi(data, period=14):
    """Calculate Relative Strength Index"""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_macd(data, fast=12, slow=26, signal=9):
    """Calculate MACD (Moving Average Convergence Divergence)"""
    ema_fast = calculate_ema(data, fast)
    ema_slow = calculate_ema(data, slow)
    macd_line = ema_fast - ema_slow
    signal_line = calculate_ema(macd_line, signal)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def calculate_bollinger_bands(data, period=20, std_dev=2):
    """Calculate Bollinger Bands"""
    sma = calculate_sma(data, period)
    std = data.rolling(window=period).std()
    upper_band = sma + (std * std_dev)
    lower_band = sma - (std * std_dev)
    return upper_band, sma, lower_band


def calculate_atr(high, low, close, period=14):
    """Calculate Average True Range (ATR)"""
    high_low = high - low
    high_close = np.abs(high - close.shift())
    low_close = np.abs(low - close.shift())
    
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window=period).mean()
    return atr


def calculate_historical_volatility(data, period=20, annualize=True):
    """Calculate Historical Volatility"""
    log_returns = np.log(data / data.shift(1))
    volatility = log_returns.rolling(window=period).std()
    
    if annualize:
        volatility = volatility * np.sqrt(252)  # Annualize (252 trading days)
    
    return volatility


def calculate_volatility_cone(data, periods=[30, 60, 90, 180]):
    """Calculate Volatility Cone for different time periods"""
    log_returns = np.log(data / data.shift(1)).dropna()
    volatilities = {}
    
    for period in periods:
        if len(log_returns) >= period:
            vol = log_returns.rolling(window=period).std() * np.sqrt(252)
            volatilities[f'{period}d'] = {
                'mean': vol.mean(),
                'std': vol.std(),
                'min': vol.min(),
                'max': vol.max(),
                'percentile_25': vol.quantile(0.25),
                'percentile_75': vol.quantile(0.75)
            }
    
    return volatilities

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Stock Market Dashboard", className="text-center mb-4"),
            html.Hr()
        ])
    ]),

    # Filters Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Filters", className="card-title"),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Exchange"),
                            dcc.Dropdown(
                                id='exchange',
                                options=EXCHANGE_OPTIONS,
                                value='US',
                                className='mb-2'
                            )
                        ], md=4),
                        dbc.Col([
                            html.Label("Stock Symbols (comma-separated)"),
                            dcc.Input(
                                id='stock-symbols',
                                type='text',
                                value=','.join(DEFAULT_STOCKS),
                                className='form-control mb-2'
                            )
                        ], md=4),
                        dbc.Col([
                            html.Label("Quick Select"),
                            dcc.Dropdown(
                                id='quick-select',
                                options=[
                                    {'label': 'US Tech Stocks', 'value': 'US_TECH'},
                                    {'label': 'Indian Nifty 50', 'value': 'NIFTY50'},
                                    {'label': 'Indian Top 8', 'value': 'INDIAN_TOP8'},
                                    {'label': 'Cryptocurrencies (BTC, ETH)', 'value': 'CRYPTO'},
                                    {'label': 'Commodities (Gold, Oil)', 'value': 'COMMODITY'}
                                ],
                                value=None,
                                placeholder='Select preset...',
                                className='mb-2'
                            )
                        ], md=4)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Date Range"),
                            dcc.DatePickerRange(
                                id='date-range',
                                start_date=(datetime.now() - timedelta(days=90)).date(),
                                end_date=datetime.now().date(),
                                className='mb-2'
                            )
                        ], md=4),
                        dbc.Col([
                            html.Label("Interval"),
                            dcc.Dropdown(
                                id='interval',
                                options=[
                                    {'label': 'Daily', 'value': '1d'},
                                    {'label': 'Weekly', 'value': '1wk'},
                                    {'label': 'Monthly', 'value': '1mo'}
                                ],
                                value='1d',
                                className='mb-2'
                            )
                        ], md=4),
                        dbc.Col([
                            html.Label(""),
                            dbc.Button("Apply Filters", id='apply-filters', color='primary', className='mt-2')
                        ], md=4)
                    ])
                ])
            ])
        ], className='mb-4')
    ]),

    # Performance Metrics
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Performance Metrics", className="card-title"),
                    dbc.Row([
                        dbc.Col([
                            html.H4(id='metric-portfolio-value', className="text-success"),
                            html.P("Portfolio Value", className="card-text text-muted")
                        ], md=3),
                        dbc.Col([
                            html.H4(id='metric-total-gain', className="text-info"),
                            html.P("Total Gain/Loss", className="card-text text-muted")
                        ], md=3),
                        dbc.Col([
                            html.H4(id='metric-top-gainer', className="text-success"),
                            html.P("Top Gainer", className="card-text text-muted")
                        ], md=3),
                        dbc.Col([
                            html.H4(id='metric-top-loser', className="text-danger"),
                            html.P("Top Loser", className="card-text text-muted")
                        ], md=3)
                    ])
                ])
            ])
        ], className='mb-4')
    ]),

    # Portfolio Tracking Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Portfolio Management", className="card-title"),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Symbol"),
                            dcc.Input(id='tx-symbol', type='text', placeholder='AAPL', className='form-control mb-2')
                        ], md=2),
                        dbc.Col([
                            html.Label("Action"),
                            dcc.Dropdown(
                                id='tx-action',
                                options=[{'label': 'Buy', 'value': 'buy'}, {'label': 'Sell', 'value': 'sell'}],
                                value='buy',
                                className='mb-2'
                            )
                        ], md=2),
                        dbc.Col([
                            html.Label("Quantity"),
                            dcc.Input(id='tx-quantity', type='number', placeholder='10', className='form-control mb-2')
                        ], md=2),
                        dbc.Col([
                            html.Label("Price"),
                            dcc.Input(id='tx-price', type='number', placeholder='150.00', className='form-control mb-2')
                        ], md=2),
                        dbc.Col([
                            html.Label("Asset Type"),
                            dcc.Dropdown(
                                id='tx-asset-type',
                                options=[
                                    {'label': 'Stock', 'value': 'stock'},
                                    {'label': 'Crypto', 'value': 'crypto'},
                                    {'label': 'Commodity', 'value': 'commodity'}
                                ],
                                value='stock',
                                className='mb-2'
                            )
                        ], md=2),
                        dbc.Col([
                            html.Label(""),
                            dbc.Button("Add Transaction", id='add-tx-btn', color='success', className='mt-2')
                        ], md=2)
                    ])
                ])
            ])
        ], className='mb-4')
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Current Holdings", className="card-title"),
                    html.Div(id='portfolio-holdings')
                ])
            ])
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Transaction History", className="card-title"),
                    html.Div(id='transaction-history')
                ])
            ])
        ], md=6)
    ], className='mb-4'),

    # Advanced Portfolio Metrics Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Advanced Portfolio Metrics", className="card-title"),
                    dbc.Row([
                        dbc.Col([
                            html.H4(id='metric-cagr', className="text-info"),
                            html.P("CAGR (%)", className="card-text text-muted")
                        ], md=3),
                        dbc.Col([
                            html.H4(id='metric-sharpe', className="text-warning"),
                            html.P("Sharpe Ratio", className="card-text text-muted")
                        ], md=3),
                        dbc.Col([
                            html.H4(id='metric-sortino', className="text-success"),
                            html.P("Sortino Ratio", className="card-text text-muted")
                        ], md=3),
                        dbc.Col([
                            html.H4(id='metric-drawdown', className="text-danger"),
                            html.P("Max Drawdown (%)", className="card-text text-muted")
                        ], md=3)
                    ])
                ])
            ])
        ], className='mb-4')
    ]),

    # Charts Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Price Comparison Chart", className="card-title"),
                    dcc.Graph(id='price-comparison-chart')
                ])
            ])
        ], md=12)
    ], className='mb-4'),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Performance Comparison", className="card-title"),
                    dcc.Graph(id='performance-bar-chart')
                ])
            ])
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Volume Comparison", className="card-title"),
                    dcc.Graph(id='volume-bar-chart')
                ])
            ])
        ], md=6)
    ], className='mb-4'),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Risk Metrics", className="card-title"),
                    dcc.Graph(id='risk-metrics-chart')
                ])
            ])
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Correlation Matrix", className="card-title"),
                    dcc.Graph(id='correlation-chart')
                ])
            ])
        ], md=6)
    ], className='mb-4'),

    # Technical Indicators Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Technical Indicators", className="card-title"),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Select Stock for Indicators"),
                            dcc.Dropdown(
                                id='indicator-stock',
                                options=[],
                                value=None,
                                className='mb-2'
                            )
                        ], md=6),
                        dbc.Col([
                            html.Label("Indicator Type"),
                            dcc.Dropdown(
                                id='indicator-type',
                                options=[
                                    {'label': 'Moving Averages (SMA/EMA)', 'value': 'ma'},
                                    {'label': 'RSI', 'value': 'rsi'},
                                    {'label': 'MACD', 'value': 'macd'},
                                    {'label': 'Bollinger Bands', 'value': 'bollinger'},
                                    {'label': 'ATR (Average True Range)', 'value': 'atr'},
                                    {'label': 'Historical Volatility', 'value': 'volatility'},
                                    {'label': 'Volatility Cone', 'value': 'volatility_cone'}
                                ],
                                value='ma',
                                className='mb-2'
                            )
                        ], md=6)
                    ])
                ])
            ])
        ], className='mb-4')
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Technical Analysis Chart", className="card-title"),
                    dcc.Graph(id='technical-indicators-chart')
                ])
            ])
        ], md=12)
    ], className='mb-4'),

    # Stock Details Table
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Stock Details", className="card-title"),
                    html.Div(id='stock-details-table')
                ])
            ])
        ])
    ]),

    dcc.Interval(
        id='interval-component',
        interval=15*1000,  # Update every 15 seconds
        n_intervals=0
    )
], fluid=True)


@app.callback(
    Output('stock-symbols', 'value'),
    [Input('quick-select', 'value'),
     Input('exchange', 'value')]
)
def update_stock_symbols(quick_select, exchange):
    """Update stock symbols based on quick select and exchange."""
    if quick_select == 'US_TECH':
        return ','.join(['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'NFLX'])
    elif quick_select == 'NIFTY50':
        fetcher = IndianStockData('NSE')
        return ','.join(fetcher.get_nifty50_symbols())
    elif quick_select == 'INDIAN_TOP8':
        return ','.join(INDIAN_STOCKS)
    elif quick_select == 'CRYPTO':
        return ','.join(CRYPTO_SYMBOLS)
    elif quick_select == 'COMMODITY':
        return ','.join(COMMODITY_SYMBOLS)
    elif exchange == 'NSE':
        return ','.join(get_default_indian_stocks('NSE'))
    elif exchange == 'BSE':
        return ','.join(get_default_indian_stocks('BSE'))
    elif exchange == 'CRYPTO':
        return ','.join(CRYPTO_SYMBOLS)
    elif exchange == 'COMMODITY':
        return ','.join(COMMODITY_SYMBOLS)
    else:
        return ','.join(DEFAULT_STOCKS)


@app.callback(
    [Output('metric-portfolio-value', 'children'),
     Output('metric-total-gain', 'children'),
     Output('metric-top-gainer', 'children'),
     Output('metric-top-loser', 'children'),
     Output('price-comparison-chart', 'figure'),
     Output('performance-bar-chart', 'figure'),
     Output('volume-bar-chart', 'figure'),
     Output('risk-metrics-chart', 'figure'),
     Output('correlation-chart', 'figure'),
     Output('stock-details-table', 'children'),
     Output('indicator-stock', 'options')],
    [Input('apply-filters', 'n_clicks'),
     Input('interval-component', 'n_intervals')],
    [State('stock-symbols', 'value'),
     State('date-range', 'start_date'),
     State('date-range', 'end_date'),
     State('interval', 'value'),
     State('exchange', 'value')]
)
def update_dashboard(n_clicks, n_intervals, symbols, start_date, end_date, interval, exchange):
    # Parse symbols
    symbol_list = [s.strip().upper() for s in symbols.split(',') if s.strip()]
    
    if not symbol_list:
        return "N/A", "N/A", "N/A", "N/A", go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure(), html.P("No stocks selected")
    
    # Fetch historical data for all stocks
    stock_data = {}
    
    for symbol in symbol_list:
        try:
            if exchange in ['NSE', 'BSE']:
                # Use Indian stock data fetcher
                data = fetch_indian_stock_data(symbol, start_date, end_date, exchange, interval)
                if not data.empty:
                    stock_data[symbol] = data
            elif exchange == 'CRYPTO':
                # Use crypto data fetcher
                data = fetch_crypto_data(symbol, start_date, end_date, interval)
                if not data.empty:
                    stock_data[symbol] = data
            elif exchange == 'COMMODITY':
                # Use commodity data fetcher
                data = fetch_commodity_data(symbol, start_date, end_date, interval)
                if not data.empty:
                    stock_data[symbol] = data
            else:
                # Use yfinance for US stocks
                ticker = yf.Ticker(symbol)
                hist = ticker.history(start=start_date, end=end_date, interval=interval)
                if not hist.empty:
                    stock_data[symbol] = hist
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
    
    if not stock_data:
        return "N/A", "N/A", "N/A", "N/A", go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure(), html.P("No data available")
    
    # Calculate metrics
    portfolio_value = 0
    total_gain = 0
    stock_metrics = []
    
    for symbol, data in stock_data.items():
        if not data.empty:
            start_price = data['Close'].iloc[0]
            end_price = data['Close'].iloc[-1]
            gain = end_price - start_price
            gain_pct = (gain / start_price) * 100
            volume = data['Volume'].mean()
            
            # Calculate risk metrics
            returns = data['Close'].pct_change().dropna()
            volatility = returns.std() * np.sqrt(252)  # Annualized volatility
            sharpe_ratio = (returns.mean() * 252) / (returns.std() * np.sqrt(252)) if returns.std() > 0 else 0
            
            portfolio_value += end_price
            total_gain += gain
            
            stock_metrics.append({
                'symbol': symbol,
                'start_price': start_price,
                'end_price': end_price,
                'gain': gain,
                'gain_pct': gain_pct,
                'volume': volume,
                'volatility': volatility,
                'sharpe_ratio': sharpe_ratio,
                'returns': returns
            })
    
    # Find top gainer and loser
    if stock_metrics:
        top_gainer = max(stock_metrics, key=lambda x: x['gain_pct'])
        top_loser = min(stock_metrics, key=lambda x: x['gain_pct'])
    else:
        top_gainer = {'symbol': 'N/A', 'gain_pct': 0}
        top_loser = {'symbol': 'N/A', 'gain_pct': 0}
    
    # Create price comparison chart
    price_fig = go.Figure()
    for symbol, data in stock_data.items():
        price_fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            name=symbol,
            mode='lines'
        ))
    price_fig.update_layout(
        title="Stock Price Comparison",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        template='plotly_dark',
        hovermode='x unified'
    )
    
    # Create performance bar chart
    perf_fig = go.Figure(data=[
        go.Bar(
            x=[m['symbol'] for m in stock_metrics],
            y=[m['gain_pct'] for m in stock_metrics],
            marker_color=['green' if m['gain_pct'] >= 0 else 'red' for m in stock_metrics]
        )
    ])
    perf_fig.update_layout(
        title="Performance (%)",
        xaxis_title="Stock",
        yaxis_title="Gain/Loss %",
        template='plotly_dark'
    )
    
    # Create volume bar chart
    vol_fig = go.Figure(data=[
        go.Bar(
            x=[m['symbol'] for m in stock_metrics],
            y=[m['volume'] for m in stock_metrics]
        )
    ])
    vol_fig.update_layout(
        title="Average Volume",
        xaxis_title="Stock",
        yaxis_title="Volume",
        template='plotly_dark'
    )
    
    # Create risk metrics chart
    risk_fig = go.Figure(data=[
        go.Bar(
            name='Volatility',
            x=[m['symbol'] for m in stock_metrics],
            y=[m['volatility'] for m in stock_metrics]
        ),
        go.Bar(
            name='Sharpe Ratio',
            x=[m['symbol'] for m in stock_metrics],
            y=[m['sharpe_ratio'] for m in stock_metrics]
        )
    ])
    risk_fig.update_layout(
        title="Risk Metrics",
        xaxis_title="Stock",
        yaxis_title="Value",
        template='plotly_dark',
        barmode='group'
    )
    
    # Create correlation matrix
    if len(stock_metrics) > 1:
        returns_df = pd.DataFrame({m['symbol']: m['returns'] for m in stock_metrics})
        correlation_matrix = returns_df.corr()
        
        corr_fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale='RdBu',
            zmid=0
        ))
        corr_fig.update_layout(
            title="Correlation Matrix",
            template='plotly_dark'
        )
    else:
        corr_fig = go.Figure()
        corr_fig.update_layout(
            title="Correlation Matrix (Need at least 2 stocks)",
            template='plotly_dark'
        )
    
    # Create details table
    table_rows = []
    for m in stock_metrics:
        table_rows.append(
            html.Tr([
                html.Td(m['symbol']),
                html.Td(f"${m['end_price']:.2f}"),
                html.Td(f"${m['gain']:.2f}"),
                html.Td(f"{m['gain_pct']:.2f}%", style={'color': 'green' if m['gain_pct'] >= 0 else 'red'}),
                html.Td(f"{m['volume']:,.0f}"),
                html.Td(f"{m['volatility']:.2f}"),
                html.Td(f"{m['sharpe_ratio']:.2f}")
            ])
        )
    
    table = dbc.Table([
        html.Thead([
            html.Tr([
                html.Th("Symbol"),
                html.Th("Current Price"),
                html.Th("Gain/Loss"),
                html.Th("Change %"),
                html.Th("Avg Volume"),
                html.Th("Volatility"),
                html.Th("Sharpe Ratio")
            ])
        ]),
        html.Tbody(table_rows)
    ], striped=True, bordered=True, hover=True, dark=True)
    
    # Create dropdown options for indicator stock selection
    indicator_options = [{'label': symbol, 'value': symbol} for symbol in symbol_list]
    
    return (
        f"${portfolio_value:.2f}",
        f"${total_gain:.2f}",
        f"{top_gainer['symbol']} ({top_gainer['gain_pct']:.2f}%)",
        f"{top_loser['symbol']} ({top_loser['gain_pct']:.2f}%)",
        price_fig,
        perf_fig,
        vol_fig,
        risk_fig,
        corr_fig,
        table,
        indicator_options
    )


@app.callback(
    Output('technical-indicators-chart', 'figure'),
    [Input('indicator-stock', 'value'),
     Input('indicator-type', 'value')],
    [State('stock-symbols', 'value'),
     State('date-range', 'start_date'),
     State('date-range', 'end_date'),
     State('interval', 'value')]
)
def update_technical_indicators(selected_stock, indicator_type, symbols, start_date, end_date, interval):
    if not selected_stock:
        return go.Figure()
    
    try:
        ticker = yf.Ticker(selected_stock)
        data = ticker.history(start=start_date, end=end_date, interval=interval)
        
        if data.empty:
            return go.Figure()
        
        fig = go.Figure()
        
        if indicator_type == 'ma':
            # Moving Averages
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['Close'],
                name='Price',
                mode='lines',
                line=dict(color='white')
            ))
            
            sma_20 = calculate_sma(data['Close'], 20)
            sma_50 = calculate_sma(data['Close'], 50)
            ema_20 = calculate_ema(data['Close'], 20)
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=sma_20,
                name='SMA 20',
                mode='lines',
                line=dict(color='blue')
            ))
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=sma_50,
                name='SMA 50',
                mode='lines',
                line=dict(color='orange')
            ))
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=ema_20,
                name='EMA 20',
                mode='lines',
                line=dict(color='green')
            ))
            
            fig.update_layout(
                title=f"{selected_stock} - Moving Averages",
                xaxis_title="Date",
                yaxis_title="Price",
                template='plotly_dark'
            )
            
        elif indicator_type == 'rsi':
            # RSI
            rsi = calculate_rsi(data['Close'])
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=rsi,
                name='RSI',
                mode='lines',
                line=dict(color='cyan')
            ))
            
            fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
            fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
            
            fig.update_layout(
                title=f"{selected_stock} - RSI (14)",
                xaxis_title="Date",
                yaxis_title="RSI",
                template='plotly_dark',
                yaxis=dict(range=[0, 100])
            )
            
        elif indicator_type == 'macd':
            # MACD
            macd_line, signal_line, histogram = calculate_macd(data['Close'])
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=macd_line,
                name='MACD Line',
                mode='lines',
                line=dict(color='blue')
            ))
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=signal_line,
                name='Signal Line',
                mode='lines',
                line=dict(color='orange')
            ))
            
            fig.add_trace(go.Bar(
                x=data.index,
                y=histogram,
                name='Histogram',
                marker_color=['green' if h > 0 else 'red' for h in histogram]
            ))
            
            fig.update_layout(
                title=f"{selected_stock} - MACD",
                xaxis_title="Date",
                yaxis_title="Value",
                template='plotly_dark'
            )
            
        elif indicator_type == 'bollinger':
            # Bollinger Bands
            upper_band, sma, lower_band = calculate_bollinger_bands(data['Close'])
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['Close'],
                name='Price',
                mode='lines',
                line=dict(color='white')
            ))
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=upper_band,
                name='Upper Band',
                mode='lines',
                line=dict(color='red', dash='dash')
            ))
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=sma,
                name='SMA 20',
                mode='lines',
                line=dict(color='blue')
            ))
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=lower_band,
                name='Lower Band',
                mode='lines',
                line=dict(color='green', dash='dash'),
                fill='tonexty',
                fillcolor='rgba(0, 255, 0, 0.1)'
            ))
            
            fig.update_layout(
                title=f"{selected_stock} - Bollinger Bands",
                xaxis_title="Date",
                yaxis_title="Price",
                template='plotly_dark'
            )
        
        elif indicator_type == 'atr':
            # ATR (Average True Range)
            atr = calculate_atr(data['High'], data['Low'], data['Close'])
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['Close'],
                name='Price',
                mode='lines',
                line=dict(color='white'),
                yaxis='y1'
            ))
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=atr,
                name='ATR (14)',
                mode='lines',
                line=dict(color='orange'),
                yaxis='y2'
            ))
            
            fig.update_layout(
                title=f"{selected_stock} - Average True Range (ATR)",
                xaxis_title="Date",
                yaxis_title="Price",
                yaxis2=dict(
                    title="ATR",
                    overlaying='y',
                    side='right',
                    showgrid=False
                ),
                template='plotly_dark'
            )
            
        elif indicator_type == 'volatility':
            # Historical Volatility
            hist_vol = calculate_historical_volatility(data['Close'])
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=hist_vol,
                name='Historical Volatility (20d)',
                mode='lines',
                line=dict(color='purple')
            ))
            
            fig.add_hline(y=hist_vol.mean(), line_dash="dash", line_color="white", 
                         annotation_text=f"Avg: {hist_vol.mean():.2f}%")
            
            fig.update_layout(
                title=f"{selected_stock} - Historical Volatility (20-day, Annualized)",
                xaxis_title="Date",
                yaxis_title="Volatility (%)",
                template='plotly_dark'
            )
            
        elif indicator_type == 'volatility_cone':
            # Volatility Cone
            vol_cone = calculate_volatility_cone(data['Close'])
            
            if vol_cone:
                periods = list(vol_cone.keys())
                means = [vol_cone[p]['mean'] * 100 for p in periods]
                mins = [vol_cone[p]['min'] * 100 for p in periods]
                maxs = [vol_cone[p]['max'] * 100 for p in periods]
                p25 = [vol_cone[p]['percentile_25'] * 100 for p in periods]
                p75 = [vol_cone[p]['percentile_75'] * 100 for p in periods]
                
                fig.add_trace(go.Scatter(
                    x=periods,
                    y=means,
                    name='Mean',
                    mode='lines+markers',
                    line=dict(color='white')
                ))
                
                fig.add_trace(go.Scatter(
                    x=periods,
                    y=maxs,
                    name='Max',
                    mode='lines+markers',
                    line=dict(color='red')
                ))
                
                fig.add_trace(go.Scatter(
                    x=periods,
                    y=mins,
                    name='Min',
                    mode='lines+markers',
                    line=dict(color='green')
                ))
                
                fig.add_trace(go.Scatter(
                    x=periods,
                    y=p75,
                    name='75th Percentile',
                    mode='lines+markers',
                    line=dict(color='orange', dash='dash')
                ))
                
                fig.add_trace(go.Scatter(
                    x=periods,
                    y=p25,
                    name='25th Percentile',
                    mode='lines+markers',
                    line=dict(color='cyan', dash='dash')
                ))
                
                fig.update_layout(
                    title=f"{selected_stock} - Volatility Cone",
                    xaxis_title="Period",
                    yaxis_title="Volatility (%)",
                    template='plotly_dark'
                )
            else:
                fig.update_layout(
                    title="Insufficient data for Volatility Cone",
                    template='plotly_dark'
                )
        
        return fig
        
    except Exception as e:
        print(f"Error generating technical indicators: {e}")
        return fig


# Portfolio Tracking Callbacks

@app.callback(
    [Output('portfolio-holdings', 'children'),
     Output('transaction-history', 'children'),
     Output('metric-cagr', 'children'),
     Output('metric-sharpe', 'children'),
     Output('metric-sortino', 'children'),
     Output('metric-drawdown', 'children')],
    [Input('add-tx-btn', 'n_clicks'),
     Input('interval-component', 'n_intervals')],
    [State('tx-symbol', 'value'),
     State('tx-action', 'value'),
     State('tx-quantity', 'value'),
     State('tx-price', 'value'),
     State('tx-asset-type', 'value')]
)
def update_portfolio(n_clicks, n_intervals, symbol, action, quantity, price, asset_type):
    """Update portfolio display and handle new transactions."""
    
    # Add transaction if button clicked and all fields provided
    if n_clicks and n_clicks > 0 and symbol and action and quantity and price:
        try:
            portfolio_tracker.add_transaction(
                symbol=symbol,
                action=action,
                quantity=float(quantity),
                price=float(price),
                asset_type=asset_type
            )
        except Exception as e:
            print(f"Error adding transaction: {e}")
    
    # Get current holdings
    holdings = portfolio_tracker.get_holdings()
    
    # Create holdings table
    if holdings:
        holdings_rows = []
        for symbol, data in holdings.items():
            holdings_rows.append(
                html.Tr([
                    html.Td(symbol),
                    html.Td(f"{data['quantity']:.4f}"),
                    html.Td(f"${data['avg_buy_price']:.2f}"),
                    html.Td(f"${data['total_invested']:.2f}"),
                    html.Td(f"${data['realized_gain_loss']:.2f}"),
                    html.Td(data['asset_type'].capitalize())
                ])
            )
        
        holdings_table = dbc.Table([
            html.Thead([
                html.Tr([
                    html.Th("Symbol"),
                    html.Th("Quantity"),
                    html.Th("Avg Buy Price"),
                    html.Th("Total Invested"),
                    html.Th("Realized Gain/Loss"),
                    html.Th("Type")
                ])
            ]),
            html.Tbody(holdings_rows)
        ], striped=True, bordered=True, hover=True, dark=True, size='sm')
    else:
        holdings_table = html.P("No holdings yet. Add transactions to build your portfolio.", className="text-muted")
    
    # Get transaction history
    transactions = portfolio_tracker.get_transactions()
    
    if transactions:
        tx_rows = []
        for tx in transactions[-10:]:  # Show last 10 transactions
            tx_rows.append(
                html.Tr([
                    html.Td(tx['date']),
                    html.Td(tx['symbol']),
                    html.Td(tx['action'].capitalize()),
                    html.Td(f"{tx['quantity']:.4f}"),
                    html.Td(f"${tx['price']:.2f}"),
                    html.Td(f"${tx['total']:.2f}"),
                    html.Td(tx['asset_type'].capitalize())
                ])
            )
        
        tx_table = dbc.Table([
            html.Thead([
                html.Tr([
                    html.Th("Date"),
                    html.Th("Symbol"),
                    html.Th("Action"),
                    html.Th("Quantity"),
                    html.Th("Price"),
                    html.Th("Total"),
                    html.Th("Type")
                ])
            ]),
            html.Tbody(tx_rows)
        ], striped=True, bordered=True, hover=True, dark=True, size='sm')
    else:
        tx_table = html.P("No transactions yet.", className="text-muted")
    
    # Calculate advanced metrics
    cagr_text = "N/A"
    sharpe_text = "N/A"
    sortino_text = "N/A"
    drawdown_text = "N/A"
    
    if holdings:
        try:
            # Fetch current prices for holdings
            current_prices = {}
            for symbol in holdings.keys():
                try:
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    current_prices[symbol] = info.get('currentPrice', 0)
                except:
                    current_prices[symbol] = 0
            
            # Get advanced metrics
            advanced_metrics = portfolio_tracker.get_advanced_metrics(current_prices)
            
            cagr_text = f"{advanced_metrics.get('cagr', 0):.2f}%"
            sharpe_text = f"{advanced_metrics.get('sharpe_ratio', 0):.2f}"
            sortino_text = f"{advanced_metrics.get('sortino_ratio', 0):.2f}"
            drawdown_text = f"{advanced_metrics.get('max_drawdown_pct', 0):.2f}%"
        except Exception as e:
            print(f"Error calculating advanced metrics: {e}")
    
    return holdings_table, tx_table, cagr_text, sharpe_text, sortino_text, drawdown_text


if __name__ == '__main__':
    # For local development
    debug_mode = os.environ.get('DASH_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 8050))
    app.run_server(debug=debug_mode, port=port)
