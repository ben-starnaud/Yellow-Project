from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from db.db import get_db
from models.models import Product, RiskProfile
from services.loan_service import calculate_loan_snapshot

# import the response schema for the products endpoint
from schemas.schemas import ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/list-products", response_model=list[ProductResponse])
async def get_products(db: AsyncSession = Depends(get_db)):
    
    # Fetch all products and all risk profiles
    # Extraction of the products into list of products objects and maps them to the models.py definition
    product_query = await db.execute(select(Product))
    products = product_query.scalars().all()

    profile_query = await db.execute(select(RiskProfile))
    profiles = profile_query.scalars().all()

    results = [] 
    
    for product in products:
        # Creating a dictionary for the product
        product_data = {
            "id": product.id,
            "brand": product.brand,
            "model_name": product.model_name,
            "base_cash_price": product.base_cash_price,
            "stock_level": product.stock_level,
            "model_image": product.model_image,
            "pricing_tiers": {} 
        }
        # Pre-calculate pricing for each risk group, for each product.
        for profile in profiles:
            terms = calculate_loan_snapshot(product.base_cash_price, profile)
            product_data["pricing_tiers"][profile.risk_group] = terms
            
        results.append(product_data)
    
    return results