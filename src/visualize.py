"""
Visualization module for stock market data.
Provides functions to create charts and visualizations.
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any


def create_candlestick_chart(data: List[Dict[str, Any]], show_ma: bool = True, show_volume: bool = True) -> go.Figure:
    """
    Create a candlestick chart with optional moving averages and volume.
    
    Args:
        data: List of OHLCV data points
        show_ma: Whether to show moving averages
        show_volume: Whether to show volume chart
        
    Returns:
        Plotly Figure object
    """
    timestamps = [d['timestamp'] * 1000 for d in data]  # Convert to milliseconds
    opens = [d['open'] for d in data]
    highs = [d['high'] for d in data]
    lows = [d['low'] for d in data]
    closes = [d['close'] for d in data]
    volumes = [d['volume'] for d in data]
    
    traces = []
    
    # Candlestick trace
    candlestick = go.Candlestick(
        x=timestamps,
        open=opens,
        high=highs,
        low=lows,
        close=closes,
        name='Price',
        increasing_line_color='#10b981',
        decreasing_line_color='#ef4444'
    )
    traces.append(candlestick)
    
    # Moving averages
    if show_ma:
        ma20 = calculate_moving_average(closes, 20)
        ma50 = calculate_moving_average(closes, 50)
        
        if ma20:
            traces.append(go.Scatter(
                x=timestamps,
                y=ma20,
                mode='lines',
                name='MA 20',
                line=dict(color='#3b82f6', width=1.5)
            ))
        
        if ma50:
            traces.append(go.Scatter(
                x=timestamps,
                y=ma50,
                mode='lines',
                name='MA 50',
                line=dict(color='#f59e0b', width=1.5)
            ))
    
    # Volume
    if show_volume:
        colors = ['#10b981' if closes[i] >= opens[i] else '#ef4444' 
                  for i in range(len(closes))]
        
        traces.append(go.Bar(
            x=timestamps,
            y=volumes,
            name='Volume',
            marker_color=colors,
            yaxis='y2',
            opacity=0.7
        ))
    
    layout = go.Layout(
        title='',
        xaxis=dict(
            rangeslider=dict(visible=False),
            type='date',
            gridcolor='#334155'
        ),
        yaxis=dict(
            title='Price',
            gridcolor='#334155',
            side='left'
        ),
        yaxis2=dict(
            title='Volume',
            overlaying='y',
            side='right',
            showgrid=False,
            visible=show_volume
        ),
        plot_bgcolor='#1e293b',
        paper_bgcolor='#1e293b',
        font=dict(color='#f1f5f9'),
        margin=dict(l=60, r=60, t=30, b=60),
        legend=dict(
            x=0,
            y=1,
            bgcolor='rgba(30, 41, 59, 0.8)',
            bordercolor='#334155',
            borderwidth=1
        ),
        dragmode='zoom',
        showlegend=True
    )
    
    return go.Figure(data=traces, layout=layout)


def calculate_moving_average(prices: List[float], period: int) -> List[float]:
    """
    Calculate simple moving average.
    
    Args:
        prices: List of prices
        period: Period for moving average
        
    Returns:
        List of moving average values (with None for insufficient data)
    """
    ma = []
    for i in range(len(prices)):
        if i < period - 1:
            ma.append(None)
        else:
            avg = sum(prices[i - period + 1:i + 1]) / period
            ma.append(avg)
    return ma


def create_portfolio_chart(history: List[Dict[str, Any]]) -> go.Figure:
    """
    Create portfolio value history chart.
    
    Args:
        history: List of {timestamp, value} dictionaries
        
    Returns:
        Plotly Figure object
    """
    timestamps = [h['timestamp'] for h in history]
    values = [h['value'] for h in history]
    
    trace = go.Scatter(
        x=timestamps,
        y=values,
        mode='lines',
        fill='tozeroy',
        name='Portfolio Value',
        line=dict(color='#3b82f6', width=2)
    )
    
    layout = go.Layout(
        title='',
        xaxis=dict(
            type='date',
            gridcolor='#334155',
            showgrid=True
        ),
        yaxis=dict(
            title='Portfolio Value ($)',
            gridcolor='#334155',
            showgrid=True
        ),
        plot_bgcolor='transparent',
        paper_bgcolor='transparent',
        font=dict(color='#f1f5f9'),
        margin=dict(l=60, r=20, t=20, b=40),
        showlegend=False,
        hovermode='x unified'
    )
    
    return go.Figure(data=[trace], layout=layout)


def create_performance_comparison(stocks: List[Dict[str, Any]]) -> go.Figure:
    """
    Create performance comparison bar chart.
    
    Args:
        stocks: List of stock data with gain_pct
        
    Returns:
        Plotly Figure object
    """
    symbols = [s['symbol'] for s in stocks]
    gains = [s['gain_pct'] for s in stocks]
    colors = ['green' if g >= 0 else 'red' for g in gains]
    
    trace = go.Bar(
        x=symbols,
        y=gains,
        marker_color=colors
    )
    
    layout = go.Layout(
        title='Performance (%)',
        xaxis_title='Stock',
        yaxis_title='Gain/Loss %',
        template='plotly_dark'
    )
    
    return go.Figure(data=[trace], layout=layout)
