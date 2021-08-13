#!/usr/bin/python3
import sys
from fastapi import FastAPI, APIRouter, Request, Response
from modules.database import engine
from modules import models
from routers import application, user, auth, vizu
import uvicorn
import time

"""
to start WEB-Server use following command in command prompt:
    uvicorn myAPI:app --reload

    http://localhost:8000/docs
"""

app = FastAPI(title="myAPI + SQLite DB", description="Gordičovo testovací API")

models.Base.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(application.router)
app.include_router(user.router)
app.include_router(vizu.router)

# ==================================== Start uvicorn =======================================#

def main():
    # start uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)

if __name__ == "__main__":
    main()
