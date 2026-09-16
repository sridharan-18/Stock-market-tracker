"""
Power BI Integration Module for Stock Market Tracker
Provides data export and API endpoints for Power BI connectivity
"""

import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import json
from typing import List, Dict, Optional
import io
import csv


class PowerBIIntegration:
    """Class to handle Power BI data integration"""
    
    def __init__(self):
        self.base_url = "http://localhost:8050"
    
    def fetch_stock_data_for_powerbi(self, symbols: List[str], period: str = "1y") -> pd.DataFrame:
        """
        Fetch stock data formatted for Power BI consumption
        
        Args:
            symbols: List of stock symbols
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)
            
        Returns:
            DataFrame with Power BI-friendly structure
        """
        all_data = []
        
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period=period)
                
                if not hist.empty:
                    # Add symbol column for Power BI
                    hist['Symbol'] = symbol
                    hist['Company_Name'] = ticker.info.get('longName', symbol)
                    hist['Sector'] = ticker.info.get('sector', 'N/A')
                    hist['Industry'] = ticker.info.get('industry', 'N/A')
                    
                    # Calculate additional metrics
                    hist['Daily_Return'] = hist['Close'].pct_change() * 100
                    hist['Volume_MA_20'] = hist['Volume'].rolling(window=20).mean()
                    hist['Price_MA_20'] = hist['Close'].rolling(window=20).mean()
                    hist['Price_MA_50'] = hist['Close'].rolling(window=50).mean()
                    
                    # Reset index to make Date a column
                    hist = hist.reset_index()
                    hist.columns = [str(col).replace(' ', '_') for col in hist.columns]
                    
                    all_data.append(hist)
                    
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")
                continue
        
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        return pd.DataFrame()
    
    def get_portfolio_summary_for_powerbi(self, portfolio_data: Dict) -> pd.DataFrame:
        """
        Transform portfolio data for Power BI
        
        Args:
            portfolio_data: Portfolio data dictionary
            
        Returns:
            DataFrame with portfolio summary
        """
        if not portfolio_data:
            return pd.DataFrame()
        
        records = []
        for symbol, data in portfolio_data.items():
            record = {
                'Symbol': symbol,
                'Quantity': data.get('quantity', 0),
                'Average_Buy_Price': data.get('avg_buy_price', 0),
                'Total_Invested': data.get('total_invested', 0),
                'Realized_Gain_Loss': data.get('realized_gain_loss', 0),
                'Asset_Type': data.get('asset_type', 'stock'),
                'Last_Updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Get current price
            try:
                ticker = yf.Ticker(symbol)
                current_price = ticker.info.get('currentPrice', 0)
                record['Current_Price'] = current_price
                record['Current_Value'] = current_price * data.get('quantity', 0)
                record['Unrealized_Gain_Loss'] = record['Current_Value'] - record['Total_Invested']
                record['Total_Return_Pct'] = (record['Unrealized_Gain_Loss'] / record['Total_Invested'] * 100) if record['Total_Invested'] > 0 else 0
            except:
                record['Current_Price'] = 0
                record['Current_Value'] = 0
                record['Unrealized_Gain_Loss'] = 0
                record['Total_Return_Pct'] = 0
            
            records.append(record)
        
        return pd.DataFrame(records)
    
    def export_to_csv(self, dataframe: pd.DataFrame, filename: str) -> str:
        """
        Export DataFrame to CSV for Power BI import
        
        Args:
            dataframe: DataFrame to export
            filename: Output filename
            
        Returns:
            Path to exported CSV file
        """
        filepath = f"data/{filename}"
        dataframe.to_csv(filepath, index=False)
        return filepath
    
    def export_to_json(self, data: Dict, filename: str) -> str:
        """
        Export data to JSON for Power BI
        
        Args:
            data: Data dictionary to export
            filename: Output filename
            
        Returns:
            Path to exported JSON file
        """
        filepath = f"data/{filename}"
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return filepath
    
    def get_powerbi_dataset_schema(self) -> Dict:
        """
        Return dataset schema for Power BI configuration
        
        Returns:
            Dictionary describing the data schema
        """
        return {
            "stock_data": {
                "columns": [
                    {"name": "Date", "type": "datetime"},
                    {"name": "Symbol", "type": "string"},
                    {"name": "Company_Name", "type": "string"},
                    {"name": "Sector", "type": "string"},
                    {"name": "Industry", "type": "string"},
                    {"name": "Open", "type": "decimal"},
                    {"name": "High", "type": "decimal"},
                    {"name": "Low", "type": "decimal"},
                    {"name": "Close", "type": "decimal"},
                    {"name": "Volume", "type": "integer"},
                    {"name": "Daily_Return", "type": "decimal"},
                    {"name": "Volume_MA_20", "type": "decimal"},
                    {"name": "Price_MA_20", "type": "decimal"},
                    {"name": "Price_MA_50", "type": "decimal"}
                ]
            },
            "portfolio_data": {
                "columns": [
                    {"name": "Symbol", "type": "string"},
                    {"name": "Quantity", "type": "decimal"},
                    {"name": "Average_Buy_Price", "type": "decimal"},
                    {"name": "Total_Invested", "type": "decimal"},
                    {"name": "Realized_Gain_Loss", "type": "decimal"},
                    {"name": "Asset_Type", "type": "string"},
                    {"name": "Current_Price", "type": "decimal"},
                    {"name": "Current_Value", "type": "decimal"},
                    {"name": "Unrealized_Gain_Loss", "type": "decimal"},
                    {"name": "Total_Return_Pct", "type": "decimal"},
                    {"name": "Last_Updated", "type": "datetime"}
                ]
            }
        }
    
    def create_powerbi_dashboard_config(self) -> Dict:
        """
        Create Power BI dashboard configuration template
        
        Returns:
            Dictionary with Power BI configuration
        """
        return {
            "data_source": {
                "type": "REST_API",
                "base_url": self.base_url,
                "endpoints": {
                    "stock_data": "/api/powerbi/stock-data",
                    "portfolio": "/api/powerbi/portfolio",
                    "transactions": "/api/powerbi/transactions"
                },
                "authentication": "None",
                "refresh_interval": "15 minutes"
            },
            "recommended_visualizations": [
                {
                    "type": "Line Chart",
                    "title": "Stock Price Trends",
                    "data_fields": ["Date", "Close"],
                    "group_by": "Symbol"
                },
                {
                    "type": "Card",
                    "title": "Portfolio Value",
                    "data_fields": ["Current_Value"],
                    "aggregation": "Sum"
                },
                {
                    "type": "Bar Chart",
                    "title": "Sector Distribution",
                    "data_fields": ["Sector"],
                    "aggregation": "Count"
                },
                {
                    "type": "Table",
                    "title": "Holdings Summary",
                    "data_fields": ["Symbol", "Quantity", "Current_Value", "Total_Return_Pct"]
                },
                {
                    "type": "Gauge",
                    "title": "Portfolio Performance",
                    "data_fields": ["Total_Return_Pct"],
                    "target": 10
                }
            ],
            "data_refresh_schedule": {
                "frequency": "Daily",
                "time": "09:30 AM",
                "timezone": "UTC"
            }
        }


# Example usage and testing
if __name__ == "__main__":
    powerbi = PowerBIIntegration()
    
    # Test stock data fetch
    symbols = ['AAPL', 'MSFT', 'GOOGL']
    stock_data = powerbi.fetch_stock_data_for_powerbi(symbols)
    
    if not stock_data.empty:
        print("Stock Data for Power BI:")
        print(stock_data.head())
        
        # Export to CSV
        csv_path = powerbi.export_to_csv(stock_data, "powerbi_stock_data.csv")
        print(f"\nData exported to: {csv_path}")
    
    # Test portfolio data
    sample_portfolio = {
        'AAPL': {
            'quantity': 10,
            'avg_buy_price': 150.0,
            'total_invested': 1500.0,
            'realized_gain_loss': 50.0,
            'asset_type': 'stock'
        },
        'MSFT': {
            'quantity': 5,
            'avg_buy_price': 300.0,
            'total_invested': 1500.0,
            'realized_gain_loss': -20.0,
            'asset_type': 'stock'
        }
    }
    
    portfolio_df = powerbi.get_portfolio_summary_for_powerbi(sample_portfolio)
    print("\nPortfolio Data for Power BI:")
    print(portfolio_df)
    
    # Export portfolio data
    portfolio_csv = powerbi.export_to_csv(portfolio_df, "powerbi_portfolio.csv")
    print(f"\nPortfolio data exported to: {portfolio_csv}")
    
    # Get schema
    schema = powerbi.get_powerbi_dataset_schema()
    print("\nPower BI Dataset Schema:")
    print(json.dumps(schema, indent=2))
    
    # Get dashboard config
    config = powerbi.create_powerbi_dashboard_config()
    print("\nPower BI Dashboard Configuration:")
    print(json.dumps(config, indent=2))