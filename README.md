# Stock Market Tracker

A modern, interactive web application for tracking and managing stock portfolios with real-time price updates, watchlist management, and activity logging.

## Features

### 📊 Core Features
- **Stock Search** - Search for stocks by symbol or company name
- **Watchlist Management** - Add and remove stocks to track
- **Real-Time Updates** - Simulated price updates every 5 seconds
- **Price Change Indicators** - Visual indicators (✓↑ green for gains, ✕↓ red for losses)
- **Activity Logging** - Track all your actions with timestamps
- **Portfolio Statistics** - View total portfolio value, gains/losses, and top performers

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
- **View Details**: Click the "Chart" button to see more information
- **Remove Stocks**: Click the "Remove" button to delete from watchlist
- **Clear All**: Use the trash icon in the header to clear entire watchlist

### Keyboard Shortcuts
- **Press "/" key** - Focus on search input from anywhere in the app

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
- **Vanilla JavaScript** - No external dependencies required
- **Local Storage API** - For data persistence

### File Structure
```
Stock Market Tracker/
├── index.html          # Main HTML file
├── style.css           # Complete styling
├── script.js           # Application logic
├── package.json        # Project metadata
└── README.md           # This file
```

### Key Functions
- `addToWatchlist()` - Add stock to watchlist
- `removeFromWatchlist()` - Remove stock from watchlist
- `simulatePriceUpdate()` - Update stock prices
- `renderWatchlist()` - Render watchlist UI
- `updateStats()` - Calculate and display statistics
- `addActivity()` - Log user actions
- `showToast()` - Display notifications

## Browser Compatibility

- ✅ Chrome/Chromium (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile browsers

## Future Enhancements

Potential features for future versions:
- Real API integration (Alpha Vantage, Yahoo Finance, etc.)
- Interactive charts (using Chart.js or similar)
- Price alerts and notifications
- Portfolio comparison tools
- Historical data analysis
- Stock news feed
- Multiple portfolio support
- User authentication
- Trading simulation
- Export to CSV

## API Integration

To connect to real market data, replace the `mockStocks` object in `script.js` with API calls to services like:
- **Alpha Vantage** - Free API for stock prices
- **Yahoo Finance** - Historical and real-time data
- **IEX Cloud** - Comprehensive market data
- **Finnhub** - Real-time market data

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
