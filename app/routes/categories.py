from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/")
def create_category(cat: schemas.CategoryCreate, db: Session = Depends(get_db)):

    new_cat = models.Category(name=cat.name)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)

    return new_cat


@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()