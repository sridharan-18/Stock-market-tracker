"""
Unit tests for Power BI API module
"""

import unittest
import os
import tempfile
import json
from unittest.mock import Mock, patch, MagicMock

# Import the module under test
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Mock Flask before importing to avoid import errors if dependencies not available
    if 'flask' not in sys.modules:
        sys.modules['flask'] = MagicMock()
        sys.modules['flask_cors'] = MagicMock()
    
    from powerbi_api import app, powerbi, portfolio_tracker
    API_AVAILABLE = True
except ImportError:
    API_AVAILABLE = False


@unittest.skipIf(not API_AVAILABLE, "Power BI API module not available")
class TestPowerBIAPI(unittest.TestCase):
    """Test cases for Power BI API endpoints"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Create temporary data directory
        self.temp_dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.temp_dir, 'data'), exist_ok=True)
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_health_check_endpoint(self):
        """Test the health check endpoint"""
        response = self.client.get('/api/powerbi/health')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)
        self.assertIn('service', data)
    
    def test_health_check_service_name(self):
        """Test that health check returns correct service name"""
        response = self.client.get('/api/powerbi/health')
        data = json.loads(response.data)
        
        self.assertEqual(data['service'], 'Stock Market Tracker Power BI API')
    
    def test_schema_endpoint(self):
        """Test the schema endpoint"""
        response = self.client.get('/api/powerbi/schema')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('schema', data)
        self.assertIn('timestamp', data)
        self.assertIn('stock_data', data['schema'])
        self.assertIn('portfolio_data', data['schema'])
    
    def test_config_endpoint(self):
        """Test the config endpoint"""
        response = self.client.get('/api/powerbi/config')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('config', data)
        self.assertIn('timestamp', data)
        self.assertIn('data_source', data['config'])
        self.assertIn('recommended_visualizations', data['config'])
    
    def test_stock_data_endpoint_missing_symbols(self):
        """Test stock data endpoint without symbols parameter"""
        response = self.client.get('/api/powerbi/stock-data')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_stock_data_endpoint_with_symbols(self):
        """Test stock data endpoint with symbols parameter"""
        with patch('powerbi_api.powerbi.fetch_stock_data_for_powerbi') as mock_fetch:
            # Mock the fetch to return a DataFrame
            import pandas as pd
            mock_df = pd.DataFrame({
                'Symbol': ['AAPL'],
                'Close': [150.0]
            })
            mock_fetch.return_value = mock_df
            
            response = self.client.get('/api/powerbi/stock-data?symbols=AAPL')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('data', data)
            self.assertIn('count', data)
            self.assertIn('symbols', data)
    
    def test_stock_data_endpoint_empty_result(self):
        """Test stock data endpoint when no data is available"""
        with patch('powerbi_api.powerbi.fetch_stock_data_for_powerbi') as mock_fetch:
            import pandas as pd
            mock_fetch.return_value = pd.DataFrame()
            
            response = self.client.get('/api/powerbi/stock-data?symbols=INVALID')
            
            self.assertEqual(response.status_code, 404)
            data = json.loads(response.data)
            self.assertIn('error', data)
    
    def test_portfolio_endpoint(self):
        """Test portfolio endpoint"""
        with patch('powerbi_api.portfolio_tracker.get_holdings') as mock_holdings:
            mock_holdings.return_value = {}
            
            response = self.client.get('/api/powerbi/portfolio')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('data', data)
            self.assertIn('count', data)
            self.assertIn('timestamp', data)
    
    def test_portfolio_endpoint_with_holdings(self):
        """Test portfolio endpoint with holdings data"""
        with patch('powerbi_api.portfolio_tracker.get_holdings') as mock_holdings, \
             patch('powerbi_api.powerbi.get_portfolio_summary_for_powerbi') as mock_summary:
            
            mock_holdings.return_value = {
                'AAPL': {
                    'quantity': 10,
                    'avg_buy_price': 150.0,
                    'total_invested': 1500.0,
                    'realized_gain_loss': 50.0,
                    'asset_type': 'stock'
                }
            }
            
            import pandas as pd
            mock_df = pd.DataFrame({
                'Symbol': ['AAPL'],
                'Quantity': [10]
            })
            mock_summary.return_value = mock_df
            
            response = self.client.get('/api/powerbi/portfolio')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('data', data)
            self.assertEqual(data['count'], 1)
    
    def test_transactions_endpoint(self):
        """Test transactions endpoint"""
        with patch('powerbi_api.portfolio_tracker.get_transactions') as mock_transactions:
            mock_transactions.return_value = []
            
            response = self.client.get('/api/powerbi/transactions')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('data', data)
            self.assertIn('count', data)
    
    def test_transactions_endpoint_with_limit(self):
        """Test transactions endpoint with limit parameter"""
        with patch('powerbi_api.portfolio_tracker.get_transactions') as mock_transactions:
            # Create mock transactions
            mock_transactions.return_value = [
                {'symbol': 'AAPL', 'action': 'buy', 'quantity': 10, 'price': 150.0},
                {'symbol': 'MSFT', 'action': 'buy', 'quantity': 5, 'price': 300.0}
            ]
            
            response = self.client.get('/api/powerbi/transactions?limit=1')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['count'], 1)
    
    def test_metrics_endpoint(self):
        """Test metrics endpoint"""
        with patch('powerbi_api.portfolio_tracker.get_holdings') as mock_holdings, \
             patch('powerbi_api.powerbi.get_portfolio_summary_for_powerbi') as mock_summary:
            
            mock_holdings.return_value = {}
            import pandas as pd
            mock_summary.return_value = pd.DataFrame()
            
            response = self.client.get('/api/powerbi/metrics')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('total_value', data)
            self.assertIn('total_invested', data)
            self.assertIn('total_gain_loss', data)
            self.assertIn('total_return_pct', data)
            self.assertIn('timestamp', data)
    
    def test_metrics_endpoint_with_holdings(self):
        """Test metrics endpoint with holdings data"""
        with patch('powerbi_api.portfolio_tracker.get_holdings') as mock_holdings, \
             patch('powerbi_api.powerbi.get_portfolio_summary_for_powerbi') as mock_summary:
            
            mock_holdings.return_value = {
                'AAPL': {
                    'quantity': 10,
                    'avg_buy_price': 150.0,
                    'total_invested': 1500.0,
                    'realized_gain_loss': 50.0,
                    'asset_type': 'stock'
                }
            }
            
            import pandas as pd
            mock_df = pd.DataFrame({
                'Symbol': ['AAPL'],
                'Quantity': [10],
                'Current_Value': [1600.0],
                'Total_Invested': [1500.0],
                'Unrealized_Gain_Loss': [100.0],
                'Total_Return_Pct': [6.67]
            })
            mock_summary.return_value = mock_df
            
            response = self.client.get('/api/powerbi/metrics')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['total_value'], 1600.0)
            self.assertEqual(data['total_invested'], 1500.0)
            self.assertEqual(data['total_gain_loss'], 100.0)
            self.assertEqual(data['holdings_count'], 1)
    
    def test_csv_format_parameter(self):
        """Test CSV format parameter for stock data endpoint"""
        with patch('powerbi_api.powerbi.fetch_stock_data_for_powerbi') as mock_fetch, \
             patch('powerbi_api.powerbi.export_to_csv') as mock_export:
            
            import pandas as pd
            mock_df = pd.DataFrame({
                'Symbol': ['AAPL'],
                'Close': [150.0]
            })
            mock_fetch.return_value = mock_df
            mock_export.return_value = 'data/test.csv'
            
            response = self.client.get('/api/powerbi/stock-data?symbols=AAPL&format=csv')
            
            # The response should be a file download
            self.assertEqual(response.status_code, 200)
    
    def test_period_parameter(self):
        """Test period parameter for stock data endpoint"""
        with patch('powerbi_api.powerbi.fetch_stock_data_for_powerbi') as mock_fetch:
            import pandas as pd
            mock_df = pd.DataFrame({
                'Symbol': ['AAPL'],
                'Close': [150.0]
            })
            mock_fetch.return_value = mock_df
            
            response = self.client.get('/api/powerbi/stock-data?symbols=AAPL&period=6mo')
            
            self.assertEqual(response.status_code, 200)
            mock_fetch.assert_called_once()
            # Verify that the period parameter was passed correctly
            call_args = mock_fetch.call_args
            self.assertEqual(call_args[0][1], '6mo')  # period parameter


@unittest.skipIf(not API_AVAILABLE, "Power BI API module not available")
class TestPowerBIAPIErrorHandling(unittest.TestCase):
    """Test error handling in Power BI API"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_stock_data_endpoint_api_error(self):
        """Test stock data endpoint when API call fails"""
        with patch('powerbi_api.powerbi.fetch_stock_data_for_powerbi') as mock_fetch:
            mock_fetch.side_effect = Exception("API Error")
            
            response = self.client.get('/api/powerbi/stock-data?symbols=AAPL')
            
            self.assertEqual(response.status_code, 500)
            data = json.loads(response.data)
            self.assertIn('error', data)
    
    def test_portfolio_endpoint_error(self):
        """Test portfolio endpoint when calculation fails"""
        with patch('powerbi_api.portfolio_tracker.get_holdings') as mock_holdings, \
             patch('powerbi_api.powerbi.get_portfolio_summary_for_powerbi') as mock_summary:
            
            mock_holdings.side_effect = Exception("Database error")
            
            response = self.client.get('/api/powerbi/portfolio')
            
            self.assertEqual(response.status_code, 500)
            data = json.loads(response.data)
            self.assertIn('error', data)
    
    def test_transactions_endpoint_error(self):
        """Test transactions endpoint when fetch fails"""
        with patch('powerbi_api.portfolio_tracker.get_transactions') as mock_transactions:
            mock_transactions.side_effect = Exception("Transaction error")
            
            response = self.client.get('/api/powerbi/transactions')
            
            self.assertEqual(response.status_code, 500)
            data = json.loads(response.data)
            self.assertIn('error', data)
    
    def test_metrics_endpoint_error(self):
        """Test metrics endpoint when calculation fails"""
        with patch('powerbi_api.portfolio_tracker.get_holdings') as mock_holdings:
            mock_holdings.side_effect = Exception("Metrics calculation error")
            
            response = self.client.get('/api/powerbi/metrics')
            
            self.assertEqual(response.status_code, 500)
            data = json.loads(response.data)
            self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main()