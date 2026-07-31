# Stock Market Dashboard

An interactive web application for analyzing and comparing stock performance using Dash and Plotly.

## Features

- **Interactive Dashboard**: Built with Dash and Plotly for real-time data visualization
- **Multi-Market Support**: US Stocks (NYSE/NASDAQ), NSE (India), BSE (India)
- **Exchange Selection**: Switch between US, NSE, and BSE exchanges
- **Quick Stock Presets**: Pre-configured stock lists (US Tech, Nifty 50, Indian Top 8)
- **Date Range Filter**: Select custom date ranges for analysis (daily, weekly, monthly intervals)
- **Stock Comparison**: Compare multiple stocks side by side
- **Performance Metrics**: Real-time portfolio value, gains/losses, top performers
- **Price Comparison Chart**: Interactive line chart comparing stock prices
- **Performance Bar Chart**: Visual comparison of percentage gains/losses
- **Volume Comparison**: Average trading volume comparison
- **Risk Metrics**: Volatility and Sharpe ratio analysis
- **Correlation Matrix**: Heatmap showing stock correlations
- **Stock Details Table**: Detailed breakdown of all tracked stocks
- **Auto-refresh**: Dashboard updates every 15 seconds
- **Dark Theme**: Professional dark theme with Bootstrap

### 📊 Advanced Analytics

- **Moving Averages (SMA)**: Simple Moving Average with 20 and 50 periods
- **Moving Averages (EMA)**: Exponential Moving Average with 20 periods
- **RSI Indicator**: Relative Strength Index with overbought/oversold levels (70/30)
- **MACD Indicator**: Moving Average Convergence Divergence with signal line and histogram
- **Bollinger Bands**: Volatility bands with upper/lower bands and SMA
- **ATR (Average True Range)**: Measure of volatility considering price ranges
- **Historical Volatility**: Rolling standard deviation of returns (annualized)
- **Volatility Cone**: Volatility distribution across different time periods
- **Technical Analysis Charts**: Interactive charts for all technical indicators

### 🇮🇳 Indian Stock Market Integration

- **NSE (National Stock Exchange)**: Full support for NSE-listed stocks
- **BSE (Bombay Stock Exchange)**: Full support for BSE-listed stocks
- **Nifty 50 Stocks**: Pre-configured list of Nifty 50 constituents
- **Sensex Stocks**: Pre-configured list of Sensex constituents
- **Symbol Mapping**: Automatic conversion to yfinance format (.NS/.BO)
- **Combined Data Sources**: yfinance integration with NSE/BSE API support
- **Index Data**: Support for NSE indices (Nifty 50, Nifty Bank, Nifty IT, etc.)
- **Pre-open Market**: NSE pre-open market data integration

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sridharan-18/Stock-Dashboard.git
cd Stock-Dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the dashboard:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://127.0.0.1:8050
```

## Dashboard Features

### Filters
- **Stock Symbols**: Enter comma-separated stock symbols (e.g., AAPL,TSLA,MSFT)
- **Date Range**: Select start and end dates for analysis
- **Interval**: Choose between Daily, Weekly, or Monthly data

### Performance Metrics
- **Portfolio Value**: Total value of all tracked stocks
- **Total Gain/Loss**: Combined gains/losses across all stocks
- **Top Gainer**: Stock with the highest percentage gain
- **Top Loser**: Stock with the highest percentage loss

### Charts
- **Price Comparison Chart**: Line chart showing price trends over time
- **Performance Comparison**: Bar chart showing percentage gains/losses
- **Volume Comparison**: Bar chart showing average trading volume
- **Risk Metrics**: Grouped bar chart showing volatility and Sharpe ratio
- **Correlation Matrix**: Heatmap showing correlations between stocks
- **Technical Indicators**: Interactive charts for SMA, EMA, RSI, MACD, and Bollinger Bands

### Stock Details Table
- Symbol
- Current Price
- Gain/Loss
- Change %
- Average Volume
- Volatility (annualized)
- Sharpe Ratio

## Default Stocks

The dashboard comes pre-configured with these popular stocks:
- AAPL (Apple)
- TSLA (Tesla)
- MSFT (Microsoft)
- GOOGL (Alphabet)
- AMZN (Amazon)
- NVDA (NVIDIA)
- META (Meta)
- NFLX (Netflix)

## Risk Metrics Explained

- **Volatility**: Annualized standard deviation of returns (higher = more risk)
- **Sharpe Ratio**: Risk-adjusted return (higher = better risk-adjusted performance)

## Technical Indicators Explained

### Moving Averages (SMA/EMA)
- **SMA (Simple Moving Average)**: Average price over a specified period (20, 50 days)
- **EMA (Exponential Moving Average)**: Weighted average giving more importance to recent prices
- **Usage**: Identify trends and potential support/resistance levels

### RSI (Relative Strength Index)
- **Range**: 0-100
- **Overbought**: Above 70 (potential sell signal)
- **Oversold**: Below 30 (potential buy signal)
- **Usage**: Identify overbought/oversold conditions

### MACD (Moving Average Convergence Divergence)
- **MACD Line**: Fast EMA (12) - Slow EMA (26)
- **Signal Line**: EMA of MACD line (9)
- **Histogram**: MACD Line - Signal Line
- **Usage**: Identify trend changes and momentum

### Bollinger Bands
- **Upper Band**: SMA + (2 × Standard Deviation)
- **Lower Band**: SMA - (2 × Standard Deviation)
- **Usage**: Measure volatility and identify potential breakouts

### ATR (Average True Range)
- **Calculation**: Maximum of (High-Low, |High-Close|, |Low-Close|)
- **Period**: 14-day average
- **Usage**: Measure volatility and set stop-loss levels

### Historical Volatility
- **Calculation**: Standard deviation of log returns (annualized)
- **Period**: 20-day rolling window
- **Usage**: Assess risk and price variability

### Volatility Cone
- **Periods**: 30, 60, 90, 180 days
- **Metrics**: Mean, Min, Max, 25th/75th percentiles
- **Usage**: Compare current volatility to historical ranges

## Technologies Used

- **Dash**: Python web framework for interactive dashboards
- **Plotly**: Interactive graphing library
- **Dash Bootstrap Components**: Bootstrap components for Dash
- **Pandas**: Data manipulation and analysis
- **yfinance**: Yahoo Finance data API
- **NumPy**: Numerical computing

## File Structure

```
Stock-Dashboard/
├── app.py              # Main dashboard application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Customization

You can customize the dashboard by modifying:
- `DEFAULT_STOCKS` in `app.py` to change default stocks
- Date range in the DatePickerRange component
- Chart layouts and colors in the callback functions

## Troubleshooting

### Data Not Loading
- Check your internet connection
- Verify stock symbols are valid
- Try a shorter date range

### Charts Not Displaying
- Ensure all dependencies are installed
- Check browser console for errors
- Try refreshing the page

## License

MIT License

## Contributing

Feel free to submit issues and enhancement requests!
