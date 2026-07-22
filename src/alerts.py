"""
Alerts and notifications module.
Handles price threshold alerts and daily summaries.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Alert:
    """Represents a price alert for a stock."""
    above: Optional[float] = None
    below: Optional[float] = None


@dataclass
class TriggeredAlert:
    """Represents a triggered alert."""
    symbol: str
    price: float
    alert: Alert
    timestamp: float
    message: str


@dataclass
class DailySummary:
    """Represents a daily portfolio summary."""
    date: str
    portfolio_value: float
    total_return: float
    return_percent: float
    holdings: List[Dict[str, Any]]
    cash: float


class AlertManager:
    """Manages price alerts and notifications."""
    
    def __init__(self):
        self.alerts: Dict[str, Alert] = {}
        self.triggered_alerts: List[TriggeredAlert] = []
        self.daily_summary: Optional[DailySummary] = None
    
    def set_alert(self, symbol: str, above: Optional[float] = None, 
                  below: Optional[float] = None) -> None:
        """
        Set price alert for a stock.
        
        Args:
            symbol: Stock symbol
            above: Alert if price goes above this value
            below: Alert if price drops below this value
        """
        if above is None and below is None:
            if symbol in self.alerts:
                del self.alerts[symbol]
        else:
            self.alerts[symbol] = Alert(above=above, below=below)
    
    def check_alerts(self, current_prices: Dict[str, float]) -> List[TriggeredAlert]:
        """
        Check if any alerts should be triggered.
        
        Args:
            current_prices: Dictionary of symbol -> current price
            
        Returns:
            List of newly triggered alerts
        """
        new_alerts = []
        
        for symbol, alert in self.alerts.items():
            if symbol not in current_prices:
                continue
            
            price = current_prices[symbol]
            triggered = False
            message = ''
            
            if alert.above and price >= alert.above:
                message = f"{symbol} reached ${price:.2f} (above threshold ${alert.above:.2f})"
                triggered = True
            elif alert.below and price <= alert.below:
                message = f"{symbol} dropped to ${price:.2f} (below threshold ${alert.below:.2f})"
                triggered = True
            
            if triggered:
                triggered_alert = TriggeredAlert(
                    symbol=symbol,
                    price=price,
                    alert=alert,
                    timestamp=datetime.now().timestamp(),
                    message=message
                )
                self.triggered_alerts.append(triggered_alert)
                new_alerts.append(triggered_alert)
                
                # Keep only last 50 triggered alerts
                if len(self.triggered_alerts) > 50:
                    self.triggered_alerts.pop(0)
        
        return new_alerts
    
    def generate_daily_summary(self, portfolio_value: float, initial_cash: float,
                             holdings_summary: List[Dict[str, Any]], 
                             current_cash: float) -> DailySummary:
        """
        Generate daily portfolio summary.
        
        Args:
            portfolio_value: Current portfolio value
            initial_cash: Initial cash investment
            holdings_summary: Summary of current holdings
            current_cash: Current cash balance
            
        Returns:
            DailySummary object
        """
        total_return = portfolio_value - initial_cash
        return_percent = (total_return / initial_cash * 100) if initial_cash > 0 else 0
        
        self.daily_summary = DailySummary(
            date=datetime.now().isoformat(),
            portfolio_value=portfolio_value,
            total_return=total_return,
            return_percent=return_percent,
            holdings=holdings_summary,
            cash=current_cash
        )
        
        return self.daily_summary
    
    def get_alert_message(self, alert: TriggeredAlert) -> str:
        """Get formatted alert message."""
        return alert.message
    
    def get_summary_message(self, summary: DailySummary) -> str:
        """Get formatted daily summary message."""
        direction = '+' if summary.return_percent >= 0 else ''
        return (f"Daily Summary: Portfolio ${summary.portfolio_value:.2f} "
                f"({direction}{summary.return_percent:.2f}%)")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert alert manager to dictionary for serialization."""
        return {
            'alerts': {
                k: {'above': v.above, 'below': v.below}
                for k, v in self.alerts.items()
            },
            'triggered_alerts': [
                {
                    'symbol': a.symbol,
                    'price': a.price,
                    'alert': {'above': a.alert.above, 'below': a.alert.below},
                    'timestamp': a.timestamp,
                    'message': a.message
                }
                for a in self.triggered_alerts
            ],
            'daily_summary': {
                'date': self.daily_summary.date,
                'portfolio_value': self.daily_summary.portfolio_value,
                'total_return': self.daily_summary.total_return,
                'return_percent': self.daily_summary.return_percent,
                'holdings': self.daily_summary.holdings,
                'cash': self.daily_summary.cash
            } if self.daily_summary else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AlertManager':
        """Create alert manager from dictionary."""
        manager = cls()
        
        for symbol, alert_data in data.get('alerts', {}).items():
            manager.alerts[symbol] = Alert(
                above=alert_data.get('above'),
                below=alert_data.get('below')
            )
        
        for alert_data in data.get('triggered_alerts', []):
            alert_obj = Alert(
                above=alert_data['alert']['above'],
                below=alert_data['alert']['below']
            )
            manager.triggered_alerts.append(TriggeredAlert(
                symbol=alert_data['symbol'],
                price=alert_data['price'],
                alert=alert_obj,
                timestamp=alert_data['timestamp'],
                message=alert_data['message']
            ))
        
        summary_data = data.get('daily_summary')
        if summary_data:
            manager.daily_summary = DailySummary(
                date=summary_data['date'],
                portfolio_value=summary_data['portfolio_value'],
                total_return=summary_data['total_return'],
                return_percent=summary_data['return_percent'],
                holdings=summary_data['holdings'],
                cash=summary_data['cash']
            )
        
        return manager
