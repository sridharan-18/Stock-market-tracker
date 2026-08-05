"""
Portfolio Tracker Module
Tracks buy/sell history and calculates portfolio performance.
"""

import pandas as pd
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import os


class PortfolioTracker:
    """
    Tracks portfolio transactions and calculates performance metrics.
    """
    
    def __init__(self, data_file: str = 'portfolio_data.json'):
        """
        Initialize the portfolio tracker.
        
        Args:
            data_file: Path to JSON file for storing portfolio data
        """
        self.data_file = data_file
        self.transactions = []
        self.load_data()
    
    def load_data(self):
        """Load portfolio data from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.transactions = data.get('transactions', [])
            except Exception as e:
                print(f"Error loading portfolio data: {e}")
                self.transactions = []
    
    def save_data(self):
        """Save portfolio data to JSON file."""
        try:
            data = {
                'transactions': self.transactions,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving portfolio data: {e}")
    
    def add_transaction(self, symbol: str, action: str, quantity: float, 
                       price: float, date: str = None, asset_type: str = 'stock') -> Dict[str, Any]:
        """
        Add a buy/sell transaction.
        
        Args:
            symbol: Asset symbol
            action: 'buy' or 'sell'
            quantity: Number of shares/units
            price: Price per share/unit
            date: Transaction date (YYYY-MM-DD), defaults to today
            asset_type: Type of asset ('stock', 'crypto', 'commodity')
            
        Returns:
            Transaction record
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        transaction = {
            'id': len(self.transactions) + 1,
            'symbol': symbol.upper(),
            'action': action.lower(),
            'quantity': float(quantity),
            'price': float(price),
            'total': float(quantity) * float(price),
            'date': date,
            'asset_type': asset_type.lower(),
            'timestamp': datetime.now().isoformat()
        }
        
        self.transactions.append(transaction)
        self.save_data()
        
        return transaction
    
    def remove_transaction(self, transaction_id: int) -> bool:
        """
        Remove a transaction by ID.
        
        Args:
            transaction_id: Transaction ID to remove
            
        Returns:
            True if removed, False if not found
        """
        for i, tx in enumerate(self.transactions):
            if tx['id'] == transaction_id:
                self.transactions.pop(i)
                self.save_data()
                return True
        return False
    
    def get_transactions(self, symbol: str = None) -> List[Dict[str, Any]]:
        """
        Get all transactions or transactions for a specific symbol.
        
        Args:
            symbol: Optional symbol to filter by
            
        Returns:
            List of transactions
        """
        if symbol:
            return [tx for tx in self.transactions if tx['symbol'] == symbol.upper()]
        return self.transactions
    
    def get_holdings(self) -> Dict[str, Dict[str, Any]]:
        """
        Calculate current holdings based on transactions.
        
        Returns:
            Dictionary with symbol as key and holding details as value
        """
        holdings = {}
        
        for tx in self.transactions:
            symbol = tx['symbol']
            action = tx['action']
            quantity = tx['quantity']
            price = tx['price']
            asset_type = tx['asset_type']
            
            if symbol not in holdings:
                holdings[symbol] = {
                    'symbol': symbol,
                    'quantity': 0,
                    'avg_buy_price': 0,
                    'total_invested': 0,
                    'total_sold': 0,
                    'realized_gain_loss': 0,
                    'asset_type': asset_type
                }
            
            if action == 'buy':
                # Update average buy price
                current_qty = holdings[symbol]['quantity']
                current_avg = holdings[symbol]['avg_buy_price']
                new_qty = current_qty + quantity
                
                if new_qty > 0:
                    new_avg = ((current_avg * current_qty) + (price * quantity)) / new_qty
                    holdings[symbol]['avg_buy_price'] = new_avg
                
                holdings[symbol]['quantity'] = new_qty
                holdings[symbol]['total_invested'] += quantity * price
            
            elif action == 'sell':
                holdings[symbol]['quantity'] -= quantity
                holdings[symbol]['total_sold'] += quantity * price
                
                # Calculate realized gain/loss
                gain_loss = (price - holdings[symbol]['avg_buy_price']) * quantity
                holdings[symbol]['realized_gain_loss'] += gain_loss
        
        # Remove holdings with zero quantity
        holdings = {k: v for k, v in holdings.items() if v['quantity'] > 0}
        
        return holdings
    
    def calculate_portfolio_value(self, current_prices: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculate current portfolio value with given current prices.
        
        Args:
            current_prices: Dictionary with symbol as key and current price as value
            
        Returns:
            Portfolio summary
        """
        holdings = self.get_holdings()
        total_value = 0
        total_cost = 0
        total_unrealized_gain_loss = 0
        
        asset_values = []
        
        for symbol, holding in holdings.items():
            current_price = current_prices.get(symbol, 0)
            quantity = holding['quantity']
            avg_price = holding['avg_buy_price']
            
            current_value = quantity * current_price
            cost_basis = quantity * avg_price
            unrealized_gain_loss = current_value - cost_basis
            
            total_value += current_value
            total_cost += cost_basis
            total_unrealized_gain_loss += unrealized_gain_loss
            
            asset_values.append({
                'symbol': symbol,
                'quantity': quantity,
                'avg_price': avg_price,
                'current_price': current_price,
                'current_value': current_value,
                'cost_basis': cost_basis,
                'unrealized_gain_loss': unrealized_gain_loss,
                'unrealized_gain_loss_pct': (unrealized_gain_loss / cost_basis * 100) if cost_basis > 0 else 0,
                'asset_type': holding['asset_type']
            })
        
        # Calculate total realized gain/loss from all transactions
        total_realized_gain_loss = sum(
            tx['total'] * (1 if tx['action'] == 'sell' else -1) 
            for tx in self.transactions if tx['action'] == 'sell'
        ) - sum(
            tx['total'] for tx in self.transactions if tx['action'] == 'buy'
        )
        
        total_gain_loss = total_unrealized_gain_loss + total_realized_gain_loss
        
        return {
            'total_value': total_value,
            'total_cost': total_cost,
            'total_unrealized_gain_loss': total_unrealized_gain_loss,
            'total_realized_gain_loss': total_realized_gain_loss,
            'total_gain_loss': total_gain_loss,
            'total_gain_loss_pct': (total_gain_loss / total_cost * 100) if total_cost > 0 else 0,
            'asset_values': asset_values,
            'num_holdings': len(holdings)
        }
    
    def get_transaction_history(self) -> pd.DataFrame:
        """
        Get transaction history as a DataFrame.
        
        Returns:
            DataFrame with transaction history
        """
        if not self.transactions:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.transactions)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date', ascending=False)
        return df
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """
        Get portfolio performance summary.
        
        Returns:
            Performance summary
        """
        if not self.transactions:
            return {'total_transactions': 0}
        
        df = self.get_transaction_history()
        
        total_buys = len(df[df['action'] == 'buy'])
        total_sells = len(df[df['action'] == 'sell'])
        total_volume = df['total'].sum()
        
        by_symbol = df.groupby('symbol').agg({
            'quantity': 'sum',
            'total': 'sum',
            'action': lambda x: (x == 'buy').sum() - (x == 'sell').sum()
        }).to_dict('index')
        
        return {
            'total_transactions': len(self.transactions),
            'total_buys': total_buys,
            'total_sells': total_sells,
            'total_volume': total_volume,
            'by_symbol': by_symbol
        }


def create_sample_portfolio(tracker: PortfolioTracker):
    """Create sample portfolio data for testing."""
    sample_transactions = [
        {'symbol': 'AAPL', 'action': 'buy', 'quantity': 10, 'price': 150.0, 'date': '2024-01-15'},
        {'symbol': 'TSLA', 'action': 'buy', 'quantity': 5, 'price': 200.0, 'date': '2024-01-20'},
        {'symbol': 'BTC', 'action': 'buy', 'quantity': 0.1, 'price': 45000.0, 'date': '2024-02-01', 'asset_type': 'crypto'},
        {'symbol': 'ETH', 'action': 'buy', 'quantity': 1.0, 'price': 2500.0, 'date': '2024-02-05', 'asset_type': 'crypto'},
        {'symbol': 'GOLD', 'action': 'buy', 'quantity': 2, 'price': 2000.0, 'date': '2024-02-10', 'asset_type': 'commodity'},
    ]
    
    for tx in sample_transactions:
        tracker.add_transaction(
            symbol=tx['symbol'],
            action=tx['action'],
            quantity=tx['quantity'],
            price=tx['price'],
            date=tx['date'],
            asset_type=tx.get('asset_type', 'stock')
        )
