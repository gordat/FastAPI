from fastapi import APIRouter, Path, Query, Depends, HTTPException, status
from typing import List
from modules import schemas, database, models, fce, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
	prefix="/user",
	tags=['Users']
)

get_db = database.get_db

# ------------------------------------ POST -----------------------------------------------#
@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return fce.create_user(request, db)

# ------------------------------------ GET -----------------------------------------------#
@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db), usr: schemas.User = Depends(oauth2.get_current_user)):
    return fce.get_user(id, db)