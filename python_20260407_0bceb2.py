"""Invoice management and automation"""

import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
import hashlib

class InvoiceManager:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def generate_pending_invoices(self) -> List[Dict]:
        """Generate invoices for recurring billing"""
        
        recurring_customers = self._get_recurring_customers()
        generated_invoices = []
        
        for customer in recurring_customers:
            invoice = self._create_invoice(customer)
            if invoice:
                generated_invoices.append(invoice)
                self._send_invoice(invoice)
                self.logger.info(f"Generated invoice {invoice['invoice_number']} for {customer['name']}")
                
        return generated_invoices
    
    def _get_recurring_customers(self) -> List[Dict]:
        """Get customers with recurring billing setup"""
        # In production, fetch from database
        return [
            {
                'id': 'CUST001',
                'name': 'Acme Corporation',
                'email': 'accounts@acme.com',
                'plan': 'enterprise',
                'amount': 12500.00,
                'billing_day': 1,
                'payment_terms': 30
            },
            {
                'id': 'CUST002',
                'name': 'TechStart Inc',
                'email': 'finance@techstart.com',
                'plan': 'professional',
                'amount': 5400.50,
                'billing_day': 15,
                'payment_terms': 15
            },
            {
                'id': 'CUST003',
                'name': 'Global Solutions Ltd',
                'email': 'ap@globalsolutions.com',
                'plan': 'enterprise',
                'amount': 8750.00,
                'billing_day': 20,
                'payment_terms': 45
            }
        ]
    
    def _create_invoice(self, customer: Dict) -> Optional[Dict]:
        """Create invoice for customer"""
        
        # Check if invoice should be generated today
        if datetime.now().day != customer['billing_day']:
            return None
            
        invoice_number = self._generate_invoice_number(customer['id'])
        
        return {
            'invoice_number': invoice_number,
            'customer_id': customer['id'],
            'customer_name': customer['name'],
            'amount': customer['amount'],
            'currency': 'USD',
            'issue_date': datetime.now(),
            'due_date': datetime.now() + timedelta(days=customer['payment_terms']),
            'status': 'pending',
            'items': [
                {
                    'description': f"{customer['plan']} Plan - Monthly Subscription",
                    'quantity': 1,
                    'unit_price': customer['amount'],
                    'total': customer['amount']
                }
            ]
        }
    
    def _generate_invoice_number(self, customer_id: str) -> str:
        """Generate unique invoice number"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_hash = hashlib.md5(f"{customer_id}{timestamp}".encode()).hexdigest()[:6]
        return f"INV-{timestamp}-{unique_hash}"
    
    def _send_invoice(self, invoice: Dict):
        """Send invoice to customer via email"""
        # In production, integrate with email service or accounting software
        self.logger.info(f"Sending invoice {invoice['invoice_number']} to {invoice['customer_name']}")
        
    def track_overdue_invoices(self) -> List[Dict]:
        """Track and flag overdue invoices"""
        
        # In production, fetch all pending invoices from database
        pending_invoices = self._get_pending_invoices()
        
        overdue_invoices = []
        today = datetime.now()
        
        for invoice in pending_invoices:
            if invoice['due_date'] < today:
                days_overdue = (today - invoice['due_date']).days
                invoice['days_overdue'] = days_overdue
                invoice['status'] = 'overdue'
                overdue_invoices.append(invoice)
                
                # Send reminder if overdue
                if days_overdue in [1, 7, 14, 30]:
                    self._send_overdue_reminder(invoice)
                    
        return overdue_invoices
    
    def _get_pending_invoices(self) -> List[Dict]:
        """Get all pending invoices"""
        # In production, fetch from database
        return [
            {
                'invoice_number': 'INV-2024-001',
                'customer_name': 'Acme Corp',
                'amount': 12500.00,
                'due_date': datetime.now() - timedelta(days=5),
                'status': 'pending'
            }
        ]
    
    def _send_overdue_reminder(self, invoice: Dict):
        """Send overdue invoice reminder"""
        self.logger.warning(f"Overdue invoice: {invoice['invoice_number']} - {invoice['days_overdue']} days overdue")
        # Send email to customer
