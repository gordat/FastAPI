from fastapi import APIRouter, Path, Query, Depends, HTTPException, status, Request, Response
from fastapi.responses import HTMLResponse
from typing import List
from modules import schemas, database, models, fce, oauth2
from sqlalchemy.orm import Session
from pathlib import Path
from mimetypes import guess_type


router = APIRouter(
	prefix="/vizu",
	tags=['Visualization']
)

get_db = database.get_db


basePath = Path(__file__).parent / "../static"

# ------------------------------------ GET -----------------------------------------------#
@router.get("/")
def show(request: Request, db: Session=Depends(get_db)): #, usr: schemas.User = Depends(oauth2.get_current_user)):
    filePath = (basePath / "index.html").resolve()
    # filename = Path(__file__).parent / "../static/index.html"

    if not filePath.exists():
        return Response(status_code=404)

    with open(filePath) as f:
        html_content = f.read()

    content_type, _ = guess_type(filePath)
    #return Response(content, media_type=content_type)
    return HTMLResponse(content=html_content, status_code=200)

@router.get("/{filename}")
def show_file(filename, request: Request, db: Session=Depends(get_db)):#, usr: schemas.User = Depends(oauth2.get_current_user)):
    filePath = (basePath) / filename

    if not filePath.exists():
        return Response(status_code=404)

    with open(filePath) as f:
        html_content = f.read()

    content_type, _ = guess_type(filePath)
    #return Response(content, media_type=content_type)
    return HTMLResponse(content=html_content, status_code=200)