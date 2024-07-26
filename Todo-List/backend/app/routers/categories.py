from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.schemas import Category as CategorySchema, CategoryCreate
from app.crud import get_categories, get_category, create_category, update_category, delete_category
from app.core.dependencies import get_db
from typing import List
import logging

logging.basicConfig(filename='app.log', level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter()

@router.get("/categories/", response_model=List[CategorySchema])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logger.info(f"Request to fetch categories with skip={skip} and limit={limit}")
    try:
        categories = get_categories(db, skip=skip, limit=limit)
        return categories
    except SQLAlchemyError as e:
        logger.error(f"Error fetching categories: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Unexpected error fetching categories: {e}")
        raise HTTPException(status_code=500, detail="Server error")


@router.get("/categories/{category_id}", response_model=CategorySchema)
def read_category(category_id: int, db: Session = Depends(get_db)):
    logger.info(f"Request to fetch category with ID: {category_id}")
    db_category = get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.post("/categories/", response_model=CategorySchema)
def create_category_endpoint(category: CategoryCreate, db: Session = Depends(get_db)):
    logger.info(f"Request to create category with name: {category.name}")
    try:
        return create_category(db=db, category=category)
    except SQLAlchemyError as e:
        logger.error(f"Error creating category: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Unexpected error creating category: {e}")
        raise HTTPException(status_code=500, detail="Server error")


@router.put("/categories/{category_id}", response_model=CategorySchema)
def update_category_endpoint(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    logger.info(f"Request to update category with ID: {category_id}")
    db_category = get_category(db, category_id=category_id)
    if db_category is None:
        logger.error(f"Category with ID {category_id} not found for update")
        raise HTTPException(status_code=404, detail="Category not found")
    return update_category(db=db,category_id=category_id, category=category)


@router.delete("/categories/{category_id}")
def delete_category_endpoint(category_id: int, db: Session = Depends(get_db)):
    logger.info(f"Request to delete category with ID: {category_id}")
    db_category = get_category(db, category_id=category_id)
    if db_category is None:
        logger.error(f"Category with ID {category_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Category not found")
    return delete_category(db, category_id=category_id)