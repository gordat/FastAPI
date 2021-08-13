from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from modules import schemas, database, models, token
from sqlalchemy.orm import Session
from modules.hashing import Hash

router = APIRouter(
    tags=['Authentication']
)

get_db = database.get_db

# ------------------------------------ POST -----------------------------------------------#
@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="Invalid Credentials!")
    
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=404, detail="Incorrect Password!")

    # Generate a jwt token and return
    access_token = token.create_access_token(data={"sub": user.email})
    print(access_token)
    return {"access_token": access_token, "token_type": "bearer"}