"""
Unit tests for Power BI Integration module
"""

import unittest
import os
import tempfile
import pandas as pd
import json
from unittest.mock import Mock, patch, MagicMock

# Import the module under test
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Mock yfinance if not available
    if 'yfinance' not in sys.modules:
        sys.modules['yfinance'] = MagicMock()
    
    from powerbi_integration import PowerBIIntegration
    POWERBI_AVAILABLE = True
except ImportError:
    POWERBI_AVAILABLE = False


@unittest.skipIf(not POWERBI_AVAILABLE, "Power BI integration module not available")
class TestPowerBIIntegration(unittest.TestCase):
    """Test cases for PowerBIIntegration class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.powerbi = PowerBIIntegration()
        self.temp_dir = tempfile.mkdtemp()
        self.original_data_dir = 'data'
        
        # Create temporary data directory
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
    
    def tearDown(self):
        """Clean up test fixtures"""
        # Clean up temporary directory
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_initialization(self):
        """Test that PowerBIIntegration initializes correctly"""
        self.assertIsInstance(self.powerbi, PowerBIIntegration)
        self.assertEqual(self.powerbi.base_url, "http://localhost:8050")
    
    @patch('powerbi_integration.yf.Ticker')
    def test_fetch_stock_data_for_powerbi(self, mock_ticker):
        """Test fetching stock data for Power BI"""
        # Mock the yfinance Ticker response
        mock_hist = pd.DataFrame({
            'Open': [150, 151, 152],
            'High': [155, 156, 157],
            'Low': [149, 150, 151],
            'Close': [154, 155, 156],
            'Volume': [1000000, 1100000, 1200000]
        }, index=pd.date_range('2024-01-01', periods=3))
        
        mock_ticker_instance = Mock()
        mock_ticker_instance.history.return_value = mock_hist
        mock_ticker_instance.info = {
            'longName': 'Apple Inc.',
            'sector': 'Technology',
            'industry': 'Consumer Electronics'
        }
        mock_ticker.return_value = mock_ticker_instance
        
        symbols = ['AAPL']
        result = self.powerbi.fetch_stock_data_for_powerbi(symbols, period='1mo')
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)
        self.assertIn('Symbol', result.columns)
        self.assertIn('Company_Name', result.columns)
        self.assertIn('Sector', result.columns)
        self.assertIn('Industry', result.columns)
        self.assertIn('Daily_Return', result.columns)
    
    @patch('powerbi_integration.yf.Ticker')
    def test_fetch_stock_data_multiple_symbols(self, mock_ticker):
        """Test fetching data for multiple symbols"""
        # Mock the yfinance Ticker response
        mock_hist = pd.DataFrame({
            'Open': [150, 151],
            'High': [155, 156],
            'Low': [149, 150],
            'Close': [154, 155],
            'Volume': [1000000, 1100000]
        }, index=pd.date_range('2024-01-01', periods=2))
        
        mock_ticker_instance = Mock()
        mock_ticker_instance.history.return_value = mock_hist
        mock_ticker_instance.info = {
            'longName': 'Test Company',
            'sector': 'Technology',
            'industry': 'Software'
        }
        mock_ticker.return_value = mock_ticker_instance
        
        symbols = ['AAPL', 'MSFT']
        result = self.powerbi.fetch_stock_data_for_powerbi(symbols, period='1mo')
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result['Symbol'].unique()), 2)
    
    def test_get_portfolio_summary_for_powerbi_empty(self):
        """Test portfolio summary with empty portfolio"""
        portfolio_data = {}
        result = self.powerbi.get_portfolio_summary_for_powerbi(portfolio_data)
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(result.empty)
    
    @patch('powerbi_integration.yf.Ticker')
    def test_get_portfolio_summary_for_powerbi_with_data(self, mock_ticker):
        """Test portfolio summary with portfolio data"""
        portfolio_data = {
            'AAPL': {
                'quantity': 10,
                'avg_buy_price': 150.0,
                'total_invested': 1500.0,
                'realized_gain_loss': 50.0,
                'asset_type': 'stock'
            }
        }
        
        # Mock the yfinance Ticker response
        mock_ticker_instance = Mock()
        mock_ticker_instance.info = {'currentPrice': 160.0}
        mock_ticker.return_value = mock_ticker_instance
        
        result = self.powerbi.get_portfolio_summary_for_powerbi(portfolio_data)
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]['Symbol'], 'AAPL')
        self.assertEqual(result.iloc[0]['Quantity'], 10)
        self.assertEqual(result.iloc[0]['Current_Price'], 160.0)
        self.assertEqual(result.iloc[0]['Current_Value'], 1600.0)
    
    def test_export_to_csv(self):
        """Test exporting data to CSV"""
        test_data = pd.DataFrame({
            'Symbol': ['AAPL', 'MSFT'],
            'Price': [150.0, 300.0]
        })
        
        # Change to temp directory for test
        original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
        try:
            os.makedirs('data', exist_ok=True)
            filepath = self.powerbi.export_to_csv(test_data, 'test_export.csv')
            
            self.assertTrue(os.path.exists(filepath))
            self.assertTrue(filepath.endswith('test_export.csv'))
            
            # Verify the file contains data
            loaded_data = pd.read_csv(filepath)
            self.assertEqual(len(loaded_data), 2)
            
        finally:
            os.chdir(original_cwd)
    
    def test_export_to_json(self):
        """Test exporting data to JSON"""
        test_data = {
            'symbol': 'AAPL',
            'price': 150.0,
            'quantity': 10
        }
        
        # Change to temp directory for test
        original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
        try:
            os.makedirs('data', exist_ok=True)
            filepath = self.powerbi.export_to_json(test_data, 'test_export.json')
            
            self.assertTrue(os.path.exists(filepath))
            self.assertTrue(filepath.endswith('test_export.json'))
            
            # Verify the file contains data
            with open(filepath, 'r') as f:
                loaded_data = json.load(f)
            self.assertEqual(loaded_data['symbol'], 'AAPL')
            
        finally:
            os.chdir(original_cwd)
    
    def test_get_powerbi_dataset_schema(self):
        """Test getting Power BI dataset schema"""
        schema = self.powerbi.get_powerbi_dataset_schema()
        
        self.assertIsInstance(schema, dict)
        self.assertIn('stock_data', schema)
        self.assertIn('portfolio_data', schema)
        
        # Check stock_data schema
        stock_schema = schema['stock_data']
        self.assertIn('columns', stock_schema)
        self.assertTrue(any(col['name'] == 'Symbol' for col in stock_schema['columns']))
        self.assertTrue(any(col['name'] == 'Close' for col in stock_schema['columns']))
        
        # Check portfolio_data schema
        portfolio_schema = schema['portfolio_data']
        self.assertIn('columns', portfolio_schema)
        self.assertTrue(any(col['name'] == 'Symbol' for col in portfolio_schema['columns']))
        self.assertTrue(any(col['name'] == 'Current_Value' for col in portfolio_schema['columns']))
    
    def test_create_powerbi_dashboard_config(self):
        """Test creating Power BI dashboard configuration"""
        config = self.powerbi.create_powerbi_dashboard_config()
        
        self.assertIsInstance(config, dict)
        self.assertIn('data_source', config)
        self.assertIn('recommended_visualizations', config)
        self.assertIn('data_refresh_schedule', config)
        
        # Check data source configuration
        data_source = config['data_source']
        self.assertEqual(data_source['type'], 'REST_API')
        self.assertIn('endpoints', data_source)
        
        # Check recommended visualizations
        visualizations = config['recommended_visualizations']
        self.assertTrue(len(visualizations) > 0)
        self.assertTrue(any(viz['type'] == 'Line Chart' for viz in visualizations))
        self.assertTrue(any(viz['type'] == 'Card' for viz in visualizations))
    
    def test_schema_column_types(self):
        """Test that schema columns have proper types"""
        schema = self.powerbi.get_powerbi_dataset_schema()
        
        for dataset_name, dataset_schema in schema.items():
            for column in dataset_schema['columns']:
                self.assertIn('name', column)
                self.assertIn('type', column)
                self.assertIn(column['type'], ['string', 'datetime', 'decimal', 'integer'])
    
    def test_config_visualization_structure(self):
        """Test that visualizations in config have proper structure"""
        config = self.powerbi.create_powerbi_dashboard_config()
        
        for viz in config['recommended_visualizations']:
            self.assertIn('type', viz)
            self.assertIn('title', viz)
            self.assertIn('data_fields', viz)


@unittest.skipIf(not POWERBI_AVAILABLE, "Power BI integration module not available")
class TestPowerBIIntegrationEdgeCases(unittest.TestCase):
    """Test edge cases and error handling for Power BI Integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.powerbi = PowerBIIntegration()
    
    @patch('powerbi_integration.yf.Ticker')
    def test_fetch_stock_data_with_empty_symbols(self, mock_ticker):
        """Test fetching data with empty symbols list"""
        result = self.powerbi.fetch_stock_data_for_powerbi([], period='1mo')
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(result.empty)
    
    @patch('powerbi_integration.yf.Ticker')
    def test_fetch_stock_data_with_api_error(self, mock_ticker):
        """Test handling of API errors when fetching stock data"""
        mock_ticker.side_effect = Exception("API Error")
        
        symbols = ['AAPL']
        result = self.powerbi.fetch_stock_data_for_powerbi(symbols, period='1mo')
        
        # Should return empty DataFrame on error
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(result.empty)
    
    @patch('powerbi_integration.yf.Ticker')
    def test_get_portfolio_summary_with_price_error(self, mock_ticker):
        """Test handling of price fetch errors in portfolio summary"""
        portfolio_data = {
            'AAPL': {
                'quantity': 10,
                'avg_buy_price': 150.0,
                'total_invested': 1500.0,
                'realized_gain_loss': 50.0,
                'asset_type': 'stock'
            }
        }
        
        # Mock the yfinance Ticker to raise an exception
        mock_ticker.side_effect = Exception("Price fetch error")
        
        result = self.powerbi.get_portfolio_summary_for_powerbi(portfolio_data)
        
        # Should still return DataFrame with zero current price
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)
        self.assertEqual(result.iloc[0]['Current_Price'], 0)
        self.assertEqual(result.iloc[0]['Current_Value'], 0)


if __name__ == '__main__':
    unittest.main()