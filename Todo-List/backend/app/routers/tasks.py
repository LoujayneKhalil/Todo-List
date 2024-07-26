from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


router = APIRouter()

@router.get("/")
def read_tasks():
    return {"message": "Get all tasks"}