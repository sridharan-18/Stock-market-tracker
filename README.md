# Stock Market Tracker

A modern, interactive web application for tracking and managing stock portfolios with real-time price updates, watchlist management, and activity logging.

## Features

### 📊 Core Features
- **Stock Search** - Search for stocks by symbol or company name with live quotes
- **Watchlist Management** - Add and remove stocks to track
- **Real-Time Updates** - Live price updates from Yahoo Finance every 15 seconds
- **Price Change Indicators** - Visual indicators (✓↑ green for gains, ✕↓ red for losses)
- **Activity Logging** - Track all your actions with timestamps
- **Portfolio Statistics** - View total portfolio value, gains/losses, and top performers

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

### Getting Started
1. Open `index.html` in your web browser
2. Use the search bar to find stocks by symbol (e.g., AAPL) or company name
3. Click on a stock or press the Search button to add it to your watchlist

### Managing Your Watchlist
- **Add Stocks**: Search and select stocks to track
- **View Charts**: Click the "Chart" button to see interactive candlestick charts
- **Remove Stocks**: Click the "Remove" button to delete from watchlist
- **Clear All**: Use the trash icon in the header to clear entire watchlist

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
- **Portfolio Value** - Total value of all watched stocks
- **Total Gain/Loss** - Combined gains/losses across all stocks
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
Stock Market Tracker/
├── index.html          # Main HTML file
├── style.css           # Complete styling
├── script.js           # Application logic and chart rendering
├── server.py           # Python backend for Yahoo Finance API
├── package.json        # Project metadata
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
