from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from fastapi import HTTPException

def validate_sa_id_and_get_birthday(id_number: str) -> date:
    """Validates length and extracts birthday. (Luhn check can be added here)"""
    if len(id_number) != 13 or not id_number.isdigit():
        raise HTTPException(status_code=400, detail="Invalid SA ID format")

    year_part = int(id_number[:2])
    month_part = int(id_number[2:4])
    day_part = int(id_number[4:6])

    # Determine century (Simplified logic for project)
    current_year_short = datetime.now().year % 100
    century = 2000 if year_part <= current_year_short else 1900
    
    try:
        birthday = date(century + year_part, month_part, day_part)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID contains invalid date")
    
    return birthday

def get_risk_group(birthday: date) -> int:
    """Assigns risk group based on Age (18-30: 1, 31-50: 2, 51-65: 3)"""
    age = (date.today() - birthday).days // 365
    
    if 18 <= age <= 30:
        return 1
    elif 31 <= age <= 50:
        return 2
    elif 51 <= age <= 65:
        return 3
    else:
        raise HTTPException(status_code=400, detail="Age must be between 18 and 65 to apply.")

def calculate_loan_snapshot(base_price: Decimal, profile: RiskProfile):
    """Calculates snapshot data where the final price is the total cost of ownership"""
    
    # 1. Convert floats to strings for exact Decimal precision
    deposit_pct = Decimal(str(profile.required_deposit_percent))
    interest_mod = Decimal(str(profile.interest_rate_modifier))
    
    # 2. Calculate the Upfront Deposit
    # R3200 * 0.20 = R640
    deposit_amt = base_price * deposit_pct
    
    # 3. Loan Principal = Amount to be financed
    # R3200 - R640 = R2560
    principal = base_price - deposit_amt
    
    # 4. Total Loan Amount = Principal + Interest
    # R2560 * (1 + 0.10) = R2816
    total_loan = principal * (Decimal('1') + interest_mod)
    
    # 5. Total Cost of Ownership (Final Price)
    # R640 (Deposit) + R2816 (Loan) = R3456
    total_cost_of_phone = deposit_amt + total_loan
    
    # 6. Daily Payment = Total Loan / 360 days
    daily = total_loan / Decimal('360')
    
    return {
        # This now returns the full price (Deposit + Principal + Interest)
        "final_cash_price": total_cost_of_phone, 
        "final_interest_rate": profile.interest_rate_modifier,
        "loan_principal": principal,
        "daily_payment": round(daily, 2)
    }