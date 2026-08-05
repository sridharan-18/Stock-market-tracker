"""
Portfolio management module.
Handles virtual trading, holdings, and portfolio calculations.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Holding:
    """Represents a stock holding."""
    shares: float
    avg_cost: float


@dataclass
class Transaction:
    """Represents a trade transaction."""
    type: str  # 'BUY' or 'SELL'
    symbol: str
    shares: float
    price: float
    total: float
    timestamp: float


@dataclass
class Portfolio:
    """Represents a user's portfolio."""
    cash: float = 10000.0
    holdings: Dict[str, Holding] = field(default_factory=dict)
    transactions: List[Transaction] = field(default_factory=list)
    value_history: List[Dict[str, Any]] = field(default_factory=list)
    
    def calculate_value(self, current_prices: Dict[str, float]) -> float:
        """
        Calculate total portfolio value.
        
        Args:
            current_prices: Dictionary of symbol -> current price
            
        Returns:
            Total portfolio value (cash + holdings)
        """
        holdings_value = 0.0
        for symbol, holding in self.holdings.items():
            if symbol in current_prices and holding.shares > 0:
                holdings_value += current_prices[symbol] * holding.shares
        return self.cash + holdings_value
    
    def buy_stock(self, symbol: str, shares: float, price: float) -> bool:
        """
        Buy shares of a stock.
        
        Args:
            symbol: Stock symbol
            shares: Number of shares to buy
            price: Current price per share
            
        Returns:
            True if successful, False otherwise
        """
        cost = price * shares
        if cost > self.cash:
            return False
        
        # Update cash
        self.cash -= cost
        
        # Update holdings
        if symbol not in self.holdings:
            self.holdings[symbol] = Holding(shares=0, avg_cost=0)
        
        holding = self.holdings[symbol]
        total_shares = holding.shares + shares
        total_cost = (holding.shares * holding.avg_cost) + cost
        holding.avg_cost = total_cost / total_shares
        holding.shares = total_shares
        
        # Record transaction
        self.transactions.append(Transaction(
            type='BUY',
            symbol=symbol,
            shares=shares,
            price=price,
            total=cost,
            timestamp=datetime.now().timestamp()
        ))
        
        return True
    
    def sell_stock(self, symbol: str, shares: float, price: float) -> bool:
        """
        Sell shares of a stock.
        
        Args:
            symbol: Stock symbol
            shares: Number of shares to sell
            price: Current price per share
            
        Returns:
            True if successful, False otherwise
        """
        if symbol not in self.holdings or self.holdings[symbol].shares < shares:
            return False
        
        proceeds = price * shares
        
        # Update cash
        self.cash += proceeds
        
        # Update holdings
        holding = self.holdings[symbol]
        holding.shares -= shares
        if holding.shares == 0:
            del self.holdings[symbol]
        
        # Record transaction
        self.transactions.append(Transaction(
            type='SELL',
            symbol=symbol,
            shares=shares,
            price=price,
            total=proceeds,
            timestamp=datetime.now().timestamp()
        ))
        
        return True
    
    def track_value(self, current_prices: Dict[str, float]) -> None:
        """
        Record current portfolio value for history tracking.
        
        Args:
            current_prices: Dictionary of symbol -> current price
        """
        value = self.calculate_value(current_prices)
        self.value_history.append({
            'timestamp': datetime.now().timestamp(),
            'value': value
        })
        
        # Keep only last 30 days
        thirty_days_ago = datetime.now().timestamp() - (30 * 24 * 60 * 60)
        self.value_history = [h for h in self.value_history if h['timestamp'] > thirty_days_ago]
    
    def get_holdings_summary(self, current_prices: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Get summary of all holdings.
        
        Args:
            current_prices: Dictionary of symbol -> current price
            
        Returns:
            List of holding summaries
        """
        summary = []
        for symbol, holding in self.holdings.items():
            if symbol in current_prices:
                current_value = current_prices[symbol] * holding.shares
                cost_basis = holding.shares * holding.avg_cost
                gain = current_value - cost_basis
                gain_pct = (gain / cost_basis * 100) if cost_basis > 0 else 0
                
                summary.append({
                    'symbol': symbol,
                    'shares': holding.shares,
                    'avg_cost': holding.avg_cost,
                    'current_price': current_prices[symbol],
                    'current_value': current_value,
                    'gain': gain,
                    'gain_pct': gain_pct
                })
        return summary
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert portfolio to dictionary for serialization."""
        return {
            'cash': self.cash,
            'holdings': {k: {'shares': v.shares, 'avg_cost': v.avg_cost} 
                        for k, v in self.holdings.items()},
            'transactions': [
                {
                    'type': t.type,
                    'symbol': t.symbol,
                    'shares': t.shares,
                    'price': t.price,
                    'total': t.total,
                    'timestamp': t.timestamp
                }
                for t in self.transactions
            ],
            'value_history': self.value_history
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Portfolio':
        """Create portfolio from dictionary."""
        portfolio = cls(cash=data.get('cash', 10000.0))
        
        for symbol, holding_data in data.get('holdings', {}).items():
            portfolio.holdings[symbol] = Holding(
                shares=holding_data['shares'],
                avg_cost=holding_data['avg_cost']
            )
        
        for tx_data in data.get('transactions', []):
            portfolio.transactions.append(Transaction(
                type=tx_data['type'],
                symbol=tx_data['symbol'],
                shares=tx_data['shares'],
                price=tx_data['price'],
                total=tx_data['total'],
                timestamp=tx_data['timestamp']
            ))
        
        portfolio.value_history = data.get('value_history', [])
        return portfolio
