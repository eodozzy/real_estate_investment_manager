"""
Comprehensive unit tests for Four Pillars analysis system

Tests all Four Pillars calculations with realistic scenarios and edge cases.
"""

import unittest
from decimal import Decimal

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from real_estate_app.analytics.four_pillars import (
    CashFlowCalculator, PrincipalPaydownCalculator, 
    AppreciationCalculator, TaxBenefitsCalculator,
    FourPillarsAnalyzer, FourPillarsResults
)


class TestCashFlowCalculator(unittest.TestCase):
    """Test cases for Cash Flow (Pillar 1) calculations"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.calc = CashFlowCalculator()
        
    def test_basic_cash_flow_calculation(self):
        """Test basic cash flow calculation"""
        annual_income = 24000.0  # $2,000/month
        expenses = {
            'property_taxes': 3600.0,
            'insurance': 1200.0,
            'maintenance': 2400.0,
            'property_management': 1200.0,
            'utilities': 0.0,
            'hoa_fees': 0.0,
            'vacancy_allowance': 1200.0,
            'other_expenses': 0.0
        }
        debt_service = 14400.0  # $1,200/month
        
        result = self.calc.calculate_cash_flow(annual_income, expenses, debt_service)
        
        # Check calculations
        expected_total_expenses = sum(expenses.values())  # $9,600
        expected_noi = annual_income - expected_total_expenses  # $14,400
        expected_cash_flow = expected_noi - debt_service  # $0
        
        self.assertEqual(result.gross_rental_income, 24000.0)
        self.assertEqual(result.operating_expenses, expected_total_expenses)
        self.assertEqual(result.net_operating_income, expected_noi)
        self.assertEqual(result.debt_service, debt_service)
        self.assertEqual(result.annual_cash_flow, expected_cash_flow)
        self.assertEqual(result.monthly_cash_flow, expected_cash_flow / 12)
        
    def test_positive_cash_flow(self):
        """Test scenario with positive cash flow"""
        annual_income = 30000.0
        expenses = {'maintenance': 3000.0, 'taxes': 3600.0}
        debt_service = 18000.0
        
        result = self.calc.calculate_cash_flow(annual_income, expenses, debt_service)
        
        expected_cash_flow = 30000.0 - 6600.0 - 18000.0  # $5,400
        self.assertEqual(result.annual_cash_flow, expected_cash_flow)
        self.assertGreater(result.annual_cash_flow, 0)
        
    def test_negative_cash_flow(self):
        """Test scenario with negative cash flow"""
        annual_income = 18000.0
        expenses = {'maintenance': 3000.0, 'taxes': 3600.0}
        debt_service = 15000.0
        
        result = self.calc.calculate_cash_flow(annual_income, expenses, debt_service)
        
        expected_cash_flow = 18000.0 - 6600.0 - 15000.0  # -$3,600
        self.assertEqual(result.annual_cash_flow, expected_cash_flow)
        self.assertLess(result.annual_cash_flow, 0)
        
    def test_expense_breakdown(self):
        """Test expense breakdown functionality"""
        expenses = self.calc.calculate_operating_expenses(
            property_taxes=3600.0,
            insurance=1200.0,
            maintenance=2400.0,
            property_management=1800.0,
            vacancy_allowance=1200.0
        )
        
        self.assertEqual(expenses['property_taxes'], 3600.0)
        self.assertEqual(expenses['insurance'], 1200.0)
        self.assertEqual(expenses['maintenance'], 2400.0)
        self.assertEqual(expenses['property_management'], 1800.0)
        self.assertEqual(expenses['vacancy_allowance'], 1200.0)
        self.assertEqual(expenses['utilities'], 0.0)
        self.assertEqual(expenses['hoa_fees'], 0.0)
        self.assertEqual(expenses['other_expenses'], 0.0)


class TestPrincipalPaydownCalculator(unittest.TestCase):
    """Test cases for Principal Paydown (Pillar 2) calculations"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.calc = PrincipalPaydownCalculator()
        self.loan_amount = 200000.0
        self.annual_rate = 0.06
        self.term_years = 30
        
    def test_first_year_principal_paydown(self):
        """Test principal paydown for first year"""
        result = self.calc.calculate_principal_paydown(
            self.loan_amount, self.annual_rate, self.term_years, 1
        )
        
        # Beginning balance should equal loan amount
        self.assertEqual(result.beginning_balance, self.loan_amount)
        
        # Ending balance should be less than beginning
        self.assertLess(result.ending_balance, result.beginning_balance)
        
        # Annual paydown should be positive
        self.assertGreater(result.annual_principal_paydown, 0)
        
        # Monthly paydown should be annual / 12
        expected_monthly = result.annual_principal_paydown / 12
        self.assertAlmostEqual(result.monthly_principal_paydown, expected_monthly, places=2)
        
        # In early years, principal paydown should be relatively small
        # (most payment goes to interest)
        self.assertLess(result.annual_principal_paydown, 10000)
        
    def test_later_year_principal_paydown(self):
        """Test principal paydown for later year (more principal, less interest)"""
        year_25_result = self.calc.calculate_principal_paydown(
            self.loan_amount, self.annual_rate, self.term_years, 25
        )
        
        year_1_result = self.calc.calculate_principal_paydown(
            self.loan_amount, self.annual_rate, self.term_years, 1
        )
        
        # Later years should have more principal paydown
        self.assertGreater(
            year_25_result.annual_principal_paydown,
            year_1_result.annual_principal_paydown
        )
        
    def test_final_year_principal_paydown(self):
        """Test principal paydown for final year"""
        result = self.calc.calculate_principal_paydown(
            self.loan_amount, self.annual_rate, self.term_years, 30
        )
        
        # Ending balance should be approximately 0
        self.assertAlmostEqual(result.ending_balance, 0.0, places=0)
        
        # Annual paydown should equal beginning balance
        self.assertAlmostEqual(
            result.annual_principal_paydown, 
            result.beginning_balance, 
            places=0
        )
        
    def test_cumulative_principal_paydown(self):
        """Test cumulative principal paydown calculation"""
        # After 5 years
        paydown_5_years = self.calc.calculate_cumulative_principal_paydown(
            self.loan_amount, self.annual_rate, self.term_years, 5
        )
        
        # After 10 years
        paydown_10_years = self.calc.calculate_cumulative_principal_paydown(
            self.loan_amount, self.annual_rate, self.term_years, 10
        )
        
        # 10 years should have more paydown than 5 years
        self.assertGreater(paydown_10_years, paydown_5_years)
        
        # Full term should equal full loan amount
        paydown_full = self.calc.calculate_cumulative_principal_paydown(
            self.loan_amount, self.annual_rate, self.term_years, 30
        )
        self.assertAlmostEqual(paydown_full, self.loan_amount, places=0)
        
    def test_edge_cases(self):
        """Test edge cases for principal paydown"""
        # Year 0 should return zeros
        result_zero = self.calc.calculate_principal_paydown(
            self.loan_amount, self.annual_rate, self.term_years, 0
        )
        self.assertEqual(result_zero.annual_principal_paydown, 0)
        
        # Year beyond loan term should return zeros
        result_beyond = self.calc.calculate_principal_paydown(
            self.loan_amount, self.annual_rate, self.term_years, 35
        )
        self.assertEqual(result_beyond.annual_principal_paydown, 0)


class TestAppreciationCalculator(unittest.TestCase):
    """Test cases for Appreciation (Pillar 3) calculations"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.calc = AppreciationCalculator()
        
    def test_basic_appreciation_calculation(self):
        """Test basic appreciation calculation"""
        beginning_value = 250000.0
        ending_value = 265000.0
        
        result = self.calc.calculate_appreciation(beginning_value, ending_value)
        
        expected_appreciation = ending_value - beginning_value  # $15,000
        expected_rate = (expected_appreciation / beginning_value) * 100  # 6%
        
        self.assertEqual(result.beginning_value, beginning_value)
        self.assertEqual(result.ending_value, ending_value)
        self.assertEqual(result.annual_appreciation, expected_appreciation)
        self.assertAlmostEqual(result.appreciation_rate, expected_rate, places=2)
        
    def test_multi_year_appreciation(self):
        """Test appreciation calculation over multiple years"""
        beginning_value = 200000.0
        ending_value = 240000.0
        years = 5.0
        
        result = self.calc.calculate_appreciation(beginning_value, ending_value, years)
        
        # Annual appreciation should be total / years
        expected_annual = (ending_value - beginning_value) / years
        self.assertAlmostEqual(result.annual_appreciation, expected_annual, places=2)
        
        # Annualized rate should be compound annual growth rate
        expected_cagr = ((ending_value / beginning_value) ** (1/years) - 1) * 100
        self.assertAlmostEqual(result.annualized_appreciation_rate, expected_cagr, places=1)
        
    def test_negative_appreciation(self):
        """Test negative appreciation (depreciation)"""
        beginning_value = 300000.0
        ending_value = 270000.0
        
        result = self.calc.calculate_appreciation(beginning_value, ending_value)
        
        self.assertLess(result.annual_appreciation, 0)
        self.assertLess(result.appreciation_rate, 0)
        
    def test_zero_appreciation(self):
        """Test zero appreciation"""
        value = 250000.0
        
        result = self.calc.calculate_appreciation(value, value)
        
        self.assertEqual(result.annual_appreciation, 0)
        self.assertEqual(result.appreciation_rate, 0)
        
    def test_future_value_projection(self):
        """Test future value projection"""
        current_value = 200000.0
        annual_rate = 0.03  # 3%
        years = 10
        
        future_value = self.calc.project_future_value(current_value, annual_rate, years)
        
        expected = current_value * ((1 + annual_rate) ** years)
        self.assertAlmostEqual(future_value, expected, places=2)
        
    def test_appreciation_scenarios(self):
        """Test appreciation scenario analysis"""
        current_value = 300000.0
        years = 5
        
        scenarios = self.calc.calculate_appreciation_scenarios(current_value, years)
        
        # Should have default scenarios
        self.assertIn('conservative', scenarios)
        self.assertIn('moderate', scenarios)
        self.assertIn('optimistic', scenarios)
        
        # Conservative should be lowest, optimistic highest
        self.assertLess(scenarios['conservative'], scenarios['moderate'])
        self.assertLess(scenarios['moderate'], scenarios['optimistic'])
        
        # All should be greater than current value (positive appreciation)
        for scenario_value in scenarios.values():
            self.assertGreater(scenario_value, current_value)


class TestTaxBenefitsCalculator(unittest.TestCase):
    """Test cases for Tax Benefits (Pillar 4) calculations"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.calc = TaxBenefitsCalculator()
        
    def test_basic_tax_benefits_calculation(self):
        """Test basic tax benefits calculation"""
        building_value = 200000.0  # Excludes land
        annual_interest = 12000.0
        operating_expenses = 8000.0
        marginal_tax_rate = 0.24  # 24%
        
        result = self.calc.calculate_tax_benefits(
            building_value, annual_interest, operating_expenses, marginal_tax_rate
        )
        
        # Depreciation should be building_value / 27.5 years
        expected_depreciation = building_value / 27.5
        self.assertAlmostEqual(result.depreciation_deduction, expected_depreciation, places=2)
        
        # Interest deduction should equal annual interest
        self.assertEqual(result.interest_deduction, annual_interest)
        
        # Operating expense deductions should equal operating expenses
        self.assertEqual(result.operating_expense_deductions, operating_expenses)
        
        # Total deductions
        expected_total = expected_depreciation + annual_interest + operating_expenses
        self.assertAlmostEqual(result.total_deductions, expected_total, places=2)
        
        # Tax savings
        expected_savings = expected_total * marginal_tax_rate
        self.assertAlmostEqual(result.tax_savings, expected_savings, places=2)
        
        # Tax rate should be converted to percentage
        self.assertAlmostEqual(result.marginal_tax_rate, 24.0, places=1)
        
    def test_building_value_calculation(self):
        """Test building value calculation (excludes land)"""
        total_value = 250000.0
        land_percentage = 0.20  # 20% land
        
        building_value = self.calc.calculate_building_value(total_value, land_percentage)
        
        expected = total_value * (1 - land_percentage)  # $200,000
        self.assertEqual(building_value, expected)
        
    def test_annual_interest_calculation(self):
        """Test annual interest paid calculation"""
        loan_amount = 200000.0
        annual_rate = 0.06
        term_years = 30
        analysis_year = 1
        
        annual_interest = self.calc.calculate_annual_interest_paid(
            loan_amount, annual_rate, term_years, analysis_year
        )
        
        # First year interest should be close to loan_amount * annual_rate
        # (slightly less due to principal payments)
        expected_approximate = loan_amount * annual_rate
        self.assertLess(annual_interest, expected_approximate)
        self.assertGreater(annual_interest, expected_approximate * 0.95)  # Within 5%
        
    def test_different_tax_rates(self):
        """Test tax benefits with different tax rates"""
        building_value = 200000.0
        annual_interest = 10000.0
        operating_expenses = 6000.0
        
        # Low tax rate
        result_low = self.calc.calculate_tax_benefits(
            building_value, annual_interest, operating_expenses, 0.12
        )
        
        # High tax rate
        result_high = self.calc.calculate_tax_benefits(
            building_value, annual_interest, operating_expenses, 0.37
        )
        
        # Higher tax rate should yield higher tax savings
        self.assertGreater(result_high.tax_savings, result_low.tax_savings)
        
        # Deductions should be the same regardless of tax rate
        self.assertEqual(result_low.total_deductions, result_high.total_deductions)


class TestFourPillarsAnalyzer(unittest.TestCase):
    """Test cases for complete Four Pillars analysis"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = FourPillarsAnalyzer()
        
        # Standard test property
        self.property_value = 250000.0
        self.loan_amount = 200000.0
        self.annual_rate = 0.06
        self.term_years = 30
        self.annual_income = 24000.0
        self.operating_expenses = {
            'property_taxes': 3000.0,
            'insurance': 1200.0,
            'maintenance': 2400.0,
            'vacancy_allowance': 1200.0
        }
        
    def test_complete_analysis(self):
        """Test complete Four Pillars analysis"""
        result = self.analyzer.analyze_investment(
            property_value=self.property_value,
            loan_amount=self.loan_amount,
            annual_interest_rate=self.annual_rate,
            loan_term_years=self.term_years,
            annual_rental_income=self.annual_income,
            operating_expenses=self.operating_expenses,
            analysis_year=1,
            ending_property_value=self.property_value * 1.03,  # 3% appreciation
            marginal_tax_rate=0.24,
            total_cash_invested=60000.0
        )
        
        # Check that all pillars are present
        self.assertIsNotNone(result.cash_flow)
        self.assertIsNotNone(result.principal_paydown)
        self.assertIsNotNone(result.appreciation)
        self.assertIsNotNone(result.tax_benefits)
        
        # Check that total return is calculated
        expected_total = (
            result.cash_flow.annual_cash_flow +
            result.principal_paydown.annual_principal_paydown +
            result.appreciation.annual_appreciation +
            result.tax_benefits.tax_savings
        )
        self.assertAlmostEqual(result.total_annual_return, expected_total, places=2)
        
        # Check return percentage
        expected_percentage = (result.total_annual_return / 60000.0) * 100
        self.assertAlmostEqual(result.total_return_percentage, expected_percentage, places=2)
        
    def test_multi_year_analysis(self):
        """Test multi-year Four Pillars analysis"""
        results = self.analyzer.analyze_multi_year(
            property_value=self.property_value,
            loan_amount=self.loan_amount,
            annual_interest_rate=self.annual_rate,
            loan_term_years=self.term_years,
            annual_rental_income=self.annual_income,
            operating_expenses=self.operating_expenses,
            years=5,
            annual_appreciation_rate=0.03
        )
        
        # Should have 5 years of results
        self.assertEqual(len(results), 5)
        
        # Each year should have increasing analysis_year
        for i, result in enumerate(results):
            self.assertEqual(result.analysis_year, i + 1)
            
        # Principal paydown should generally increase over time
        # (more principal, less interest as loan amortizes)
        paydowns = [r.principal_paydown.annual_principal_paydown for r in results]
        self.assertLess(paydowns[0], paydowns[-1])
        
    def test_summary_report(self):
        """Test summary report generation"""
        # Single year result
        result = self.analyzer.analyze_investment(
            property_value=self.property_value,
            loan_amount=self.loan_amount,
            annual_interest_rate=self.annual_rate,
            loan_term_years=self.term_years,
            annual_rental_income=self.annual_income,
            operating_expenses=self.operating_expenses
        )
        
        summary = self.analyzer.create_summary_report(result)
        
        # Check that summary contains expected keys
        expected_keys = [
            'analysis_period', 'total_years', 'average_annual_return',
            'average_return_percentage', 'total_cumulative_return',
            'average_cash_flow', 'average_principal_paydown',
            'average_appreciation', 'average_tax_benefits'
        ]
        
        for key in expected_keys:
            self.assertIn(key, summary)
            
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        # Zero rental income
        result_no_income = self.analyzer.analyze_investment(
            property_value=self.property_value,
            loan_amount=self.loan_amount,
            annual_interest_rate=self.annual_rate,
            loan_term_years=self.term_years,
            annual_rental_income=0.0,
            operating_expenses=self.operating_expenses
        )
        
        # Should have negative cash flow
        self.assertLess(result_no_income.cash_flow.annual_cash_flow, 0)
        
        # No loan (cash purchase)
        result_no_loan = self.analyzer.analyze_investment(
            property_value=self.property_value,
            loan_amount=0.0,
            annual_interest_rate=0.0,
            loan_term_years=30,
            annual_rental_income=self.annual_income,
            operating_expenses=self.operating_expenses
        )
        
        # Should have no debt service or principal paydown
        self.assertEqual(result_no_loan.cash_flow.debt_service, 0)
        self.assertEqual(result_no_loan.principal_paydown.annual_principal_paydown, 0)


class TestFourPillarsRealistic(unittest.TestCase):
    """Test Four Pillars with realistic investment scenarios"""
    
    def test_typical_rental_property(self):
        """Test typical single-family rental property"""
        analyzer = FourPillarsAnalyzer()
        
        # Typical rental property scenario
        result = analyzer.analyze_investment(
            property_value=320000.0,
            loan_amount=256000.0,  # 80% LTV
            annual_interest_rate=0.0675,  # 6.75%
            loan_term_years=30,
            annual_rental_income=28800.0,  # $2,400/month
            operating_expenses={
                'property_taxes': 4800.0,
                'insurance': 1500.0,
                'maintenance': 2880.0,  # 10% of rent
                'property_management': 2880.0,  # 10% of rent
                'vacancy_allowance': 1440.0,  # 5% of rent
                'other_expenses': 500.0
            },
            marginal_tax_rate=0.24,
            total_cash_invested=70000.0  # Down payment + closing costs
        )
        
        # Sanity checks for realistic results
        self.assertGreater(result.cash_flow.net_operating_income, 10000)
        self.assertGreater(result.principal_paydown.annual_principal_paydown, 2000)
        self.assertGreater(result.appreciation.annual_appreciation, 5000)
        self.assertGreater(result.tax_benefits.tax_savings, 3000)
        
        # Total return should be reasonable (5-25%)
        self.assertGreater(result.total_return_percentage, 5.0)
        self.assertLess(result.total_return_percentage, 25.0)
        
    def test_high_end_property(self):
        """Test high-end investment property"""
        analyzer = FourPillarsAnalyzer()
        
        result = analyzer.analyze_investment(
            property_value=650000.0,
            loan_amount=520000.0,  # 80% LTV
            annual_interest_rate=0.07,
            loan_term_years=30,
            annual_rental_income=54000.0,  # $4,500/month
            operating_expenses={
                'property_taxes': 9750.0,  # 1.5% of value
                'insurance': 2400.0,
                'maintenance': 5400.0,  # 10% of rent
                'property_management': 5400.0,  # 10% of rent
                'vacancy_allowance': 2700.0,  # 5% of rent
                'hoa_fees': 1200.0,
                'other_expenses': 1000.0
            },
            marginal_tax_rate=0.32,  # Higher tax bracket
            total_cash_invested=140000.0
        )
        
        # Higher value property should have higher absolute returns
        self.assertGreater(result.appreciation.annual_appreciation, 15000)
        self.assertGreater(result.tax_benefits.tax_savings, 8000)
        
    def test_poor_performing_property(self):
        """Test property with poor performance"""
        analyzer = FourPillarsAnalyzer()
        
        result = analyzer.analyze_investment(
            property_value=180000.0,
            loan_amount=162000.0,  # 90% LTV (high leverage)
            annual_interest_rate=0.08,  # Higher interest rate
            loan_term_years=30,
            annual_rental_income=16800.0,  # $1,400/month (low rent)
            operating_expenses={
                'property_taxes': 2700.0,
                'insurance': 1200.0,
                'maintenance': 3360.0,  # 20% of rent (high maintenance)
                'property_management': 1680.0,  # 10% of rent
                'vacancy_allowance': 1680.0,  # 10% vacancy
                'other_expenses': 800.0
            },
            ending_property_value=180000.0,  # No appreciation
            marginal_tax_rate=0.22,
            total_cash_invested=25000.0
        )
        
        # Should have poor cash flow due to high expenses and debt service
        self.assertLess(result.cash_flow.annual_cash_flow, 1000)
        
        # May have negative total return
        self.assertLess(result.total_return_percentage, 10.0)


if __name__ == '__main__':
    unittest.main()