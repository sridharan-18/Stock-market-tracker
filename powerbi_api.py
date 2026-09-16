"""
Flask API Server for Power BI Integration
Provides REST API endpoints for Power BI data connectivity
"""

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import pandas as pd
from datetime import datetime
import os
from powerbi_integration import PowerBIIntegration
from portfolio_tracker import PortfolioTracker

app = Flask(__name__)
CORS(app)

# Initialize Power BI integration
powerbi = PowerBIIntegration()
portfolio_tracker = PortfolioTracker()

# Ensure data directory exists
os.makedirs('data', exist_ok=True)


@app.route('/api/powerbi/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Stock Market Tracker Power BI API'
    })


@app.route('/api/powerbi/stock-data', methods=['GET'])
def get_stock_data():
    """
    Get stock data for Power BI
    
    Query Parameters:
        - symbols: Comma-separated list of stock symbols (required)
        - period: Time period (default: 1y)
        - format: Response format (json/csv, default: json)
    """
    symbols = request.args.get('symbols', '')
    period = request.args.get('period', '1y')
    response_format = request.args.get('format', 'json')
    
    if not symbols:
        return jsonify({'error': 'Symbols parameter is required'}), 400
    
    symbol_list = [s.strip().upper() for s in symbols.split(',')]
    
    try:
        stock_data = powerbi.fetch_stock_data_for_powerbi(symbol_list, period)
        
        if stock_data.empty:
            return jsonify({'error': 'No data available for the specified symbols'}), 404
        
        if response_format == 'csv':
            # Export to CSV and return file
            filename = f"stock_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = powerbi.export_to_csv(stock_data, filename)
            return send_file(filepath, mimetype='text/csv', as_attachment=True, download_name=filename)
        else:
            # Return JSON
            return jsonify({
                'data': stock_data.to_dict(orient='records'),
                'count': len(stock_data),
                'symbols': symbol_list,
                'period': period,
                'timestamp': datetime.now().isoformat()
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/powerbi/portfolio', methods=['GET'])
def get_portfolio_data():
    """
    Get portfolio data for Power BI
    
    Query Parameters:
        - format: Response format (json/csv, default: json)
    """
    response_format = request.args.get('format', 'json')
    
    try:
        holdings = portfolio_tracker.get_holdings()
        portfolio_df = powerbi.get_portfolio_summary_for_powerbi(holdings)
        
        if portfolio_df.empty:
            return jsonify({
                'data': [],
                'count': 0,
                'message': 'No portfolio data available',
                'timestamp': datetime.now().isoformat()
            })
        
        if response_format == 'csv':
            # Export to CSV and return file
            filename = f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = powerbi.export_to_csv(portfolio_df, filename)
            return send_file(filepath, mimetype='text/csv', as_attachment=True, download_name=filename)
        else:
            # Return JSON
            return jsonify({
                'data': portfolio_df.to_dict(orient='records'),
                'count': len(portfolio_df),
                'timestamp': datetime.now().isoformat()
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/powerbi/transactions', methods=['GET'])
def get_transaction_data():
    """
    Get transaction history for Power BI
    
    Query Parameters:
        - format: Response format (json/csv, default: json)
        - limit: Number of recent transactions (default: 100)
    """
    response_format = request.args.get('format', 'json')
    limit = int(request.args.get('limit', 100))
    
    try:
        transactions = portfolio_tracker.get_transactions()
        
        if transactions:
            # Limit to recent transactions
            recent_transactions = transactions[-limit:]
            df = pd.DataFrame(recent_transactions)
        else:
            df = pd.DataFrame()
        
        if df.empty:
            return jsonify({
                'data': [],
                'count': 0,
                'message': 'No transaction data available',
                'timestamp': datetime.now().isoformat()
            })
        
        if response_format == 'csv':
            # Export to CSV and return file
            filename = f"transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = f"data/{filename}"
            df.to_csv(filepath, index=False)
            return send_file(filepath, mimetype='text/csv', as_attachment=True, download_name=filename)
        else:
            # Return JSON
            return jsonify({
                'data': df.to_dict(orient='records'),
                'count': len(df),
                'timestamp': datetime.now().isoformat()
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/powerbi/schema', methods=['GET'])
def get_schema():
    """Get Power BI dataset schema"""
    schema = powerbi.get_powerbi_dataset_schema()
    return jsonify({
        'schema': schema,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/powerbi/config', methods=['GET'])
def get_config():
    """Get Power BI dashboard configuration"""
    config = powerbi.create_powerbi_dashboard_config()
    return jsonify({
        'config': config,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/powerbi/metrics', methods=['GET'])
def get_metrics():
    """Get aggregated portfolio metrics for Power BI"""
    try:
        holdings = portfolio_tracker.get_holdings()
        portfolio_df = powerbi.get_portfolio_summary_for_powerbi(holdings)
        
        if portfolio_df.empty:
            return jsonify({
                'total_value': 0,
                'total_invested': 0,
                'total_gain_loss': 0,
                'total_return_pct': 0,
                'top_performer': None,
                'worst_performer': None,
                'sector_distribution': {},
                'timestamp': datetime.now().isoformat()
            })
        
        # Calculate aggregate metrics
        total_value = portfolio_df['Current_Value'].sum()
        total_invested = portfolio_df['Total_Invested'].sum()
        total_gain_loss = portfolio_df['Unrealized_Gain_Loss'].sum()
        total_return_pct = (total_gain_loss / total_invested * 100) if total_invested > 0 else 0
        
        # Find top and worst performers
        if not portfolio_df.empty:
            top_performer = portfolio_df.loc[portfolio_df['Total_Return_Pct'].idxmax()].to_dict()
            worst_performer = portfolio_df.loc[portfolio_df['Total_Return_Pct'].idxmin()].to_dict()
        else:
            top_performer = None
            worst_performer = None
        
        # Sector distribution (if available)
        sector_distribution = {}
        if 'Sector' in portfolio_df.columns:
            sector_counts = portfolio_df['Sector'].value_counts()
            sector_distribution = sector_counts.to_dict()
        
        return jsonify({
            'total_value': total_value,
            'total_invested': total_invested,
            'total_gain_loss': total_gain_loss,
            'total_return_pct': total_return_pct,
            'top_performer': top_performer,
            'worst_performer': worst_performer,
            'sector_distribution': sector_distribution,
            'holdings_count': len(portfolio_df),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('POWERBI_API_PORT', '5000'))
    print(f"Starting Power BI API Server on port {port}")
    print(f"Available endpoints:")
    print(f"  - GET /api/powerbi/health")
    print(f"  - GET /api/powerbi/stock-data?symbols=AAPL,MSFT&period=1y&format=json")
    print(f"  - GET /api/powerbi/portfolio?format=json")
    print(f"  - GET /api/powerbi/transactions?format=json&limit=100")
    print(f"  - GET /api/powerbi/schema")
    print(f"  - GET /api/powerbi/config")
    print(f"  - GET /api/powerbi/metrics")
    
    app.run(host='0.0.0.0', port=port, debug=True)