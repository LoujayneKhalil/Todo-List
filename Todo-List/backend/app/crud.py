from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .models import Category
from .schemas import CategoryCreate, CategoryUpdate
import logging

logging.basicConfig(filename='app.log', level=logging.INFO)
logger = logging.getLogger(__name__)


###############################################################################################################
##############################################  Categories CRUD  ##############################################

def get_categories(db: Session, skip: int = 0, limit: int = 10):
    logger.info(f"Fetching categories with skip={skip}, limit={limit}")
    try:
        return db.query(Category).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise
    
def get_category(db: Session, category_id: int):
    logger.info(f"Fetching category with ID: {category_id}")
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        return category
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise

def create_category(db: Session, category: CategoryCreate):
    logger.info(f"Creating category with name: {category.name}")
    try:
        db_category = Category(name=category.name)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error occurred: {e}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"An unexpected error occurred: {e}")
        raise

def update_category(db: Session, category_id: int, category: CategoryUpdate):
    logger.info(f"Updating category with ID {category_id} to name: {category.name}")
    try:
        db_category = db.query(Category).filter(Category.id == category_id).first()
        if not db_category:
            return None
        db_category.name = category.name
        db.commit()
        db.refresh(db_category)
        return db_category
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error occurred: {e}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"An unexpected error occurred: {e}")
        raise

def delete_category(db: Session, category_id: int):
    try:
        db_category = db.query(Category).filter(Category.id == category_id).first()
        if not db_category:
            logger.error(f"Category with ID {category_id} not found for deletion")
            return None
        logger.info(f"Deleting category with ID {category_id}")
        db.delete(db_category)
        db.commit()
        logger.info(f"Category with ID {category_id} successfully deleted")
        return {"message": f"Category with ID: {category_id} is deleted"}
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error occurred: {e}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"An unexpected error occurred: {e}")
        raise
    
    
################################################################################################################
#################################################  Tasks CRUD  #################################################