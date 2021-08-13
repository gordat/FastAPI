from fastapi import FastAPI, APIRouter, Path, Query, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from modules import schemas, database, models, fce, oauth2
from sqlalchemy.orm import Session
import json

router = APIRouter(
	prefix="/apps",
	tags=['Applications']
)

get_db = database.get_db

inventory = fce.reloadData()

# ------------------------------------ GET ALL -----------------------------------------------#

@router.get("/", status_code=200, response_model=List[schemas.ShowItem])
def all(name: str = Query(None, title="Name", description="Name of Item", max_length=10, min_length=2), db: Session = Depends(get_db)):
    fce.updateDB(db)
    return fce.get_all(name, db)    

# ------------------------------------ GET ID -----------------------------------------------#
@router.get("/{id}", status_code=200, response_model=schemas.ShowItem)
def show(id: int, db: Session = Depends(get_db)):
    fce.updateDB(db)
    return fce.show(id, db)

# ------------------------------------ POST -----------------------------------------------#
@router.post("/{id}", status_code=201)
#http://localhost:8000/docs
def create(id: int, item: schemas.AppItem, db: Session=Depends(get_db), usr: schemas.User = Depends(oauth2.get_current_user)):
    fce.updateDB(db)
    return fce.create(id, item, db)

# ------------------------------------ PUT -----------------------------------------------#
@router.put("/{id}", status_code=202, response_model=schemas.UpdateAppItem)
async def update(id: int, item: schemas.UpdateAppItem, db: Session=Depends(get_db), usr: schemas.User = Depends(oauth2.get_current_user)):
    fce.updateDB(db)
    return fce.update(id, item, db)

# ------------------------------------ DELETE -----------------------------------------------#
@router.delete("/{id}", status_code=204)
#http://localhost:8000/docs
def destroy(id: int = Query(..., description="The ID of the item to delete.", gt=0), db: Session=Depends(get_db), usr: schemas.User = Depends(oauth2.get_current_user)):
    fce.updateDB(db)
    fce.destroy(inventory, id, db)

@router.get("/vizu")
async def vizu():
    return index.html
