from pydantic import BaseModel
from typing import List

class TaskBase(BaseModel):
    title: str
    description: str
    task_order: int
    
class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    category_id: int
    
class Task(TaskBase):
    id: int
    category_id: int
    
    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str
    category_order: int
    
    
class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    tasks: List[Task] = []
    
    class Config:
        from_attributes = True