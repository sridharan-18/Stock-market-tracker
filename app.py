import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions=True)

# Default stocks
DEFAULT_STOCKS = ['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'NFLX']


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
                            html.Label("Stock Symbols (comma-separated)"),
                            dcc.Input(
                                id='stock-symbols',
                                type='text',
                                value=','.join(DEFAULT_STOCKS),
                                className='form-control mb-2'
                            )
                        ], md=4),
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
                        ], md=4)
                    ]),
                    dbc.Button("Apply Filters", id='apply-filters', color='primary', className='mt-2')
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
                                    {'label': 'Bollinger Bands', 'value': 'bollinger'}
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
     State('interval', 'value')]
)
def update_dashboard(n_clicks, n_intervals, symbols, start_date, end_date, interval):
    # Parse symbols
    symbol_list = [s.strip().upper() for s in symbols.split(',') if s.strip()]
    
    if not symbol_list:
        return "N/A", "N/A", "N/A", "N/A", go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure(), html.P("No stocks selected")
    
    # Fetch historical data for all stocks
    stock_data = {}
    for symbol in symbol_list:
        try:
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
        
        return fig
        
    except Exception as e:
        print(f"Error generating technical indicators: {e}")
        return go.Figure()


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
