from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .models import Category, Task
from .schemas import CategoryCreate, CategoryUpdate, TaskCreate, Task as TaskSchema, TaskUpdate
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

def get_task_by_task_id(db: Session, task_id: int):
    logger.info(f"Fetching task with ID: {task_id}")
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        return task
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise

def create_task(db: Session, task: TaskCreate, category_id: int):
    logger.info(f"Creating task with title: {task.title} in category with ID: {category_id}")
    try:
        db_task = Task(title=task.title, description=task.description, task_order=task.task_order, category_id=category_id)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error occurred: {e}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"An unexpected error occurred: {e}")
        raise
    
def update_task(db: Session, task_id: int, task: TaskUpdate):
    logger.info(f"Updating task with ID {task_id} to title: {task.title}")
    try:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            return None
        
        # Check if the category_id exists
        category = db.query(Category).filter(Category.id == task.category_id).first()
        if not category:
            logger.error(f"Category with ID {task.category_id} not found")
            raise HTTPException(status_code=404, detail="Category not found")
        
        db_task.title = task.title
        db_task.description = task.description
        db_task.task_order = task.task_order
        db_task.category_id = task.category_id
        db.commit()
        db.refresh(db_task)
        return db_task
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error occurred: {e}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"An unexpected error occurred: {e}")
        raise
    
def delete_task(db: Session, task_id: int):
    try:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            logger.error(f"Task with ID {task_id} not found for deletion")
            return None
        logger.info(f"Deleting task with ID {task_id}")
        db.delete(db_task)
        db.commit()
        logger.info(f"Task with ID {task_id} successfully deleted")
        return {"message": f"Task with ID: {task_id} is deleted"}
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error occurred: {e}")
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"An unexpected error occurred: {e}")
        raise