from cashflow_engine.payment_processor import PaymentProcessor

processor = PaymentProcessor(config)
incoming = processor.process_incoming_payments()