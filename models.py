from sqlalchemy import JSON, Column, ForeignKey, Integer, String, Table
from database import Base
from sqlalchemy.orm import relationship


job_applications = Table("job_applications", Base.metadata,
                       Column("user_id", ForeignKey("users.id"), primary_key=True),
                       Column("job_id", ForeignKey("jobs.id"), primary_key=True))

class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, autoincrement=True)
  username = Column(String(25), unique=True)
  email =  Column(String(80), unique=True)
  user_type = Column(String(80))

  notifications = relationship("Notification", back_populates="user")
  applications = relationship("Job", secondary=job_applications, back_populates="applicants")

  def __repr__(self):
    return f'<User {self.username} | {self.email}>'
  

class Job(Base):
  __tablename__ = "jobs"
  id = Column(Integer, primary_key=True, autoincrement=True)
  company= Column(String(25))
  jobtitle= Column(String(25))
  category= Column(String(25))
  location= Column(String(25))
  _type= Column(String(25))
  applicants = relationship("User", secondary=job_applications, back_populates="applications")
  
  def __repr__(self):
    return f'<Job {self.id} | {self.jobtitle}>'
  

class Notification(Base):
  __tablename__ = "notifications"
  id = Column(Integer, primary_key=True, autoincrement=True)
  message= Column(JSON)
  user_id = Column(Integer, ForeignKey("users.id"))
  
  user = relationship("User", back_populates="notifications")
  
  def __repr__(self):
    return f'<Notification {self.id} | {self.message}>'