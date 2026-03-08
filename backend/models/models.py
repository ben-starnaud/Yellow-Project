from sqlalchemy import Column, Integer, String, Numeric, Float, Date, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from db.db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    model_name = Column(String, nullable=False)
    base_cash_price = Column(Numeric(10, 2), nullable=False)
    stock_level = Column(Integer, default=0)
    model_image = Column(Text, nullable=True)
    
    contracts = relationship("LoanContract", back_populates="product")

class RiskProfile(Base):
    __tablename__ = "risk_profiles"

    id = Column(Integer, primary_key=True)
    risk_group = Column(Integer, unique=True) # 1, 2, or 3
    interest_rate_modifier = Column(Float, nullable=False) # e.g. 0.15
    required_deposit_percent = Column(Float, nullable=False) # e.g. 0.10

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    id_number = Column(String(13), unique=True, index=True, nullable=False)
    birthday = Column(Date, nullable=False)
    monthly_income = Column(Numeric(10, 2), nullable=False)
    proof_of_income_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # One application has one contract
    contract = relationship("LoanContract", back_populates="application", uselist=False)

class LoanContract(Base):
    __tablename__ = "loan_contracts"
    
    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("applications.id"), unique=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    
    # Snapshot Fields (Copying data at time of creation)
    final_cash_price = Column(Numeric(10, 2))
    final_interest_rate = Column(Float)
    loan_principal = Column(Numeric(10, 2))
    daily_payment = Column(Numeric(10, 2))

    application = relationship("Application", back_populates="contract")
    product = relationship("Product", back_populates="contracts")