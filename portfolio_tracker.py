"""
Portfolio Tracker Module
Tracks buy/sell history and calculates portfolio performance.
"""

import pandas as pd
import json
import numpy as np
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
    
    def calculate_cagr(self, current_prices: Dict[str, float], risk_free_rate: float = 0.02) -> Dict[str, Any]:
        """
        Calculate Compound Annual Growth Rate (CAGR) for the portfolio.
        
        Args:
            current_prices: Dictionary with symbol as key and current price as value
            risk_free_rate: Risk-free rate (default 2%)
            
        Returns:
            CAGR metrics
        """
        if not self.transactions:
            return {'cagr': 0, 'annualized_return': 0}
        
        # Get first and last transaction dates
        df = self.get_transaction_history()
        if df.empty:
            return {'cagr': 0, 'annualized_return': 0}
        
        first_date = df['date'].min()
        last_date = df['date'].max()
        
        # Calculate years between first and last transaction
        years = (last_date - first_date).days / 365.25
        
        if years < 0.01:  # Less than ~3.65 days
            return {'cagr': 0, 'annualized_return': 0, 'years': years}
        
        # Calculate portfolio value
        portfolio_summary = self.calculate_portfolio_value(current_prices)
        total_value = portfolio_summary['total_value']
        total_cost = portfolio_summary['total_cost']
        
        if total_cost <= 0:
            return {'cagr': 0, 'annualized_return': 0, 'years': years}
        
        # CAGR formula: (Ending Value / Beginning Value)^(1/n) - 1
        cagr = ((total_value / total_cost) ** (1 / years)) - 1
        
        return {
            'cagr': cagr * 100,  # Convert to percentage
            'annualized_return': cagr * 100,
            'years': years,
            'total_value': total_value,
            'total_cost': total_cost
        }
    
    def calculate_sharpe_ratio(self, current_prices: Dict[str, float], 
                               historical_data: Dict[str, pd.DataFrame] = None,
                               risk_free_rate: float = 0.02) -> Dict[str, Any]:
        """
        Calculate Sharpe Ratio for the portfolio.
        
        Args:
            current_prices: Dictionary with symbol as key and current price as value
            historical_data: Dictionary with symbol as key and historical price DataFrame
            risk_free_rate: Risk-free rate (default 2%)
            
        Returns:
            Sharpe ratio metrics
        """
        if not self.transactions:
            return {'sharpe_ratio': 0, 'sortino_ratio': 0}
        
        portfolio_summary = self.calculate_portfolio_value(current_prices)
        total_value = portfolio_summary['total_value']
        total_cost = portfolio_summary['total_cost']
        
        if total_cost <= 0:
            return {'sharpe_ratio': 0, 'sortino_ratio': 0}
        
        # Calculate total return
        total_return = (total_value - total_cost) / total_cost
        
        # If historical data provided, calculate volatility-based Sharpe ratio
        if historical_data:
            # Calculate portfolio returns over time
            holdings = self.get_holdings()
            portfolio_returns = []
            
            for symbol, holding in holdings.items():
                if symbol in historical_data and not historical_data[symbol].empty:
                    data = historical_data[symbol]
                    # Calculate daily returns
                    returns = data['Close'].pct_change().dropna()
                    # Weight by holding quantity
                    weighted_returns = returns * (holding['quantity'] * holding['avg_buy_price'])
                    portfolio_returns.append(weighted_returns)
            
            if portfolio_returns:
                # Combine all returns
                all_returns = pd.concat(portfolio_returns)
                # Calculate standard deviation (annualized)
                volatility = all_returns.std() * np.sqrt(252) if len(all_returns) > 1 else 0
                
                if volatility > 0:
                    # Sharpe Ratio = (Return - Risk Free Rate) / Volatility
                    sharpe_ratio = (total_return - risk_free_rate) / volatility
                else:
                    sharpe_ratio = 0
                
                # Sortino Ratio (downside deviation)
                negative_returns = all_returns[all_returns < 0]
                downside_deviation = negative_returns.std() * np.sqrt(252) if len(negative_returns) > 1 else 0
                
                if downside_deviation > 0:
                    sortino_ratio = (total_return - risk_free_rate) / downside_deviation
                else:
                    sortino_ratio = 0
                
                return {
                    'sharpe_ratio': sharpe_ratio,
                    'sortino_ratio': sortino_ratio,
                    'volatility': volatility,
                    'total_return': total_return,
                    'risk_free_rate': risk_free_rate
                }
        
        # Simple Sharpe ratio without historical data (using total return as proxy)
        # Assume 20% annual volatility as default
        default_volatility = 0.20
        sharpe_ratio = (total_return - risk_free_rate) / default_volatility
        
        return {
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': 0,
            'volatility': default_volatility,
            'total_return': total_return,
            'risk_free_rate': risk_free_rate
        }
    
    def calculate_max_drawdown(self, current_prices: Dict[str, float],
                              historical_data: Dict[str, pd.DataFrame] = None) -> Dict[str, Any]:
        """
        Calculate Maximum Drawdown for the portfolio.
        
        Args:
            current_prices: Dictionary with symbol as key and current price as value
            historical_data: Dictionary with symbol as key and historical price DataFrame
            
        Returns:
            Maximum drawdown metrics
        """
        if not historical_data:
            return {'max_drawdown': 0, 'max_drawdown_pct': 0}
        
        holdings = self.get_holdings()
        if not holdings:
            return {'max_drawdown': 0, 'max_drawdown_pct': 0}
        
        # Calculate portfolio value over time
        portfolio_values = []
        
        # Get common date range
        all_dates = set()
        for symbol, data in historical_data.items():
            if symbol in holdings and not data.empty:
                all_dates.update(data.index)
        
        if not all_dates:
            return {'max_drawdown': 0, 'max_drawdown_pct': 0}
        
        sorted_dates = sorted(all_dates)
        
        for date in sorted_dates:
            value = 0
            for symbol, holding in holdings.items():
                if symbol in historical_data and not historical_data[symbol].empty:
                    data = historical_data[symbol]
                    if date in data.index:
                        price = data.loc[date, 'Close']
                        value += holding['quantity'] * price
            portfolio_values.append(value)
        
        if not portfolio_values:
            return {'max_drawdown': 0, 'max_drawdown_pct': 0}
        
        portfolio_values = np.array(portfolio_values)
        
        # Calculate running maximum
        running_max = np.maximum.accumulate(portfolio_values)
        
        # Calculate drawdown
        drawdown = (portfolio_values - running_max) / running_max
        
        # Maximum drawdown
        max_drawdown = drawdown.min()
        max_drawdown_pct = max_drawdown * 100
        
        return {
            'max_drawdown': max_drawdown,
            'max_drawdown_pct': max_drawdown_pct,
            'peak_value': running_max.max(),
            'trough_value': portfolio_values[drawdown.argmin()]
        }
    
    def get_advanced_metrics(self, current_prices: Dict[str, float],
                           historical_data: Dict[str, pd.DataFrame] = None,
                           risk_free_rate: float = 0.02) -> Dict[str, Any]:
        """
        Get all advanced portfolio metrics.
        
        Args:
            current_prices: Dictionary with symbol as key and current price as value
            historical_data: Dictionary with symbol as key and historical price DataFrame
            risk_free_rate: Risk-free rate
            
        Returns:
            Advanced metrics including CAGR, Sharpe ratio, Max Drawdown
        """
        portfolio_summary = self.calculate_portfolio_value(current_prices)
        cagr_data = self.calculate_cagr(current_prices, risk_free_rate)
        sharpe_data = self.calculate_sharpe_ratio(current_prices, historical_data, risk_free_rate)
        drawdown_data = self.calculate_max_drawdown(current_prices, historical_data)
        
        return {
            'portfolio_value': portfolio_summary['total_value'],
            'total_cost': portfolio_summary['total_cost'],
            'total_gain_loss': portfolio_summary['total_gain_loss'],
            'total_gain_loss_pct': portfolio_summary['total_gain_loss_pct'],
            'cagr': cagr_data.get('cagr', 0),
            'sharpe_ratio': sharpe_data.get('sharpe_ratio', 0),
            'sortino_ratio': sharpe_data.get('sortino_ratio', 0),
            'max_drawdown_pct': drawdown_data.get('max_drawdown_pct', 0),
            'volatility': sharpe_data.get('volatility', 0),
            'num_holdings': portfolio_summary['num_holdings']
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
