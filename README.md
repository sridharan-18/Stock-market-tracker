# Stock Market Tracker

A modern, interactive web application for tracking and managing stock portfolios with real-time price updates, watchlist management, activity logging, and Power BI integration for professional dashboards.

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

### 💰 Portfolio Simulation
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
The application includes these popular stocks:
- **AAPL** - Apple Inc.
- **GOOGL** - Alphabet Inc.
- **MSFT** - Microsoft Corporation
- **AMZN** - Amazon.com Inc.
- **TSLA** - Tesla Inc.
- **META** - Meta Platforms Inc.
- **NVDA** - NVIDIA Corporation
- **NFLX** - Netflix Inc.

### 🔄 Multi-Market Support
- **US Stocks (NYSE/NASDAQ)** - Full support for US stock market
- **NSE (National Stock Exchange)** - Full support for NSE-listed stocks
- **BSE (Bombay Stock Exchange)** - Full support for BSE-listed stocks
- **Cryptocurrencies** - Bitcoin, Ethereum, and major altcoins
- **Commodities** - Gold, oil, silver, and other commodities

### 📊 Advanced Analytics
- **Moving Averages (SMA/EMA)** - Simple and Exponential Moving Averages
- **RSI Indicator** - Relative Strength Index with overbought/oversold levels
- **MACD Indicator** - Moving Average Convergence Divergence
- **Bollinger Bands** - Volatility bands for trend analysis
- **ATR (Average True Range)** - Measure of volatility
- **Historical Volatility** - Rolling standard deviation of returns
- **Volatility Cone** - Volatility distribution across time periods

### 🎯 Advanced Portfolio Metrics
- **CAGR (Compound Annual Growth Rate)** - Annualized return calculation
- **Sharpe Ratio** - Risk-adjusted return metric
- **Sortino Ratio** - Downside risk-adjusted return metric
- **Maximum Drawdown** - Largest peak-to-trough decline
- **Volatility** - Annualized standard deviation of returns

### 📊 Power BI Integration
- **REST API** - Built-in Flask API for Power BI connectivity
- **Data Export** - Export stock and portfolio data in JSON/CSV format
- **Schema Support** - Pre-configured dataset schemas for Power BI
- **Dashboard Templates** - Ready-to-use Power BI dashboard configurations
- **Real-time Data** - Live data endpoints for Power BI refresh

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sridharan-18/Stock-market-tracker.git
cd Stock-market-tracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Local Development

1. Run the dashboard:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://127.0.0.1:8050
```

### Docker Deployment

1. Build and run with Docker:
```bash
docker build -t stock-market-tracker .
docker run -p 8050:8050 -p 8000:8000 stock-market-tracker
```

2. Or use Docker Compose:
```bash
docker-compose up -d
```

### Power BI API

Run the Power BI integration API server:
```bash
python powerbi_api.py
```

The API will be available at `http://127.0.0.1:5000` with endpoints:
- `GET /api/powerbi/health` - Health check
- `GET /api/powerbi/stock-data?symbols=AAPL,MSFT&period=1y` - Stock data
- `GET /api/powerbi/portfolio` - Portfolio data
- `GET /api/powerbi/transactions` - Transaction history
- `GET /api/powerbi/schema` - Dataset schema
- `GET /api/powerbi/config` - Dashboard configuration
- `GET /api/powerbi/metrics` - Aggregated metrics

## How to Use

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

## Deployment

### Heroku Deployment

1. Install Heroku CLI and login:
```bash
heroku login
```

2. Create a new Heroku app:
```bash
heroku create stock-market-tracker
```

3. Deploy:
```bash
git push heroku main
```

### Render Deployment

1. Connect your GitHub repository to Render
2. Render will automatically detect the `render.yaml` configuration
3. Deploy with the provided configuration

### Google Cloud Deployment

1. Enable Cloud Build and Cloud Run APIs:
```bash
gcloud services enable cloudbuild.googleapis.com run.googleapis.com
```

2. Build and deploy:
```bash
gcloud builds submit --config cloudbuild.yaml
```

3. Get the service URL:
```bash
gcloud run services describe stock-market-tracker --region us-central1 --format 'value(status.url)'
```

### Power BI Integration

This project includes Power BI integration for professional dashboards:

1. **Data Export**: Use the Power BI API to export stock and portfolio data
2. **REST API**: Built-in Flask API for Power BI connectivity
3. **Schema Support**: Pre-configured dataset schemas for Power BI
4. **Dashboard Templates**: Ready-to-use Power BI dashboard configurations

To connect Power BI:
1. Deploy the application (using any of the methods above)
2. Use the Power BI API endpoints as data sources
3. Import the provided schema for field mapping
4. Configure automatic data refresh

## File Structure

```
stock-market-tracker/
├── app.py                      # Main Dash dashboard application
├── server.py                   # Backend server for data fetching
├── indian_stocks.py            # Indian stock market integration
├── crypto_commodities.py       # Crypto and commodities data
├── portfolio_tracker.py        # Portfolio management logic
├── powerbi_integration.py      # Power BI data integration
├── powerbi_api.py              # Power BI REST API server
├── dashboard/                  # Web dashboard files
│   ├── index.html             # Main web application
│   ├── style.css              # Styling
│   ├── script.js              # Frontend logic
│   └── dashboard.py           # Dash interactive dashboard
├── data/                       # Data storage directory
├── tests/                      # Test files
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
├── Procfile                    # Heroku deployment configuration
├── render.yaml                 # Render deployment configuration
├── cloudbuild.yaml             # Google Cloud deployment configuration
├── runtime.txt                 # Python runtime specification
├── .dockerignore              # Docker ignore file
├── .gitignore                 # Git ignore file
├── LICENSE                    # MIT License
└── README.md                  # This file
```

## Technologies Used

- **Dash**: Python web framework for interactive dashboards
- **Plotly**: Interactive graphing library
- **Dash Bootstrap Components**: Bootstrap components for Dash
- **Pandas**: Data manipulation and analysis
- **yfinance**: Yahoo Finance data API
- **NumPy**: Numerical computing
- **Flask**: Web framework for Power BI API
- **Flask-CORS**: CORS support for Flask
- **Gunicorn**: WSGI HTTP Server

## Troubleshooting

### Data Not Loading
- Check your internet connection
- Verify stock symbols are valid
- Try a shorter date range

### Charts Not Displaying
- Ensure all dependencies are installed
- Check browser console for errors
- Try refreshing the page

### Docker Issues
- Ensure Docker is running
- Check port availability (8050, 8000, 5000)
- Verify Dockerfile syntax

### Deployment Issues
- Check deployment platform logs
- Verify environment variables
- Ensure all dependencies are in requirements.txt

## License

MIT License - Feel free to use and modify as needed

## Contributing

Feel free to submit issues and enhancement requests!

---

**Last Updated**: 2026-09-16  
**Version**: 2.0.0