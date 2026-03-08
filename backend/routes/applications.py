import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from decimal import Decimal

from db.db import get_db
from models.models import Application, LoanContract, Product, RiskProfile
from services.loan_service import validate_sa_id_and_get_birthday, get_risk_group, calculate_loan_snapshot

# Import the response schema for the application endpoint
from schemas.schemas import ApplicationResponse

router = APIRouter(prefix="/applications", tags=["Applications"])

UPLOAD_DIR = "uploads"

# In your applications router file
@router.get("/check-id/{id_number}")
async def check_id_exists(id_number: str, db: AsyncSession = Depends(get_db)):
    """Check if an ID number has already been used in an application."""
    query = await db.execute(select(Application).where(Application.id_number == id_number))
    exists = query.scalars().first() is not None
    return {"exists": exists}

@router.post("/apply", response_model = ApplicationResponse)
async def create_loan_application(
    full_name: str = Form(...),
    id_number: str = Form(..., min_length=13, max_length=13),  # SA ID numbers are 13 digits
    monthly_income: float = Form(...),
    phone_id: int = Form(...),
    proof_of_income: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    # Validate ID and calculate Birthday and Risk
    birthday = validate_sa_id_and_get_birthday(id_number)
    personal_risk_group_id = get_risk_group(birthday)

    # Check if ID already exists 
    existing_id = await db.execute(select(Application).where(Application.id_number == id_number))
    if existing_id.scalars().first():
        raise HTTPException(status_code=400, detail="An application with this ID already exists")

    # Fetch Product based off primary key and Risk Profile based of personal_risk_group_id
    product = await db.get(Product, phone_id)
    risk_profile = await db.execute(select(RiskProfile).where(RiskProfile.risk_group == personal_risk_group_id))
    profile = risk_profile.scalars().first()
    
    if not product or not profile:
        raise HTTPException(status_code=404, detail="Phone or Risk Profile not found")

    # Rename the file using a UUID to prevent (basically to standardise)
    # 1. duplicate filenames 
    # 2. security leaks (trying to rename files to access other parts of the system)
    file_ext = os.path.splitext(proof_of_income.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Write the file to the /uploads directory 
    write_document_file(proof_of_income, file_path)

    # 5. Create Application and Loan Contract (The "Snapshot")
    new_application = Application(
        full_name = full_name,
        id_number = id_number,
        birthday = birthday,
        monthly_income = Decimal(str(monthly_income)),
        proof_of_income_url = file_path
    )
    
    db.add(new_application)

    # draft commit to keep the id of the application
    await db.flush() 

    # perform the calculations for the contract
    terms = calculate_loan_snapshot(product.base_cash_price, profile)
    
    new_contract = LoanContract(
        application_id = new_application.id,
        product_id = product.id,
        **terms # Unpacks dictionary 
    )
    
    db.add(new_contract)

    # Full commit to save both application and contract
    await db.commit()

    return {"message": "Application submitted", "application_id": new_application.id}

# When writing the file to the system, read it in smaller chunks to prevent memory issues
def write_document_file(file: UploadFile, destination: str):
    with open(destination, "wb") as buffer:
        while True:
            chunk = file.file.read(1024)  
            if not chunk:
                break
            buffer.write(chunk)