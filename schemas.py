from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
  username: str
  email: str
  user_type: str

  class Config:
    orm_mode = True

class JobBase(BaseModel):
  company: str
  jobtitle: str
  category: str
  location: str
  _type: str

  class Config:
    orm_mode = True


class User(UserBase):
    applications: Optional[list[JobBase]] = []

class Job(JobBase):
  applicants: Optional[list[UserBase]] = []

class JobResponse(Job):
  id: Optional[int]

class Notification(BaseModel):
  id: Optional[int]
  message: JobBase
