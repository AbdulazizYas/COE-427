from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from api.users import users
from api.jobs import jobs
from api.notifications import notifications
from models import Base
from database import engine
import os

app = FastAPI(
    title="Linker", openapi_url="/openapi.json"
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users)
app.include_router(jobs)
app.include_router(notifications)

if __name__ == "__main__":
  Base.metadata.create_all(bind=engine)
  uvicorn.run(
    app="main:app",
    reload=True if os.environ["ENV"] != "prod" else False,
    host="localhost" if os.environ["ENV"] != "prod" else "0.0.0.0",
    port=8000
  )