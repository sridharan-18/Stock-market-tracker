# Stock Market Dashboard

An interactive web application for analyzing and comparing stock performance using Dash and Plotly.

## Features

- **Interactive Dashboard**: Built with Dash and Plotly for real-time data visualization
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
