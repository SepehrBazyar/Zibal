from django.test import TestCase
from .models import Transaction

# Create your tests here.
class TestTransaction(TestCase):
    def test_count_monthly(self):
        result = Transaction.result('count', 'monthly')
        self.assertEqual(result[0]['value'], 923)
    
    def test_count_weekly(self):
        result = Transaction.result('count', 'weekly')
        self.assertEqual(result[0]['value'], 101)

    def test_count_daily(self):
        result = Transaction.result('count', 'daily')
        self.assertEqual(result[0]['value'], 101)

    def test_amount_monthly(self):
        result = Transaction.result('amount', 'monthly')
        self.assertEqual(result[0]['value'], 43_168_459_015)

    def test_amount_weekly(self):
        result = Transaction.result('amount', 'weekly')
        self.assertEqual(result[0]['value'], 5_071_732_714)

    def test_amount_daily(self):
        result = Transaction.result('amount', 'daily')
        self.assertEqual(result[0]['value'], 5_071_732_714)

    def test_count_monthly_merchant(self):
        result = Transaction.result('count', 'monthly', '5b086ecdf92ea126d079275d')
        self.assertEqual(result[0]['value'], 264)
    
    def test_count_weekly_merchant(self):
        result = Transaction.result('count', 'weekly', '5b086ecdf92ea126d079275d')
        self.assertEqual(result[0]['value'], 11)

    def test_count_daily_merchant(self):
        result = Transaction.result('count', 'daily', '5b086ecdf92ea126d079275d')
        self.assertEqual(result[0]['value'], 11)

    def test_amount_monthly_merchant(self):
        result = Transaction.result('amount', 'monthly', '5b086ecdf92ea126d079275d')
        self.assertEqual(result[0]['value'], 12_326_824_528)

    def test_amount_weekly_merchant(self):
        result = Transaction.result('amount', 'weekly', '5b086ecdf92ea126d079275d')
        self.assertEqual(result[0]['value'], 595_187_577)

    def test_amount_daily_merchant(self):
        result = Transaction.result('amount', 'daily', '5b086ecdf92ea126d079275d')
        self.assertEqual(result[0]['value'], 595_187_577)
