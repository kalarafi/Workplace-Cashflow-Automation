#!/usr/bin/env python3
"""
Cash Flow Automation System
Main entry point for automating company cash flow operations
"""

import logging
import sys
from datetime import datetime
from cashflow_engine.cashflow_calculator import CashFlowCalculator
from cashflow_engine.payment_processor import PaymentProcessor
from cashflow_engine.invoice_manager import InvoiceManager
from cashflow_engine.reporting import ReportingEngine
import yaml

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'logs/cashflow_{datetime.now().strftime("%Y%m%d")}.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def load_config():
    """Load configuration from YAML file"""
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)

def main():
    """Main execution function"""
    logger = setup_logging()
    logger.info("Starting Cash Flow Automation System")
    
    try:
        # Load configuration
        config = load_config()
        
        # Initialize components
        calculator = CashFlowCalculator(config)
        payment_processor = PaymentProcessor(config)
        invoice_manager = InvoiceManager(config)
        reporting = ReportingEngine(config)
        
        # Run daily cash flow operations
        logger.info("Processing daily cash flow operations...")
        
        # Generate pending invoices
        pending_invoices = invoice_manager.generate_pending_invoices()
        logger.info(f"Generated {len(pending_invoices)} pending invoices")
        
        # Process incoming payments
        incoming_payments = payment_processor.process_incoming_payments()
        logger.info(f"Processed {len(incoming_payments)} incoming payments")
        
        # Process outgoing payments
        outgoing_payments = payment_processor.process_outgoing_payments()
        logger.info(f"Processed {len(outgoing_payments)} outgoing payments")
        
        # Calculate cash flow metrics
        cashflow_metrics = calculator.calculate_daily_cashflow(
            incoming_payments, 
            outgoing_payments
        )
        
        # Generate reports
        reporting.generate_daily_report(cashflow_metrics)
        reporting.generate_forecast(calculator.forecast_cashflow(days=90))
        
        # Send notifications
        if cashflow_metrics['net_cashflow'] < config['alerts']['min_cash_threshold']:
            payment_processor.send_alert("Low cash balance warning!", cashflow_metrics)
        
        logger.info("Cash flow automation completed successfully")
        
    except Exception as e:
        logger.error(f"Error in cash flow automation: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()