# Stock Market Dashboard

An interactive web application for analyzing and comparing stock performance using Dash and Plotly.

## Features

- **Interactive Dashboard**: Built with Dash and Plotly for real-time data visualization
- **Multi-Market Support**: US Stocks (NYSE/NASDAQ), NSE (India), BSE (India), Cryptocurrencies, Commodities
- **Exchange Selection**: Switch between US, NSE, BSE, Crypto, and Commodities
- **Quick Stock Presets**: Pre-configured stock lists (US Tech, Nifty 50, Indian Top 8, Crypto, Commodities)
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

### 💰 Portfolio Management

- **Transaction Tracking**: Record buy/sell transactions for stocks, crypto, and commodities
- **Holdings Display**: View current portfolio holdings with average buy prices
- **Transaction History**: Complete history of all buy/sell transactions
- **Realized Gain/Loss**: Track realized gains and losses from sold positions
- **Multi-Asset Support**: Track stocks, cryptocurrencies, and commodities in one portfolio
- **Persistent Storage**: Portfolio data saved to JSON file for persistence

### 📈 Advanced Portfolio Metrics

- **CAGR (Compound Annual Growth Rate)**: Annualized return calculation over investment period
- **Sharpe Ratio**: Risk-adjusted return metric (Return - Risk Free Rate) / Volatility
- **Sortino Ratio**: Downside risk-adjusted return metric focusing on negative returns
- **Maximum Drawdown**: Largest peak-to-trough decline in portfolio value
- **Volatility**: Annualized standard deviation of portfolio returns
- **Real-time Calculation**: Metrics update automatically with current prices

### ₿ Cryptocurrency Support

- **Bitcoin (BTC)**: Real-time Bitcoin price tracking
- **Ethereum (ETH)**: Real-time Ethereum price tracking
- **Additional Cryptos**: Support for XRP, ADA, SOL, DOGE, DOT, MATIC, LINK, AVAX
- **Crypto-Specific Features**: 24h volume, market cap, circulating supply
- **USD Pairs**: All crypto prices in USD via yfinance

### 🛢️ Commodities Support

- **Gold (GC=F)**: Gold futures price tracking
- **Crude Oil (CL=F)**: Crude oil futures price tracking
- **Silver (SI=F)**: Silver futures price tracking
- **Natural Gas (NG=F)**: Natural gas futures price tracking
- **Additional Commodities**: Copper, Platinum, Corn, Wheat, Soybean, Coffee
- **Futures Data**: Real-time futures contract prices via yfinance

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
=======
# Stock Market Tracker

A modern, interactive web application for tracking and managing stock portfolios with real-time price updates, watchlist management, and activity logging.

## Features

### 📊 Interactive Dashboard
- **Dash-based Web App** - Interactive dashboard built with Dash and Plotly
- **Date Range Filter** - Select custom date ranges for analysis
- **Stock Comparison** - Compare multiple stocks side by side
- **Performance Metrics** - Real-time portfolio value, gains/losses, top performers
- **Price Comparison Chart** - Interactive line chart comparing stock prices
- **Performance Bar Chart** - Visual comparison of percentage gains/losses
- **Volume Comparison** - Average trading volume comparison
- **Stock Details Table** - Detailed breakdown of all tracked stocks
- **Auto-refresh** - Dashboard updates every 15 seconds
- **Dark Theme** - Professional dark theme with Bootstrap

### 📊 Core Features
- **Stock Search** - Search for stocks by symbol or company name with live quotes
- **Watchlist Management** - Add and remove stocks to track
- **Real-Time Updates** - Live price updates from Yahoo Finance every 15 seconds
- **Price Change Indicators** - Visual indicators (✓↑ green for gains, ✕↓ red for losses)
- **Activity Logging** - Track all your actions with timestamps
- **Portfolio Statistics** - View total portfolio value, gains/losses, and top performers

### � Portfolio Simulation
- **Virtual Trading** - Buy and sell stocks with virtual cash
- **Starting Capital** - Begin with $10,000 virtual cash balance
- **Real-time Portfolio Value** - Track portfolio value based on current stock prices
- **Holdings Tracking** - View shares owned for each stock
- **Transaction History** - Complete record of all buy/sell transactions
- **Performance Tracking** - Monitor portfolio returns over time
- **Portfolio Performance Chart** - Visual chart showing portfolio value history
- **Average Cost Calculation** - Track average cost basis for holdings

### 🔔 Alerts & Notifications
- **Price Threshold Alerts** - Set alerts when stocks go above or below specific prices
- **Real-time Alert Checking** - Alerts checked every 30 seconds
- **Toast Notifications** - Instant visual feedback when alerts trigger
- **Activity Log Integration** - Alert triggers logged in activity history
- **Alert Persistence** - Alerts saved to localStorage
- **Daily Summary** - Automatic daily portfolio performance summary
- **Gain/Loss Tracking** - Daily summary shows portfolio returns and individual stock performance

### 📈 Data Visualization
- **Interactive Candlestick Charts** - Professional OHLC (Open, High, Low, Close) candlestick charts
- **Moving Averages** - 20-day and 50-day moving average lines for trend analysis
- **Volume Charts** - Trading volume visualization with color-coded bars
- **Multiple Time Ranges** - View data for 1 month, 3 months, 6 months, 1 year, or 2 years
- **Flexible Intervals** - Daily, weekly, or monthly data intervals
- **Interactive Controls** - Toggle moving averages and volume display on/off
- **Zoom & Pan** - Interactive chart controls for detailed analysis

### 💾 Data Persistence
- **Local Storage** - Watchlist automatically saved to browser storage
- **Persistent History** - Activity log maintained during session

### 🎨 User Interface
- **Dark Theme** - Eye-friendly dark mode design
- **Responsive Design** - Works on desktop, tablet, and mobile devices
- **Smooth Animations** - Professional transitions and hover effects
- **Toast Notifications** - Real-time feedback for user actions

### 🚀 Built-in Stock Symbols
The application includes mock data for these stocks:
- **AAPL** - Apple Inc.
- **GOOGL** - Alphabet Inc.
- **MSFT** - Microsoft Corporation
- **AMZN** - Amazon.com Inc.
- **TSLA** - Tesla Inc.
- **META** - Meta Platforms Inc.
- **NVDA** - NVIDIA Corporation
- **NFLX** - Netflix Inc.

## How to Use

### Running the Applications

**Web Dashboard (Dash):**
1. Install dependencies: `pip install -r requirements.txt`
2. Run the Dash dashboard: `python dashboard/dashboard.py`
3. Open browser to `http://127.0.0.1:8050`
4. Use filters to customize date range, stocks, and interval
5. View interactive charts and performance metrics

**Web App (HTML/JS):**
1. Start the backend server: `python src/fetch_data.py`
2. Open `dashboard/index.html` in your web browser
3. Use the search bar to find stocks by symbol (e.g., AAPL) or company name
4. Click on a stock or press the Search button to add it to your watchlist

### Managing Your Watchlist
- **Add Stocks**: Search and select stocks to track
- **View Charts**: Click the "Chart" button to see interactive candlestick charts
- **Buy Stocks**: Click the "Buy" button to purchase shares with virtual cash
- **Sell Stocks**: Click the "Sell" button to sell owned shares
- **Remove Stocks**: Click the "Remove" button to delete from watchlist
- **Clear All**: Use the trash icon in the header to clear entire watchlist

### Portfolio Trading
- **Starting Balance**: Begin with $10,000 virtual cash
- **Buy Shares**: Enter number of shares to buy (cost deducted from cash)
- **Sell Shares**: Enter number of shares to sell (proceeds added to cash)
- **View Holdings**: See number of shares owned for each stock
- **Track Performance**: Monitor portfolio value and returns over time
- **View Chart**: See portfolio performance history in the Portfolio Performance section

### Setting Price Alerts
- **Open Alert Modal**: Click the "Alert" button on any stock card
- **Set Above Threshold**: Enter price to trigger alert when stock goes above
- **Set Below Threshold**: Enter price to trigger alert when stock drops below
- **Clear Alerts**: Use "Clear Alert" button to remove existing alerts
- **Alert Notifications**: Toast notifications appear when alerts trigger
- **Alert History**: Triggered alerts logged in activity log
- **Daily Summary**: Automatic daily portfolio performance summary every 24 hours

### Chart Features
- **Open Chart**: Click the "Chart" button on any stock card
- **Time Range**: Select from 1 month, 3 months, 6 months, 1 year, or 2 years
- **Interval**: Choose daily, weekly, or monthly data
- **Moving Averages**: Toggle 20-day and 50-day moving averages on/off
- **Volume**: Toggle volume chart display on/off
- **Interactive**: Zoom, pan, and explore the chart with mouse controls
- **Close**: Press Escape key or click the X button to close the chart

### Keyboard Shortcuts
- **Press "/" key** - Focus on search input from anywhere in the app
- **Press "Escape" key** - Close chart modal

### Understanding the Display
- **Green ✓↑** - Stock price increased (positive change)
- **Red ✕↓** - Stock price decreased (negative change)
- **Percentage** - Shows the percentage change from the last update

## Statistics Overview

The dashboard displays:
- **Portfolio Value** - Total value of cash and stock holdings
- **Total Gain/Loss** - Portfolio return from initial $10,000 investment
- **Watched Stocks** - Number of stocks in your watchlist
- **Top Gainer** - Stock with the highest percentage gain

## Activity Log

The recent activity section shows:
- All actions performed (adding/removing stocks)
- Timestamps for each action
- Visual indicators for action type (positive/negative)

## Technical Details

### Architecture
- **HTML5** - Semantic markup structure
- **CSS3** - Modern styling with CSS Grid/Flexbox
- **Vanilla JavaScript** - Core application logic
- **Plotly.js** - Interactive charting library for data visualization
- **Python Server** - Backend for fetching live market data from Yahoo Finance
- **Local Storage API** - For data persistence

### File Structure
```
stock-market-tracker/
├── data/               # Data storage directory
├── notebooks/          # Jupyter notebooks for analysis
├── src/                # Source code modules
│   ├── fetch_data.py   # Data fetching from Yahoo Finance API
│   ├── visualize.py    # Chart and visualization functions
│   ├── portfolio.py    # Portfolio management logic
│   └── alerts.py       # Alert and notification system
├── dashboard/          # Web dashboard files
│   ├── index.html      # Main web application
│   ├── style.css       # Styling
│   ├── script.js       # Frontend logic
│   └── dashboard.py    # Dash interactive dashboard
├── tests/              # Test files
├── requirements.txt    # Python dependencies
├── LICENSE             # MIT License
└── README.md           # This file
```

### Key Functions
- `addToWatchlist()` - Add stock to watchlist
- `removeFromWatchlist()` - Remove stock from watchlist
- `refreshWatchlist()` - Fetch live quotes from Yahoo Finance
- `renderWatchlist()` - Render watchlist UI
- `updateStats()` - Calculate and display statistics
- `addActivity()` - Log user actions
- `showToast()` - Display notifications
- `buyStock()` - Execute buy transaction
- `sellStock()` - Execute sell transaction
- `calculatePortfolioValue()` - Calculate total portfolio value
- `trackPortfolioValue()` - Record portfolio value over time
- `updatePortfolioUI()` - Update portfolio statistics display
- `renderPortfolioChart()` - Render portfolio performance chart
- `setAlert()` - Set price threshold alerts for stocks
- `checkAlerts()` - Check if any alerts should be triggered
- `generateDailySummary()` - Generate daily portfolio performance summary
- `openChartModal()` - Open interactive chart for a stock
- `updateChart()` - Fetch and render historical data
- `renderCandlestickChart()` - Render candlestick chart with Plotly
- `calculateMovingAverages()` - Calculate 20-day and 50-day moving averages

## Browser Compatibility

- ✅ Chrome/Chromium (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile browsers

## Future Enhancements

Potential features for future versions:
- Price alerts and notifications
- Portfolio comparison tools
- Advanced technical indicators (RSI, MACD, Bollinger Bands)
- Stock news feed integration
- Multiple portfolio support
- User authentication and cloud sync
- Trading simulation
- Export to CSV/Excel
- Additional chart types (line, area, scatter)

## API Integration

The application currently integrates with:
- **Yahoo Finance** - Live quotes and historical OHLCV data via Python backend

To run the backend server:
```bash
python server.py
```

The server will start on `http://127.0.0.1:8000` and provide:
- `/quote?symbol=XXX` - Live quote endpoint
- `/historical?symbol=XXX&interval=1d&range=1mo` - Historical data endpoint

## Tips for Best Experience

1. **Search Efficiently** - Start typing the stock symbol
2. **Monitor Changes** - Watch prices update in real-time
3. **Review Activity** - Check the activity log to see all your actions
4. **Mobile Usage** - The app works great on mobile devices with touch support

## License

MIT License - Feel free to use and modify as needed

## Notes

- The current version uses simulated/mock stock data for demonstration
- For production use, integrate with real market data APIs
- Prices update automatically every 5 seconds
- All watchlist data is saved locally in your browser

---

**Last Updated**: 2026-07-18  
**Version**: 1.0.0
>>>>>>> baef758faa30d43c55c52b43737ba1e66a5b2963
