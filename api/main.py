from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi import BackgroundTasks
import datetime

from . import crud, models, schemas
from .database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def write_notification(email: str, message=""):
    with open("logmail.txt", mode="a") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)
    
@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message=f"some notification at {datetime.datetime.now()}")
    return {"message": "Notification sent in the background"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/{user_id}/repositories/", response_model=schemas.Repository)
def create_repository_for_user(
    user_id: int, repository: schemas.RepositoryCreate, db: Session = Depends(get_db)
):
    return crud.create_user_repository(db=db, repository=repository, user_id=user_id)

@app.get("/repositories/", response_model=List[schemas.Repository])
def read_repositories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repositories = crud.get_repositories(db, skip=skip, limit=limit)
    return repositories