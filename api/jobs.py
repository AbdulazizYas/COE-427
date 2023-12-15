from fastapi import APIRouter, Body, Depends, HTTPException
import models
from sqlalchemy.orm import Session
from dependencies import get_db
from schemas import Job, JobResponse, User

jobs = APIRouter(
  prefix="/jobs",
  tags=["Jobs"]
)

@jobs.get("/", response_model= list[JobResponse])
async def getJobs(db: Session = Depends(get_db)):
  return db.query(models.Job).all()

@jobs.post("/add", response_model= JobResponse)
async def addJob(job: Job, db: Session = Depends(get_db)):
  job = models.Job(**job.model_dump())
  db.add(job)
  db.commit()
  db.refresh(job)
  return job

@jobs.post("/{username}/apply/{job_id}", response_model=User)
async def applyForJob(username: str, job_id: int,  db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.username == username).first()

  if user is None:
    raise HTTPException(status_code=404, detail="User not found")
  
  job = db.query(models.Job).filter(models.Job.id == job_id).first()

  if job is None:
    raise HTTPException(status_code=404, detail="Job not found")

  user.applications.append(job)

  db.commit()
  db.refresh(user)

  return user


