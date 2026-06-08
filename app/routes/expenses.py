from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.jwt_handler import get_current_user

router = APIRouter(prefix="/expenses", tags=["Expenses"])


# CREATE EXPENSE
@router.post("/")
def create_expense(
    exp: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    new_expense = models.Expense(
        amount=exp.amount,
        description=exp.description,
        category_id=exp.category_id,
        user_id=user_id
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


# GET EXPENSES (ONLY USER DATA)
@router.get("/")
def get_expenses(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    expenses = db.query(models.Expense).filter(
        models.Expense.user_id == user_id
    ).all()

    return expenses


# UPDATE EXPENSE
@router.put("/{expense_id}")
def update_expense(
    expense_id: int,
    exp: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id,
        models.Expense.user_id == user_id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    expense.amount = exp.amount
    expense.description = exp.description
    expense.category_id = exp.category_id

    db.commit()
    db.refresh(expense)

    return expense


# DELETE EXPENSE
@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id,
        models.Expense.user_id == user_id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()

    return {"message": "Expense deleted successfully"}