"""
Financial Calculations for Real Estate Investment Analysis

This module provides comprehensive financial calculations for real estate investment
analysis, including mortgage calculations, cash flow analysis, and return calculations.
"""

import math
from typing import Dict, List, Tuple, Optional, Union
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class FinancialCalculator:
    """
    Core financial calculation utilities for real estate investments
    """
    
    @staticmethod
    def round_currency(amount: Union[float, Decimal], places: int = 2) -> Decimal:
        """
        Round monetary amounts to specified decimal places
        
        Args:
            amount: Amount to round
            places: Number of decimal places (default: 2)
            
        Returns:
            Rounded Decimal amount
        """
        if amount is None:
            return Decimal('0.00')
        
        decimal_amount = Decimal(str(amount))
        return decimal_amount.quantize(Decimal('0.' + '0' * places), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_monthly_payment(loan_amount: float, annual_rate: float, 
                                 term_years: int) -> float:
        """
        Calculate monthly mortgage payment using standard amortization formula
        
        Args:
            loan_amount: Principal loan amount
            annual_rate: Annual interest rate (as decimal, e.g., 0.06 for 6%)
            term_years: Loan term in years
            
        Returns:
            Monthly payment amount
            
        Formula: M = P * [r(1+r)^n] / [(1+r)^n - 1]
        Where: M = monthly payment, P = principal, r = monthly rate, n = total payments
        """
        if loan_amount <= 0 or term_years <= 0:
            return 0.0
        
        if annual_rate <= 0:
            # No interest case
            return loan_amount / (term_years * 12)
        
        monthly_rate = annual_rate / 12
        num_payments = term_years * 12
        
        # Calculate payment using amortization formula
        factor = (1 + monthly_rate) ** num_payments
        monthly_payment = loan_amount * (monthly_rate * factor) / (factor - 1)
        
        return float(FinancialCalculator.round_currency(monthly_payment))
    
    @staticmethod
    def calculate_loan_balance(loan_amount: float, annual_rate: float, 
                              term_years: int, payments_made: int) -> float:
        """
        Calculate remaining loan balance after specified number of payments
        
        Args:
            loan_amount: Original loan amount
            annual_rate: Annual interest rate (as decimal)
            term_years: Loan term in years
            payments_made: Number of payments already made
            
        Returns:
            Remaining loan balance
        """
        if payments_made <= 0:
            return loan_amount
        
        if annual_rate <= 0:
            # No interest case
            total_payments = term_years * 12
            remaining_payments = max(0, total_payments - payments_made)
            return loan_amount * (remaining_payments / total_payments)
        
        monthly_rate = annual_rate / 12
        total_payments = term_years * 12
        
        if payments_made >= total_payments:
            return 0.0
        
        # Calculate remaining balance using formula
        factor = (1 + monthly_rate) ** total_payments
        paid_factor = (1 + monthly_rate) ** payments_made
        
        remaining_balance = loan_amount * (factor - paid_factor) / (factor - 1)
        
        return max(0.0, float(FinancialCalculator.round_currency(remaining_balance)))
    
    @staticmethod
    def calculate_principal_payment(loan_amount: float, annual_rate: float,
                                   term_years: int, payment_number: int) -> float:
        """
        Calculate principal portion of a specific payment
        
        Args:
            loan_amount: Original loan amount
            annual_rate: Annual interest rate (as decimal)
            term_years: Loan term in years
            payment_number: Payment number (1-based)
            
        Returns:
            Principal portion of the payment
        """
        if payment_number <= 0:
            return 0.0
        
        monthly_payment = FinancialCalculator.calculate_monthly_payment(
            loan_amount, annual_rate, term_years
        )
        
        # Calculate balance before this payment
        balance_before = FinancialCalculator.calculate_loan_balance(
            loan_amount, annual_rate, term_years, payment_number - 1
        )
        
        if balance_before <= 0:
            return 0.0
        
        # Interest portion
        monthly_rate = annual_rate / 12
        interest_payment = balance_before * monthly_rate
        
        # Principal is the remainder
        principal_payment = monthly_payment - interest_payment
        
        return max(0.0, float(FinancialCalculator.round_currency(principal_payment)))
    
    @staticmethod
    def calculate_interest_payment(loan_amount: float, annual_rate: float,
                                  term_years: int, payment_number: int) -> float:
        """
        Calculate interest portion of a specific payment
        
        Args:
            loan_amount: Original loan amount
            annual_rate: Annual interest rate (as decimal)
            term_years: Loan term in years
            payment_number: Payment number (1-based)
            
        Returns:
            Interest portion of the payment
        """
        if payment_number <= 0 or annual_rate <= 0:
            return 0.0
        
        # Calculate balance before this payment
        balance_before = FinancialCalculator.calculate_loan_balance(
            loan_amount, annual_rate, term_years, payment_number - 1
        )
        
        if balance_before <= 0:
            return 0.0
        
        monthly_rate = annual_rate / 12
        interest_payment = balance_before * monthly_rate
        
        return float(FinancialCalculator.round_currency(interest_payment))
    
    @staticmethod
    def generate_amortization_schedule(loan_amount: float, annual_rate: float,
                                     term_years: int) -> List[Dict]:
        """
        Generate complete amortization schedule
        
        Args:
            loan_amount: Original loan amount
            annual_rate: Annual interest rate (as decimal)
            term_years: Loan term in years
            
        Returns:
            List of payment dictionaries with payment details
        """
        schedule = []
        total_payments = term_years * 12
        monthly_payment = FinancialCalculator.calculate_monthly_payment(
            loan_amount, annual_rate, term_years
        )
        
        remaining_balance = loan_amount
        
        for payment_num in range(1, total_payments + 1):
            if remaining_balance <= 0:
                break
            
            # Calculate interest for this payment
            monthly_rate = annual_rate / 12
            interest_payment = remaining_balance * monthly_rate
            
            # Calculate principal (ensure we don't overpay)
            principal_payment = min(monthly_payment - interest_payment, remaining_balance)
            
            # Update balance
            remaining_balance -= principal_payment
            
            payment_info = {
                'payment_number': payment_num,
                'payment_amount': float(FinancialCalculator.round_currency(monthly_payment)),
                'principal_payment': float(FinancialCalculator.round_currency(principal_payment)),
                'interest_payment': float(FinancialCalculator.round_currency(interest_payment)),
                'remaining_balance': float(FinancialCalculator.round_currency(remaining_balance))
            }
            
            schedule.append(payment_info)
        
        return schedule
    
    @staticmethod
    def calculate_cap_rate(annual_noi: float, purchase_price: float) -> float:
        """
        Calculate capitalization rate
        
        Args:
            annual_noi: Annual Net Operating Income
            purchase_price: Property purchase price
            
        Returns:
            Cap rate as percentage (e.g., 8.5 for 8.5%)
        """
        if purchase_price <= 0:
            return 0.0
        
        cap_rate = (annual_noi / purchase_price) * 100
        return float(FinancialCalculator.round_currency(cap_rate))
    
    @staticmethod
    def calculate_cash_on_cash_return(annual_cash_flow: float, 
                                    total_cash_invested: float) -> float:
        """
        Calculate cash-on-cash return
        
        Args:
            annual_cash_flow: Annual cash flow after debt service
            total_cash_invested: Total cash invested (down payment + closing costs + repairs)
            
        Returns:
            Cash-on-cash return as percentage
        """
        if total_cash_invested <= 0:
            return 0.0
        
        return float(FinancialCalculator.round_currency(
            (annual_cash_flow / total_cash_invested) * 100
        ))
    
    @staticmethod
    def calculate_debt_service_coverage_ratio(annual_noi: float, 
                                            annual_debt_service: float) -> float:
        """
        Calculate Debt Service Coverage Ratio (DSCR)
        
        Args:
            annual_noi: Annual Net Operating Income
            annual_debt_service: Annual debt service (principal + interest)
            
        Returns:
            DSCR ratio (e.g., 1.25)
        """
        if annual_debt_service <= 0:
            return float('inf') if annual_noi > 0 else 0.0
        
        return float(FinancialCalculator.round_currency(
            annual_noi / annual_debt_service
        ))
    
    @staticmethod
    def calculate_loan_to_value_ratio(loan_amount: float, property_value: float) -> float:
        """
        Calculate Loan-to-Value ratio
        
        Args:
            loan_amount: Current loan amount
            property_value: Current property value
            
        Returns:
            LTV ratio as percentage
        """
        if property_value <= 0:
            return 0.0
        
        return float(FinancialCalculator.round_currency(
            (loan_amount / property_value) * 100
        ))
    
    @staticmethod
    def calculate_break_even_ratio(total_operating_expenses: float,
                                  gross_rental_income: float) -> float:
        """
        Calculate break-even ratio
        
        Args:
            total_operating_expenses: Total operating expenses including debt service
            gross_rental_income: Gross rental income
            
        Returns:
            Break-even ratio as percentage
        """
        if gross_rental_income <= 0:
            return 100.0 if total_operating_expenses > 0 else 0.0
        
        return float(FinancialCalculator.round_currency(
            (total_operating_expenses / gross_rental_income) * 100
        ))
    
    @staticmethod
    def calculate_operating_expense_ratio(operating_expenses: float,
                                        gross_rental_income: float) -> float:
        """
        Calculate operating expense ratio (excludes debt service)
        
        Args:
            operating_expenses: Operating expenses (excluding debt service)
            gross_rental_income: Gross rental income
            
        Returns:
            Operating expense ratio as percentage
        """
        if gross_rental_income <= 0:
            return 100.0 if operating_expenses > 0 else 0.0
        
        return float(FinancialCalculator.round_currency(
            (operating_expenses / gross_rental_income) * 100
        ))
    
    @staticmethod
    def calculate_rental_yield(annual_rental_income: float, 
                             property_value: float, 
                             gross: bool = True) -> float:
        """
        Calculate rental yield (gross or net)
        
        Args:
            annual_rental_income: Annual rental income
            property_value: Property value
            gross: If True, calculate gross yield; if False, use NOI for net yield
            
        Returns:
            Rental yield as percentage
        """
        if property_value <= 0:
            return 0.0
        
        return float(FinancialCalculator.round_currency(
            (annual_rental_income / property_value) * 100
        ))
    
    @staticmethod
    def calculate_price_per_square_foot(price: float, square_footage: float) -> float:
        """
        Calculate price per square foot
        
        Args:
            price: Property price
            square_footage: Property square footage
            
        Returns:
            Price per square foot
        """
        if square_footage <= 0:
            return 0.0
        
        return float(FinancialCalculator.round_currency(price / square_footage))
    
    @staticmethod
    def calculate_rent_per_square_foot(monthly_rent: float, square_footage: float) -> float:
        """
        Calculate rent per square foot
        
        Args:
            monthly_rent: Monthly rental amount
            square_footage: Property square footage
            
        Returns:
            Monthly rent per square foot
        """
        if square_footage <= 0:
            return 0.0
        
        return float(FinancialCalculator.round_currency(monthly_rent / square_footage))
    
    @staticmethod
    def calculate_appreciation_rate(initial_value: float, final_value: float,
                                  years: float) -> float:
        """
        Calculate annualized appreciation rate
        
        Args:
            initial_value: Initial property value
            final_value: Final property value
            years: Number of years
            
        Returns:
            Annualized appreciation rate as percentage
        """
        if initial_value <= 0 or years <= 0:
            return 0.0
        
        if final_value <= 0:
            return -100.0
        
        # Calculate compound annual growth rate (CAGR)
        rate = ((final_value / initial_value) ** (1 / years)) - 1
        
        return float(FinancialCalculator.round_currency(rate * 100))
    
    @staticmethod
    def future_value(present_value: float, annual_rate: float, years: float) -> float:
        """
        Calculate future value with compound growth
        
        Args:
            present_value: Present value
            annual_rate: Annual growth rate (as decimal)
            years: Number of years
            
        Returns:
            Future value
        """
        if years <= 0:
            return present_value
        
        future_val = present_value * ((1 + annual_rate) ** years)
        return float(FinancialCalculator.round_currency(future_val))
    
    @staticmethod
    def present_value(future_value: float, annual_rate: float, years: float) -> float:
        """
        Calculate present value with discounting
        
        Args:
            future_value: Future value
            annual_rate: Annual discount rate (as decimal)
            years: Number of years
            
        Returns:
            Present value
        """
        if years <= 0:
            return future_value
        
        if annual_rate <= 0:
            return future_value
        
        present_val = future_value / ((1 + annual_rate) ** years)
        return float(FinancialCalculator.round_currency(present_val))
    
    @staticmethod
    def calculate_irr(cash_flows: List[float], precision: float = 0.0001,
                     max_iterations: int = 1000) -> Optional[float]:
        """
        Calculate Internal Rate of Return using Newton-Raphson method
        
        Args:
            cash_flows: List of cash flows (negative for outflows, positive for inflows)
            precision: Precision for convergence
            max_iterations: Maximum iterations
            
        Returns:
            IRR as decimal (e.g., 0.12 for 12%) or None if no solution found
        """
        if len(cash_flows) < 2:
            return None
        
        # Initial guess
        rate = 0.1
        
        for iteration in range(max_iterations):
            # Calculate NPV and its derivative
            npv = 0
            npv_derivative = 0
            
            for i, cf in enumerate(cash_flows):
                npv += cf / ((1 + rate) ** i)
                if i > 0:
                    npv_derivative -= i * cf / ((1 + rate) ** (i + 1))
            
            # Check for convergence
            if abs(npv) < precision:
                return float(FinancialCalculator.round_currency(rate, 6))
            
            # Newton-Raphson update
            if npv_derivative == 0:
                break
            
            new_rate = rate - npv / npv_derivative
            
            # Prevent negative rates or extreme values
            if new_rate < -0.99 or new_rate > 10:
                break
            
            rate = new_rate
        
        return None  # No convergence found