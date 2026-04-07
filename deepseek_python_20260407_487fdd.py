"""Reporting and analytics engine"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging
import json

class ReportingEngine:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def generate_daily_report(self, cashflow_metrics: Dict):
        """Generate daily cash flow report"""
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'type': 'daily_cashflow',
            'metrics': cashflow_metrics,
            'summary': self._generate_summary(cashflow_metrics)
        }
        
        # Save report
        self._save_report(report, f"daily_report_{datetime.now().strftime('%Y%m%d')}.json")
        
        # Generate visualization
        self._create_cashflow_chart(cashflow_metrics)
        
        return report
    
    def generate_forecast(self, forecast_data: pd.DataFrame):
        """Generate cash flow forecast report"""
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'type': 'cashflow_forecast',
            'forecast_period_days': len(forecast_data),
            'total_forecasted_inflow': forecast_data['forecasted_inflow'].sum(),
            'total_forecasted_outflow': forecast_data['forecasted_outflow'].sum(),
            'net_forecast': forecast_data['net_forecast'].sum(),
            'peak_balance_date': forecast_data.loc[forecast_data['net_forecast'].idxmax(), 'date'].isoformat(),
            'lowest_balance_date': forecast_data.loc[forecast_data['net_forecast'].idxmin(), 'date'].isoformat()
        }
        
        self._save_report(report, f"forecast_{datetime.now().strftime('%Y%m%d')}.json")
        self._plot_forecast(forecast_data)
        
        return report
    
    def _generate_summary(self, metrics: Dict) -> str:
        """Generate human-readable summary"""
        
        if metrics['net_cashflow'] > 0:
            status = "positive"
            recommendation = "Consider investing excess cash"
        else:
            status = "negative"
            recommendation = "Review expenses and accelerate receivables"
            
        return f"Daily cash flow is {status} with net ${metrics['net_cashflow']:.2f}. {recommendation}"
    
    def _save_report(self, report: Dict, filename: str):
        """Save report to file"""
        with open(f"reports/{filename}", 'w') as f:
            json.dump(report, f, indent=2, default=str)
        self.logger.info(f"Report saved: {filename}")
    
    def _create_cashflow_chart(self, metrics: Dict):
        """Create cash flow visualization"""
        
        categories = ['Incoming', 'Outgoing', 'Net']
        values = [metrics['total_incoming'], metrics['total_outgoing'], metrics['net_cashflow']]
        colors = ['green', 'red', 'blue' if metrics['net_cashflow'] >= 0 else 'orange']
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(categories, values, color=colors)
        plt.title(f'Daily Cash Flow - {metrics["date"]}')
        plt.ylabel('Amount ($)')
        plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + abs(bar.get_height())*0.01,
                    f'${value:,.2f}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(f'reports/cashflow_chart_{datetime.now().strftime("%Y%m%d")}.png')
        plt.close()
    
    def _plot_forecast(self, forecast_df: pd.DataFrame):
        """Plot forecast visualization"""
        
        plt.figure(figsize=(12, 6))
        
        plt.plot(forecast_df['date'], forecast_df['forecasted_inflow'], 
                label='Forecasted Inflow', marker='o', linewidth=2)
        plt.plot(forecast_df['date'], forecast_df['forecasted_outflow'], 
                label='Forecasted Outflow', marker='s', linewidth=2)
        plt.plot(forecast_df['date'], forecast_df['net_forecast'], 
                label='Net Forecast', marker='^', linewidth=2, linestyle='--')
        
        plt.xlabel('Date')
        plt.ylabel('Amount ($)')
        plt.title('90-Day Cash Flow Forecast')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plt.savefig(f'reports/forecast_{datetime.now().strftime("%Y%m%d")}.png')
        plt.close()