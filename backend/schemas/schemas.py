from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import List, Dict, Optional

from pydantic import BaseModel, Field

# Fast Api docs were a bit funky so added example/s to simpify reading the docs 

class PricingTier(BaseModel):
    final_cash_price: Decimal = Field(..., examples=["15000.00"])
    final_interest_rate: Decimal = Field(..., examples=["0.15"])
    loan_principal: Decimal = Field(..., examples=["12000.00"])
    daily_payment: Decimal = Field(..., examples=["45.50"])

# Response schema for the /products/list-products endpoint
class ProductResponse(BaseModel):
    id: int
    brand: str = Field(..., examples=["Apple"])
    model_name: str = Field(..., examples=["iPhone 15"])
    base_cash_price: Decimal = Field(..., examples=["19999.00"])
    stock_level: int = Field(..., examples=[10])
    model_image: Optional[str] = None 
    pricing_tiers: Dict[int, PricingTier]
    
    model_config = ConfigDict(from_attributes=True)

# Response Scheme for the /applications/apply endpoint
class ApplicationResponse(BaseModel):
    message: str
    application_id: int