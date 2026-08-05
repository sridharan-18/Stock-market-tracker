import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import requests
import yfinance as yf

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions=True)

# API Base URL
API_BASE_URL = 'http://127.0.0.1:8000'

# Default stocks
DEFAULT_STOCKS = ['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'AMZN']

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
                                start_date=(datetime.now() - timedelta(days=30)).date(),
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
     Output('stock-details-table', 'children')],
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
        return "N/A", "N/A", "N/A", "N/A", go.Figure(), go.Figure(), go.Figure(), html.P("No stocks selected")
    
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
        return "N/A", "N/A", "N/A", "N/A", go.Figure(), go.Figure(), go.Figure(), html.P("No data available")
    
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
            
            portfolio_value += end_price
            total_gain += gain
            
            stock_metrics.append({
                'symbol': symbol,
                'start_price': start_price,
                'end_price': end_price,
                'gain': gain,
                'gain_pct': gain_pct,
                'volume': volume
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
    
    # Create details table
    table_rows = []
    for m in stock_metrics:
        table_rows.append(
            html.Tr([
                html.Td(m['symbol']),
                html.Td(f"${m['end_price']:.2f}"),
                html.Td(f"${m['gain']:.2f}"),
                html.Td(f"{m['gain_pct']:.2f}%", style={'color': 'green' if m['gain_pct'] >= 0 else 'red'}),
                html.Td(f"{m['volume']:,.0f}")
            ])
        )
    
    table = dbc.Table([
        html.Thead([
            html.Tr([
                html.Th("Symbol"),
                html.Th("Current Price"),
                html.Th("Gain/Loss"),
                html.Th("Change %"),
                html.Th("Avg Volume")
            ])
        ]),
        html.Tbody(table_rows)
    ], striped=True, bordered=True, hover=True, dark=True)
    
    return (
        f"${portfolio_value:.2f}",
        f"${total_gain:.2f}",
        f"{top_gainer['symbol']} ({top_gainer['gain_pct']:.2f}%)",
        f"{top_loser['symbol']} ({top_loser['gain_pct']:.2f}%)",
        price_fig,
        perf_fig,
        vol_fig,
        table
    )


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
