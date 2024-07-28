from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import Task as TaskSchema, TaskCreate, TaskUpdate
from app.crud import create_task, get_task_by_task_id, get_category, update_task, delete_task
from app.core.dependencies import get_db
import logging

logging.basicConfig(filename='app.log', level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("/tasks/{task_id}", response_model=TaskSchema)
def get_task_endpint(task_id: int, db: Session = Depends(get_db)):
    db_task = get_task_by_task_id(db, task_id=task_id)
    if db_task is None:
        logger.error(f"Task with ID {task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.post("/categories/{category_id}/tasks/", response_model=TaskSchema)
def create_task_endpoint(category_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    db_category = get_category(db, category_id=category_id)
    if db_category is None:
        logger.error(f"Category with ID {category_id} not found")
        raise HTTPException(status_code=404, detail="Category Not Found")
    return create_task(db, task, category_id=category_id)


@router.put("/tasks/{task_id}", response_model=TaskSchema)
def update_task_endpoint(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = get_task_by_task_id(db, task_id=task_id)
    if db_task is None:
        logger.error(f"Task with ID {task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")
    return update_task(db, task_id=task_id, task=task)


@router.delete("/tasks/{task_id}")
def delete_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    db_task = get_task_by_task_id(db, task_id=task_id)
    if db_task is None:
        logger.error(f"Task with ID {task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")
    category_id = db_task.category_id
    
    delete_result = delete_task(db, task_id=task_id)
    if delete_result is None:
        raise HTTPException(status_code=404, detail="Task not found for deletion")

    return {"id": task_id, "category_id": category_id, "message": delete_result["message"]}