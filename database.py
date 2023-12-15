from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


engine = None

if os.environ["ENV"] == "prod":
  engine = create_engine(os.environ["DATABASE_URL"])
else:
  engine = create_engine(os.environ["DATABASE_URL"], connect_args={"check_same_thread": False})


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()