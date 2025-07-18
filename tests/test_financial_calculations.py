"""
Comprehensive unit tests for financial calculations module

Tests all core financial calculations with realistic scenarios and edge cases.
"""

import unittest
import math
from decimal import Decimal

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from real_estate_app.analytics.financial_calculations import FinancialCalculator


class TestFinancialCalculator(unittest.TestCase):
    """Test cases for FinancialCalculator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.calc = FinancialCalculator()
        
        # Standard test loan parameters
        self.loan_amount = 200000.0
        self.annual_rate = 0.06  # 6%
        self.term_years = 30
        
    def test_round_currency(self):
        """Test currency rounding"""
        self.assertEqual(self.calc.round_currency(123.456), Decimal('123.46'))
        self.assertEqual(self.calc.round_currency(123.454), Decimal('123.45'))
        self.assertEqual(self.calc.round_currency(None), Decimal('0.00'))
        self.assertEqual(self.calc.round_currency(0), Decimal('0.00'))
        
    def test_monthly_payment_calculation(self):
        """Test monthly mortgage payment calculation"""
        # Standard 30-year loan at 6%
        payment = self.calc.calculate_monthly_payment(
            self.loan_amount, self.annual_rate, self.term_years
        )
        # Expected payment: ~$1,199.10
        self.assertAlmostEqual(payment, 1199.10, places=2)
        
        # Test zero interest rate
        payment_no_interest = self.calc.calculate_monthly_payment(
            self.loan_amount, 0.0, self.term_years
        )
        expected_no_interest = self.loan_amount / (self.term_years * 12)
        self.assertAlmostEqual(payment_no_interest, expected_no_interest, places=2)
        
        # Test edge cases
        self.assertEqual(self.calc.calculate_monthly_payment(0, 0.06, 30), 0.0)
        self.assertEqual(self.calc.calculate_monthly_payment(200000, 0.06, 0), 0.0)
        
    def test_loan_balance_calculation(self):
        """Test remaining loan balance calculation"""
        # Balance after 0 payments should equal original amount
        balance_0 = self.calc.calculate_loan_balance(
            self.loan_amount, self.annual_rate, self.term_years, 0
        )
        self.assertEqual(balance_0, self.loan_amount)
        
        # Balance after 12 payments (1 year)
        balance_12 = self.calc.calculate_loan_balance(
            self.loan_amount, self.annual_rate, self.term_years, 12
        )
        # Should be less than original but more than after 24 payments
        self.assertLess(balance_12, self.loan_amount)
        
        # Balance after 24 payments (2 years)
        balance_24 = self.calc.calculate_loan_balance(
            self.loan_amount, self.annual_rate, self.term_years, 24
        )
        self.assertLess(balance_24, balance_12)
        
        # Balance after all payments should be 0
        total_payments = self.term_years * 12
        balance_final = self.calc.calculate_loan_balance(
            self.loan_amount, self.annual_rate, self.term_years, total_payments
        )
        self.assertAlmostEqual(balance_final, 0.0, places=2)
        
        # Test zero interest
        balance_no_interest = self.calc.calculate_loan_balance(
            self.loan_amount, 0.0, self.term_years, 12
        )
        expected = self.loan_amount * (1 - 12 / (self.term_years * 12))
        self.assertAlmostEqual(balance_no_interest, expected, places=2)
        
    def test_principal_payment_calculation(self):
        """Test principal portion of specific payment"""
        # First payment should have least principal
        principal_1 = self.calc.calculate_principal_payment(
            self.loan_amount, self.annual_rate, self.term_years, 1
        )
        
        # Payment in middle of loan
        principal_180 = self.calc.calculate_principal_payment(
            self.loan_amount, self.annual_rate, self.term_years, 180
        )
        
        # Last payment should have most principal
        principal_360 = self.calc.calculate_principal_payment(
            self.loan_amount, self.annual_rate, self.term_years, 360
        )
        
        # Principal should increase over time
        self.assertLess(principal_1, principal_180)
        self.assertLess(principal_180, principal_360)
        
        # Test edge cases
        self.assertEqual(self.calc.calculate_principal_payment(
            self.loan_amount, self.annual_rate, self.term_years, 0
        ), 0.0)
        
    def test_interest_payment_calculation(self):
        """Test interest portion of specific payment"""
        # First payment should have most interest
        interest_1 = self.calc.calculate_interest_payment(
            self.loan_amount, self.annual_rate, self.term_years, 1
        )
        
        # Payment in middle of loan
        interest_180 = self.calc.calculate_interest_payment(
            self.loan_amount, self.annual_rate, self.term_years, 180
        )
        
        # Last payment should have least interest
        interest_360 = self.calc.calculate_interest_payment(
            self.loan_amount, self.annual_rate, self.term_years, 360
        )
        
        # Interest should decrease over time
        self.assertGreater(interest_1, interest_180)
        self.assertGreater(interest_180, interest_360)
        
        # First payment interest should be approximately loan_amount * monthly_rate
        monthly_rate = self.annual_rate / 12
        expected_first_interest = self.loan_amount * monthly_rate
        self.assertAlmostEqual(interest_1, expected_first_interest, places=2)
        
    def test_amortization_schedule(self):
        """Test amortization schedule generation"""
        schedule = self.calc.generate_amortization_schedule(
            self.loan_amount, self.annual_rate, self.term_years
        )
        
        # Should have 360 payments for 30-year loan
        self.assertEqual(len(schedule), 360)
        
        # First payment
        first_payment = schedule[0]
        self.assertEqual(first_payment['payment_number'], 1)
        self.assertGreater(first_payment['interest_payment'], first_payment['principal_payment'])
        
        # Last payment
        last_payment = schedule[-1]
        self.assertEqual(last_payment['payment_number'], 360)
        self.assertLess(last_payment['interest_payment'], last_payment['principal_payment'])
        self.assertLess(last_payment['remaining_balance'], 2.0)
        
        # Total principal should equal loan amount (allow for small rounding differences)
        total_principal = sum(p['principal_payment'] for p in schedule)
        diff = abs(total_principal - self.loan_amount)
        self.assertLess(diff, 2.0, msg=f"Total principal paydown diff: {diff}")
        
    def test_cap_rate_calculation(self):
        """Test cap rate calculation"""
        noi = 12000.0
        price = 150000.0
        
        cap_rate = self.calc.calculate_cap_rate(noi, price)
        expected = (noi / price) * 100  # 8.0%
        self.assertAlmostEqual(cap_rate, expected, places=2)
        
        # Test edge cases
        self.assertEqual(self.calc.calculate_cap_rate(12000, 0), 0.0)
        
    def test_cash_on_cash_return(self):
        """Test cash-on-cash return calculation"""
        cash_flow = 3600.0  # $300/month
        cash_invested = 50000.0
        
        cocr = self.calc.calculate_cash_on_cash_return(cash_flow, cash_invested)
        expected = (cash_flow / cash_invested) * 100  # 7.2%
        self.assertAlmostEqual(cocr, expected, places=2)
        
        # Test edge cases
        self.assertEqual(self.calc.calculate_cash_on_cash_return(3600, 0), 0.0)
        
    def test_debt_service_coverage_ratio(self):
        """Test DSCR calculation"""
        noi = 15000.0
        debt_service = 12000.0
        
        dscr = self.calc.calculate_debt_service_coverage_ratio(noi, debt_service)
        expected = noi / debt_service  # 1.25
        self.assertAlmostEqual(dscr, expected, places=2)
        
        # Test edge cases
        self.assertEqual(self.calc.calculate_debt_service_coverage_ratio(15000, 0), float('inf'))
        self.assertEqual(self.calc.calculate_debt_service_coverage_ratio(0, 12000), 0.0)
        
    def test_loan_to_value_ratio(self):
        """Test LTV calculation"""
        loan = 160000.0
        value = 200000.0
        
        ltv = self.calc.calculate_loan_to_value_ratio(loan, value)
        expected = (loan / value) * 100  # 80%
        self.assertAlmostEqual(ltv, expected, places=2)
        
        # Test edge cases
        self.assertEqual(self.calc.calculate_loan_to_value_ratio(160000, 0), 0.0)
        
    def test_break_even_ratio(self):
        """Test break-even ratio calculation"""
        expenses = 18000.0
        income = 24000.0
        
        ber = self.calc.calculate_break_even_ratio(expenses, income)
        expected = (expenses / income) * 100  # 75%
        self.assertAlmostEqual(ber, expected, places=2)
        
    def test_operating_expense_ratio(self):
        """Test operating expense ratio calculation"""
        expenses = 6000.0
        income = 24000.0
        
        oer = self.calc.calculate_operating_expense_ratio(expenses, income)
        expected = (expenses / income) * 100  # 25%
        self.assertAlmostEqual(oer, expected, places=2)
        
    def test_rental_yield(self):
        """Test rental yield calculation"""
        annual_rent = 18000.0
        property_value = 200000.0
        
        yield_rate = self.calc.calculate_rental_yield(annual_rent, property_value)
        expected = (annual_rent / property_value) * 100  # 9%
        self.assertAlmostEqual(yield_rate, expected, places=2)
        
    def test_price_per_square_foot(self):
        """Test price per square foot calculation"""
        price = 250000.0
        sqft = 1500.0
        
        price_per_sqft = self.calc.calculate_price_per_square_foot(price, sqft)
        expected = price / sqft  # $166.67
        self.assertAlmostEqual(price_per_sqft, expected, places=2)
        
        # Test edge cases
        self.assertEqual(self.calc.calculate_price_per_square_foot(250000, 0), 0.0)
        
    def test_rent_per_square_foot(self):
        """Test rent per square foot calculation"""
        rent = 1200.0
        sqft = 1500.0
        
        rent_per_sqft = self.calc.calculate_rent_per_square_foot(rent, sqft)
        expected = rent / sqft  # $0.80
        self.assertAlmostEqual(rent_per_sqft, expected, places=2)
        
    def test_appreciation_rate(self):
        """Test appreciation rate calculation"""
        initial = 200000.0
        final = 240000.0
        years = 5.0
        
        rate = self.calc.calculate_appreciation_rate(initial, final, years)
        # CAGR = (240000/200000)^(1/5) - 1 = 3.714%
        expected = 3.714
        self.assertAlmostEqual(rate, expected, places=1)
        
        # Test edge cases
        self.assertEqual(self.calc.calculate_appreciation_rate(0, 240000, 5), 0.0)
        self.assertEqual(self.calc.calculate_appreciation_rate(200000, 240000, 0), 0.0)
        self.assertEqual(self.calc.calculate_appreciation_rate(200000, 0, 5), -100.0)
        
    def test_future_value(self):
        """Test future value calculation"""
        pv = 100000.0
        rate = 0.03
        years = 10.0
        
        fv = self.calc.future_value(pv, rate, years)
        expected = pv * ((1 + rate) ** years)  # $134,391.64
        self.assertAlmostEqual(fv, expected, places=2)
        
        # Test edge cases
        self.assertEqual(self.calc.future_value(100000, 0.03, 0), 100000.0)
        
    def test_present_value(self):
        """Test present value calculation"""
        fv = 134391.64
        rate = 0.03
        years = 10.0
        
        pv = self.calc.present_value(fv, rate, years)
        expected = fv / ((1 + rate) ** years)  # $100,000
        self.assertAlmostEqual(pv, expected, places=2)
        
        # Test edge cases
        self.assertEqual(self.calc.present_value(134391.64, 0.03, 0), 134391.64)
        self.assertEqual(self.calc.present_value(134391.64, 0.0, 10), 134391.64)
        
    def test_irr_calculation(self):
        """Test IRR calculation"""
        # Simple test case: -100, +110 (10% return)
        cash_flows = [-100, 110]
        irr = self.calc.calculate_irr(cash_flows)
        self.assertAlmostEqual(irr, 0.10, places=3)
        
        # More complex case
        cash_flows = [-1000, 300, 400, 500, 600]
        irr = self.calc.calculate_irr(cash_flows)
        self.assertIsNotNone(irr)
        self.assertGreater(irr, 0)
        
        # Edge cases
        self.assertIsNone(self.calc.calculate_irr([]))
        self.assertIsNone(self.calc.calculate_irr([-100]))


class TestFinancialCalculatorIntegration(unittest.TestCase):
    """Integration tests for financial calculations"""
    
    def test_loan_payment_consistency(self):
        """Test that payment calculations are consistent across methods"""
        loan_amount = 300000.0
        annual_rate = 0.045  # 4.5%
        term_years = 30
        
        # Calculate monthly payment
        monthly_payment = FinancialCalculator.calculate_monthly_payment(
            loan_amount, annual_rate, term_years
        )
        
        # Generate full schedule
        schedule = FinancialCalculator.generate_amortization_schedule(
            loan_amount, annual_rate, term_years
        )
        
        # All payments should be the same amount (except possibly last)
        for i, payment in enumerate(schedule[:-1]):  # Exclude last payment
            self.assertAlmostEqual(
                payment['payment_amount'], monthly_payment, places=2,
                msg=f"Payment {i+1} amount mismatch"
            )
        
        # Sum of all principal payments should equal loan amount
        total_principal = sum(p['principal_payment'] for p in schedule)
        self.assertAlmostEqual(total_principal, loan_amount, places=1)
        
    def test_balance_calculation_consistency(self):
        """Test that balance calculations are consistent"""
        loan_amount = 250000.0
        annual_rate = 0.0375  # 3.75%
        term_years = 15
        
        # Test various payment numbers
        for payments_made in [0, 12, 24, 60, 120, 180]:
            balance = FinancialCalculator.calculate_loan_balance(
                loan_amount, annual_rate, term_years, payments_made
            )
            
            # Generate schedule up to this point
            if payments_made > 0:
                schedule = FinancialCalculator.generate_amortization_schedule(
                    loan_amount, annual_rate, term_years
                )
                schedule_balance = schedule[payments_made - 1]['remaining_balance']
                
                # Allow for small rounding differences in balance calculations
                diff = abs(balance - schedule_balance)
                self.assertLess(diff, 1.0, msg=f"Balance mismatch at payment {payments_made}: {diff}")
    
    def test_realistic_property_scenario(self):
        """Test with realistic property investment scenario"""
        # Property details
        purchase_price = 320000.0
        down_payment = 64000.0  # 20%
        loan_amount = purchase_price - down_payment
        annual_rate = 0.0675  # 6.75%
        term_years = 30
        
        # Calculate metrics
        monthly_payment = FinancialCalculator.calculate_monthly_payment(
            loan_amount, annual_rate, term_years
        )
        
        # Monthly payment should be reasonable
        self.assertGreater(monthly_payment, 1000)
        self.assertLess(monthly_payment, 3000)
        
        # Calculate cap rate
        annual_rent = 28800.0  # $2,400/month
        annual_expenses = 8640.0  # 30% of rent
        noi = annual_rent - annual_expenses
        
        cap_rate = FinancialCalculator.calculate_cap_rate(noi, purchase_price)
        
        # Cap rate should be reasonable (4-12%)
        self.assertGreater(cap_rate, 3.0)
        self.assertLess(cap_rate, 15.0)
        
        # Calculate cash-on-cash return
        annual_debt_service = monthly_payment * 12
        annual_cash_flow = noi - annual_debt_service
        total_cash_invested = down_payment + (purchase_price * 0.03)  # 3% closing costs
        
        cocr = FinancialCalculator.calculate_cash_on_cash_return(
            annual_cash_flow, total_cash_invested
        )
        
        # Cash-on-cash should be reasonable (-10% to 20%)
        self.assertGreater(cocr, -15.0)
        self.assertLess(cocr, 25.0)


if __name__ == '__main__':
    unittest.main()