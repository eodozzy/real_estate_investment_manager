"""
Four Pillars Total Return Analysis for Real Estate Investments

This module implements the comprehensive Four Pillars analysis system:
1. Cash Flow - Rental income minus operating expenses and debt service
2. Principal Paydown - Loan amortization benefits
3. Appreciation - Property value growth over time
4. Tax Benefits - Depreciation, interest deductions, and expense write-offs

The Four Pillars analysis provides a complete picture of real estate investment returns
by capturing all major sources of investment income and tax benefits.
"""

from typing import Dict, List, Optional, Union, NamedTuple
from datetime import datetime, date
from decimal import Decimal
import logging

from .financial_calculations import FinancialCalculator
from ..config.settings import app_settings

logger = logging.getLogger(__name__)


class CashFlowAnalysis(NamedTuple):
    """Cash flow analysis results"""
    gross_rental_income: float
    operating_expenses: float
    net_operating_income: float
    debt_service: float
    annual_cash_flow: float
    monthly_cash_flow: float
    expense_breakdown: Dict[str, float]


class PrincipalPaydownAnalysis(NamedTuple):
    """Principal paydown analysis results"""
    beginning_balance: float
    ending_balance: float
    annual_principal_paydown: float
    monthly_principal_paydown: float
    total_principal_paid: float
    remaining_balance: float


class AppreciationAnalysis(NamedTuple):
    """Appreciation analysis results"""
    beginning_value: float
    ending_value: float
    annual_appreciation: float
    appreciation_rate: float
    cumulative_appreciation: float
    annualized_appreciation_rate: float


class TaxBenefitsAnalysis(NamedTuple):
    """Tax benefits analysis results"""
    depreciation_deduction: float
    interest_deduction: float
    operating_expense_deductions: float
    total_deductions: float
    tax_savings: float
    marginal_tax_rate: float
    effective_tax_rate: float


class FourPillarsResults(NamedTuple):
    """Complete Four Pillars analysis results"""
    cash_flow: CashFlowAnalysis
    principal_paydown: PrincipalPaydownAnalysis
    appreciation: AppreciationAnalysis
    tax_benefits: TaxBenefitsAnalysis
    total_annual_return: float
    total_return_percentage: float
    analysis_year: int


class CashFlowCalculator:
    """Calculator for Pillar 1: Cash Flow Analysis"""
    
    @staticmethod
    def calculate_cash_flow(
        annual_rental_income: float,
        operating_expenses: Dict[str, float],
        debt_service: float
    ) -> CashFlowAnalysis:
        """
        Calculate annual cash flow after operating expenses and debt service
        
        Args:
            annual_rental_income: Gross annual rental income
            operating_expenses: Dictionary of operating expense categories
            debt_service: Annual debt service (principal + interest)
            
        Returns:
            CashFlowAnalysis with detailed breakdown
        """
        # Calculate total operating expenses
        total_operating_expenses = sum(operating_expenses.values())
        
        # Net Operating Income (NOI)
        net_operating_income = annual_rental_income - total_operating_expenses
        
        # Annual cash flow after debt service
        annual_cash_flow = net_operating_income - debt_service
        
        # Monthly cash flow
        monthly_cash_flow = annual_cash_flow / 12
        
        return CashFlowAnalysis(
            gross_rental_income=float(FinancialCalculator.round_currency(annual_rental_income)),
            operating_expenses=float(FinancialCalculator.round_currency(total_operating_expenses)),
            net_operating_income=float(FinancialCalculator.round_currency(net_operating_income)),
            debt_service=float(FinancialCalculator.round_currency(debt_service)),
            annual_cash_flow=float(FinancialCalculator.round_currency(annual_cash_flow)),
            monthly_cash_flow=float(FinancialCalculator.round_currency(monthly_cash_flow)),
            expense_breakdown={k: float(FinancialCalculator.round_currency(v)) 
                             for k, v in operating_expenses.items()}
        )
    
    @staticmethod
    def calculate_operating_expenses(
        property_taxes: float = 0,
        insurance: float = 0,
        maintenance: float = 0,
        property_management: float = 0,
        utilities: float = 0,
        hoa_fees: float = 0,
        vacancy_allowance: float = 0,
        other_expenses: float = 0
    ) -> Dict[str, float]:
        """
        Calculate and categorize operating expenses
        
        Args:
            property_taxes: Annual property taxes
            insurance: Annual insurance premiums
            maintenance: Annual maintenance and repairs
            property_management: Annual property management fees
            utilities: Annual utilities (if landlord pays)
            hoa_fees: Annual HOA fees
            vacancy_allowance: Annual vacancy allowance
            other_expenses: Other annual operating expenses
            
        Returns:
            Dictionary of operating expense categories
        """
        return {
            'property_taxes': property_taxes,
            'insurance': insurance,
            'maintenance': maintenance,
            'property_management': property_management,
            'utilities': utilities,
            'hoa_fees': hoa_fees,
            'vacancy_allowance': vacancy_allowance,
            'other_expenses': other_expenses
        }


class PrincipalPaydownCalculator:
    """Calculator for Pillar 2: Principal Paydown Analysis"""
    
    @staticmethod
    def calculate_principal_paydown(
        loan_amount: float,
        annual_interest_rate: float,
        loan_term_years: int,
        analysis_year: int
    ) -> PrincipalPaydownAnalysis:
        """
        Calculate principal paydown for a specific year
        
        Args:
            loan_amount: Original loan amount
            annual_interest_rate: Annual interest rate (as decimal)
            loan_term_years: Loan term in years
            analysis_year: Year to analyze (1-based)
            
        Returns:
            PrincipalPaydownAnalysis with paydown details
        """
        if analysis_year <= 0 or analysis_year > loan_term_years:
            return PrincipalPaydownAnalysis(0, 0, 0, 0, 0, 0)
        
        # Calculate beginning balance (end of previous year)
        beginning_payments = (analysis_year - 1) * 12
        beginning_balance = FinancialCalculator.calculate_loan_balance(
            loan_amount, annual_interest_rate, loan_term_years, beginning_payments
        )
        
        # Calculate ending balance (end of current year)
        ending_payments = analysis_year * 12
        ending_balance = FinancialCalculator.calculate_loan_balance(
            loan_amount, annual_interest_rate, loan_term_years, ending_payments
        )
        
        # Annual principal paydown is the difference
        annual_principal_paydown = beginning_balance - ending_balance
        
        # Monthly average
        monthly_principal_paydown = annual_principal_paydown / 12
        
        # Total principal paid to date
        total_principal_paid = loan_amount - ending_balance
        
        return PrincipalPaydownAnalysis(
            beginning_balance=float(FinancialCalculator.round_currency(beginning_balance)),
            ending_balance=float(FinancialCalculator.round_currency(ending_balance)),
            annual_principal_paydown=float(FinancialCalculator.round_currency(annual_principal_paydown)),
            monthly_principal_paydown=float(FinancialCalculator.round_currency(monthly_principal_paydown)),
            total_principal_paid=float(FinancialCalculator.round_currency(total_principal_paid)),
            remaining_balance=float(FinancialCalculator.round_currency(ending_balance))
        )
    
    @staticmethod
    def calculate_cumulative_principal_paydown(
        loan_amount: float,
        annual_interest_rate: float,
        loan_term_years: int,
        years: int
    ) -> float:
        """
        Calculate cumulative principal paydown over multiple years
        
        Args:
            loan_amount: Original loan amount
            annual_interest_rate: Annual interest rate
            loan_term_years: Loan term in years
            years: Number of years to calculate
            
        Returns:
            Total principal paid down over the period
        """
        if years <= 0:
            return 0.0
        
        final_payments = min(years * 12, loan_term_years * 12)
        remaining_balance = FinancialCalculator.calculate_loan_balance(
            loan_amount, annual_interest_rate, loan_term_years, final_payments
        )
        
        total_paydown = loan_amount - remaining_balance
        return float(FinancialCalculator.round_currency(total_paydown))


class AppreciationCalculator:
    """Calculator for Pillar 3: Appreciation Analysis"""
    
    @staticmethod
    def calculate_appreciation(
        beginning_value: float,
        ending_value: float,
        years: float = 1.0
    ) -> AppreciationAnalysis:
        """
        Calculate property appreciation for a given period
        
        Args:
            beginning_value: Property value at beginning of period
            ending_value: Property value at end of period
            years: Number of years in the period
            
        Returns:
            AppreciationAnalysis with appreciation details
        """
        # Total appreciation over the period
        total_appreciation = ending_value - beginning_value
        
        # Annual appreciation amount (for multi-year periods)
        annual_appreciation = total_appreciation / years if years > 0 else total_appreciation
        
        # Appreciation rate for the period (based on total appreciation)
        if beginning_value > 0:
            appreciation_rate = (total_appreciation / beginning_value) * 100
        else:
            appreciation_rate = 0.0
        
        # Cumulative appreciation
        cumulative_appreciation = total_appreciation
        
        # Annualized appreciation rate (CAGR)
        annualized_rate = FinancialCalculator.calculate_appreciation_rate(
            beginning_value, ending_value, years
        )
        
        return AppreciationAnalysis(
            beginning_value=float(FinancialCalculator.round_currency(beginning_value)),
            ending_value=float(FinancialCalculator.round_currency(ending_value)),
            annual_appreciation=float(FinancialCalculator.round_currency(annual_appreciation)),
            appreciation_rate=float(FinancialCalculator.round_currency(appreciation_rate)),
            cumulative_appreciation=float(FinancialCalculator.round_currency(cumulative_appreciation)),
            annualized_appreciation_rate=float(FinancialCalculator.round_currency(annualized_rate))
        )
    
    @staticmethod
    def project_future_value(
        current_value: float,
        annual_appreciation_rate: float,
        years: int
    ) -> float:
        """
        Project future property value based on appreciation rate
        
        Args:
            current_value: Current property value
            annual_appreciation_rate: Expected annual appreciation rate (as decimal)
            years: Number of years to project
            
        Returns:
            Projected future value
        """
        future_value = FinancialCalculator.future_value(
            current_value, annual_appreciation_rate, years
        )
        return float(FinancialCalculator.round_currency(future_value))
    
    @staticmethod
    def calculate_appreciation_scenarios(
        current_value: float,
        years: int,
        scenarios: Dict[str, float] = None
    ) -> Dict[str, float]:
        """
        Calculate appreciation under different rate scenarios
        
        Args:
            current_value: Current property value
            years: Number of years
            scenarios: Dictionary of scenario names and rates
            
        Returns:
            Dictionary of scenarios and projected values
        """
        if scenarios is None:
            scenarios = {
                'conservative': 0.02,  # 2% annual
                'moderate': 0.03,      # 3% annual
                'optimistic': 0.05     # 5% annual
            }
        
        results = {}
        for scenario_name, rate in scenarios.items():
            future_value = AppreciationCalculator.project_future_value(
                current_value, rate, years
            )
            results[scenario_name] = future_value
        
        return results


class TaxBenefitsCalculator:
    """Calculator for Pillar 4: Tax Benefits Analysis"""
    
    @staticmethod
    def calculate_tax_benefits(
        building_value: float,
        annual_interest_paid: float,
        operating_expenses: float,
        marginal_tax_rate: float,
        depreciation_method: str = 'straight_line',
        depreciation_period: float = None
    ) -> TaxBenefitsAnalysis:
        """
        Calculate annual tax benefits from real estate investment
        
        Args:
            building_value: Depreciable building value (excludes land)
            annual_interest_paid: Annual mortgage interest paid
            operating_expenses: Deductible operating expenses
            marginal_tax_rate: Investor's marginal tax rate (as decimal)
            depreciation_method: Depreciation method ('straight_line')
            depreciation_period: Depreciation period in years
            
        Returns:
            TaxBenefitsAnalysis with tax benefit details
        """
        if depreciation_period is None:
            # Default to IRS residential rental property depreciation period
            depreciation_period = app_settings.get('default_depreciation_years', 27.5)
        
        # Calculate annual depreciation deduction
        if depreciation_method == 'straight_line':
            annual_depreciation = building_value / depreciation_period
        else:
            # Future: implement accelerated depreciation methods
            annual_depreciation = building_value / depreciation_period
        
        # Total deductions
        total_deductions = annual_depreciation + annual_interest_paid + operating_expenses
        
        # Tax savings (deductions × marginal tax rate)
        tax_savings = total_deductions * marginal_tax_rate
        
        # Effective tax rate (actual tax saved / gross income)
        # Note: This would need gross income for accurate calculation
        effective_tax_rate = marginal_tax_rate  # Simplified for now
        
        return TaxBenefitsAnalysis(
            depreciation_deduction=float(FinancialCalculator.round_currency(annual_depreciation)),
            interest_deduction=float(FinancialCalculator.round_currency(annual_interest_paid)),
            operating_expense_deductions=float(FinancialCalculator.round_currency(operating_expenses)),
            total_deductions=float(FinancialCalculator.round_currency(total_deductions)),
            tax_savings=float(FinancialCalculator.round_currency(tax_savings)),
            marginal_tax_rate=float(FinancialCalculator.round_currency(marginal_tax_rate * 100)),
            effective_tax_rate=float(FinancialCalculator.round_currency(effective_tax_rate * 100))
        )
    
    @staticmethod
    def calculate_building_value(
        total_property_value: float,
        land_percentage: float = None
    ) -> float:
        """
        Calculate depreciable building value (excludes land)
        
        Args:
            total_property_value: Total property value
            land_percentage: Percentage of value attributed to land (as decimal)
            
        Returns:
            Depreciable building value
        """
        if land_percentage is None:
            land_percentage = app_settings.get('land_to_building_ratio', 0.20)
        
        building_value = total_property_value * (1 - land_percentage)
        return float(FinancialCalculator.round_currency(building_value))
    
    @staticmethod
    def calculate_annual_interest_paid(
        loan_amount: float,
        annual_interest_rate: float,
        loan_term_years: int,
        analysis_year: int
    ) -> float:
        """
        Calculate total interest paid in a specific year
        
        Args:
            loan_amount: Original loan amount
            annual_interest_rate: Annual interest rate
            loan_term_years: Loan term in years
            analysis_year: Year to analyze (1-based)
            
        Returns:
            Total interest paid in the year
        """
        if analysis_year <= 0 or analysis_year > loan_term_years:
            return 0.0
        
        total_interest = 0.0
        start_payment = (analysis_year - 1) * 12 + 1
        end_payment = analysis_year * 12
        
        for payment_num in range(start_payment, end_payment + 1):
            interest_payment = FinancialCalculator.calculate_interest_payment(
                loan_amount, annual_interest_rate, loan_term_years, payment_num
            )
            total_interest += interest_payment
        
        return float(FinancialCalculator.round_currency(total_interest))


class FourPillarsAnalyzer:
    """Main Four Pillars Analysis orchestrator"""
    
    def __init__(self):
        self.cash_flow_calc = CashFlowCalculator()
        self.principal_calc = PrincipalPaydownCalculator()
        self.appreciation_calc = AppreciationCalculator()
        self.tax_calc = TaxBenefitsCalculator()
    
    def analyze_investment(
        self,
        # Property and loan details
        property_value: float,
        loan_amount: float,
        annual_interest_rate: float,
        loan_term_years: int,
        
        # Income and expenses
        annual_rental_income: float,
        operating_expenses: Dict[str, float],
        
        # Analysis parameters
        analysis_year: int = 1,
        ending_property_value: float = None,
        marginal_tax_rate: float = None,
        land_percentage: float = None,
        
        # Optional overrides
        total_cash_invested: float = None
    ) -> FourPillarsResults:
        """
        Perform complete Four Pillars analysis
        
        Args:
            property_value: Current property value
            loan_amount: Loan amount
            annual_interest_rate: Annual interest rate (as decimal)
            loan_term_years: Loan term in years
            annual_rental_income: Annual rental income
            operating_expenses: Dictionary of operating expenses
            analysis_year: Year to analyze (default: 1)
            ending_property_value: Property value at end of analysis year
            marginal_tax_rate: Marginal tax rate (as decimal)
            land_percentage: Land percentage of total value
            total_cash_invested: Total cash invested (for return calculation)
            
        Returns:
            FourPillarsResults with complete analysis
        """
        # Set defaults
        if ending_property_value is None:
            # Assume 3% appreciation if not provided
            appreciation_rate = 0.03
            ending_property_value = property_value * (1 + appreciation_rate)
        
        if marginal_tax_rate is None:
            marginal_tax_rate = app_settings.get('default_marginal_tax_rate', 0.24)
        
        if land_percentage is None:
            land_percentage = app_settings.get('land_to_building_ratio', 0.20)
        
        if total_cash_invested is None:
            # Estimate as down payment + closing costs (rough estimate)
            down_payment = property_value - loan_amount
            total_cash_invested = down_payment * 1.05  # Add 5% for closing costs
        
        # Calculate annual debt service
        monthly_payment = FinancialCalculator.calculate_monthly_payment(
            loan_amount, annual_interest_rate, loan_term_years
        )
        annual_debt_service = monthly_payment * 12
        
        # Pillar 1: Cash Flow
        cash_flow = self.cash_flow_calc.calculate_cash_flow(
            annual_rental_income, operating_expenses, annual_debt_service
        )
        
        # Pillar 2: Principal Paydown
        principal_paydown = self.principal_calc.calculate_principal_paydown(
            loan_amount, annual_interest_rate, loan_term_years, analysis_year
        )
        
        # Pillar 3: Appreciation
        appreciation = self.appreciation_calc.calculate_appreciation(
            property_value, ending_property_value, 1.0
        )
        
        # Pillar 4: Tax Benefits
        building_value = self.tax_calc.calculate_building_value(property_value, land_percentage)
        annual_interest = self.tax_calc.calculate_annual_interest_paid(
            loan_amount, annual_interest_rate, loan_term_years, analysis_year
        )
        
        # Use operating expenses for tax deductions (excluding debt service)
        deductible_expenses = sum(operating_expenses.values())
        
        tax_benefits = self.tax_calc.calculate_tax_benefits(
            building_value, annual_interest, deductible_expenses, marginal_tax_rate
        )
        
        # Calculate total return
        total_annual_return = (
            cash_flow.annual_cash_flow +
            principal_paydown.annual_principal_paydown +
            appreciation.annual_appreciation +
            tax_benefits.tax_savings
        )
        
        # Calculate total return percentage
        if total_cash_invested > 0:
            total_return_percentage = (total_annual_return / total_cash_invested) * 100
        else:
            total_return_percentage = 0.0
        
        return FourPillarsResults(
            cash_flow=cash_flow,
            principal_paydown=principal_paydown,
            appreciation=appreciation,
            tax_benefits=tax_benefits,
            total_annual_return=float(FinancialCalculator.round_currency(total_annual_return)),
            total_return_percentage=float(FinancialCalculator.round_currency(total_return_percentage)),
            analysis_year=analysis_year
        )
    
    def analyze_multi_year(
        self,
        property_value: float,
        loan_amount: float,
        annual_interest_rate: float,
        loan_term_years: int,
        annual_rental_income: float,
        operating_expenses: Dict[str, float],
        years: int = 5,
        annual_appreciation_rate: float = 0.03,
        marginal_tax_rate: float = None,
        total_cash_invested: float = None
    ) -> List[FourPillarsResults]:
        """
        Perform Four Pillars analysis for multiple years
        
        Args:
            property_value: Initial property value
            loan_amount: Loan amount
            annual_interest_rate: Annual interest rate
            loan_term_years: Loan term in years
            annual_rental_income: Annual rental income
            operating_expenses: Dictionary of operating expenses
            years: Number of years to analyze
            annual_appreciation_rate: Expected annual appreciation rate
            marginal_tax_rate: Marginal tax rate
            total_cash_invested: Total cash invested
            
        Returns:
            List of FourPillarsResults for each year
        """
        results = []
        
        for year in range(1, years + 1):
            # Calculate property value for this year
            ending_value = property_value * ((1 + annual_appreciation_rate) ** year)
            
            # Perform analysis for this year
            year_result = self.analyze_investment(
                property_value=property_value,
                loan_amount=loan_amount,
                annual_interest_rate=annual_interest_rate,
                loan_term_years=loan_term_years,
                annual_rental_income=annual_rental_income,
                operating_expenses=operating_expenses,
                analysis_year=year,
                ending_property_value=ending_value,
                marginal_tax_rate=marginal_tax_rate,
                total_cash_invested=total_cash_invested
            )
            
            results.append(year_result)
        
        return results
    
    def create_summary_report(self, results: Union[FourPillarsResults, List[FourPillarsResults]]) -> Dict:
        """
        Create a summary report of Four Pillars analysis
        
        Args:
            results: Single year or multi-year results
            
        Returns:
            Dictionary with summary statistics
        """
        if isinstance(results, FourPillarsResults):
            results = [results]
        
        if not results:
            return {}
        
        # Calculate averages and totals
        total_years = len(results)
        
        summary = {
            'analysis_period': f"{results[0].analysis_year} to {results[-1].analysis_year}",
            'total_years': total_years,
            'average_annual_return': sum(r.total_annual_return for r in results) / total_years,
            'average_return_percentage': sum(r.total_return_percentage for r in results) / total_years,
            'total_cumulative_return': sum(r.total_annual_return for r in results),
            
            # Pillar averages
            'average_cash_flow': sum(r.cash_flow.annual_cash_flow for r in results) / total_years,
            'average_principal_paydown': sum(r.principal_paydown.annual_principal_paydown for r in results) / total_years,
            'average_appreciation': sum(r.appreciation.annual_appreciation for r in results) / total_years,
            'average_tax_benefits': sum(r.tax_benefits.tax_savings for r in results) / total_years,
            
            # Performance metrics
            'best_year': max(results, key=lambda r: r.total_annual_return).analysis_year,
            'best_year_return': max(r.total_annual_return for r in results),
            'worst_year': min(results, key=lambda r: r.total_annual_return).analysis_year,
            'worst_year_return': min(r.total_annual_return for r in results),
        }
        
        # Round all currency values
        for key, value in summary.items():
            if isinstance(value, (int, float)) and 'year' not in key and 'total_years' not in key:
                summary[key] = float(FinancialCalculator.round_currency(value))
        
        return summary