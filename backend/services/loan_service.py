from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from fastapi import HTTPException

# String manipulation to validate SA ID and extract birthday
def validate_sa_id_and_get_birthday(id_number: str) -> date:
    if len(id_number) != 13 or not id_number.isdigit():
        raise HTTPException(status_code=400, detail="Invalid SA ID format")

    year_part = int(id_number[:2])
    month_part = int(id_number[2:4])
    day_part = int(id_number[4:6])

    current_year_short = datetime.now().year % 100
    century = 2000 if year_part <= current_year_short else 1900
    
    try:
        birthday = date(century + year_part, month_part, day_part)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID contains invalid date")
    
    return birthday

# Risk Group Assignment based on Age
def get_risk_group(birthday: date) -> int:
    age = (date.today() - birthday).days // 365
    
    if 18 <= age <= 30:
        return 1
    elif 31 <= age <= 50:
        return 2
    elif 51 <= age <= 65:
        return 3
    else:
        raise HTTPException(status_code=400, detail="Age must be between 18 and 65 to apply.")

# Loan Calculation for a given product price and risk profile
def calculate_loan_snapshot(base_price: Decimal, profile: RiskProfile):

    deposit_pct = Decimal(str(profile.required_deposit_percent))
    interest_mod = Decimal(str(profile.interest_rate_modifier))
    
    deposit_amt = base_price * deposit_pct
    
    principal = base_price - deposit_amt
    
    total_loan = principal * (Decimal('1') + interest_mod)

    total_cost_of_phone = deposit_amt + total_loan
    
    daily = total_loan / Decimal('360')
    
    return {
        "final_cash_price": total_cost_of_phone, 
        "final_interest_rate": profile.interest_rate_modifier,
        "loan_principal": principal,
        "daily_payment": round(daily, 2)
    }