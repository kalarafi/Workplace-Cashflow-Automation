"""Cash flow calculation and forecasting engine"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

class CashFlowCalculator:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def calculate_daily_cashflow(self, incoming: List[Dict], outgoing: List[Dict]) -> Dict:
        """Calculate net daily cash flow"""
        
        total_incoming = sum(payment['amount'] for payment in incoming)
        total_outgoing = sum(payment['amount'] for payment in outgoing)
        net_cashflow = total_incoming - total_outgoing
        
        return {
            'date': datetime.now().date(),
            'total_incoming': total_incoming,
            'total_outgoing': total_outgoing,
            'net_cashflow': net_cashflow,
            'incoming_count': len(incoming),
            'outgoing_count': len(outgoing),
            'average_transaction': (total_incoming + total_outgoing) / (len(incoming) + len(outgoing)) if (incoming or outgoing) else 0
        }
    
    def forecast_cashflow(self, days: int = 90) -> pd.DataFrame:
        """Generate cash flow forecast using time series analysis"""
        
        # Simulate historical data (in production, this would come from database)
        historical_days = 365
        dates = pd.date_range(end=datetime.now(), periods=historical_days, freq='D')
        
        # Generate realistic cash flow patterns
        np.random.seed(42)
        base_inflow = 50000
        base_outflow = 45000
        seasonality = np.sin(np.linspace(0, 2*np.pi, historical_days)) * 10000
        noise = np.random.normal(0, 5000, historical_days)
        
        inflows = base_inflow + seasonality + noise
        outflows = base_outflow + seasonality * 0.8 + np.random.normal(0, 4000, historical_days)
        
        historical_df = pd.DataFrame({
            'date': dates,
            'inflow': np.maximum(inflows, 0),
            'outflow': np.maximum(outflows, 0)
        })
        
        # Simple moving average forecast
        forecast_dates = pd.date_range(start=datetime.now(), periods=days+1, freq='D')[1:]
        
        inflow_forecast = []
        outflow_forecast = []
        
        for i, date in enumerate(forecast_dates):
            # Use last 30 days average with some trend
            lookback = historical_df.tail(30)
            trend_factor = 1 + (i * 0.001)  # Slight upward trend
            
            forecast_inflow = lookback['inflow'].mean() * trend_factor
            forecast_outflow = lookback['outflow'].mean() * trend_factor
            
            inflow_forecast.append(forecast_inflow)
            outflow_forecast.append(forecast_outflow)
        
        forecast_df = pd.DataFrame({
            'date': forecast_dates,
            'forecasted_inflow': inflow_forecast,
            'forecasted_outflow': outflow_forecast,
            'net_forecast': np.array(inflow_forecast) - np.array(outflow_forecast)
        })
        
        return forecast_df
    
    def calculate_ratios(self, cashflow_data: pd.DataFrame) -> Dict:
        """Calculate key financial ratios"""
        
        operating_cashflow = cashflow_data['inflow'].sum() - cashflow_data['outflow'].sum()
        current_assets = 500000  # This would come from accounting system
        current_liabilities = 300000
        
        return {
            'operating_cashflow_ratio': operating_cashflow / current_liabilities if current_liabilities > 0 else 0,
            'current_ratio': current_assets / current_liabilities if current_liabilities > 0 else 0,
            'cashflow_margin': (operating_cashflow / cashflow_data['inflow'].sum()) if cashflow_data['inflow'].sum() > 0 else 0,
            'cash_conversion_cycle': self._calculate_cash_conversion_cycle()
        }
    
    def _calculate_cash_conversion_cycle(self) -> float:
        """Calculate cash conversion cycle in days"""
        # This would integrate with inventory, AR, AP systems
        days_inventory_outstanding = 45
        days_sales_outstanding = 30
        days_payables_outstanding = 35
        
        return days_inventory_outstanding + days_sales_outstanding - days_payables_outstanding
