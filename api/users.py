from fastapi import APIRouter, Body, Depends, HTTPException
from schemas import User
import models
from sqlalchemy.orm import Session
from dependencies import get_db

users = APIRouter(
  prefix="/users",
  tags=["Users"]
)

@users.get("/", response_model=list[User])
async def getUsers(db: Session = Depends(get_db)):
  return db.query(models.User).all()

@users.post("/create", response_model=User)
async def createUser(user: User, db: Session = Depends(get_db)):
  check_user = db.query(models.User).filter(models.User.username == user.username).first()

  if check_user is not None:
    raise HTTPException(status_code=400, detail="Username already registered")
  
  check_user = db.query(models.User).filter(models.User.email == user.email).first()

  if check_user is not None:
    raise HTTPException(status_code=400, detail="Email already registered")
  
  new_user = models.User(
    email=user.email,
    username= user.username,
    user_type=user.user_type
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

@users.post("/login", response_model= User)
async def login(email: str = Body(...), pwd: str = Body(...), db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.email == email).first()

  if user is None:
    raise HTTPException(status_code=404, detail=f"User with email: {email} does not exist")
  return user
