from fastapi import APIRouter, Depends, WebSocket
import models
from schemas import Notification
from sqlalchemy.orm import Session
import boto3
import os

from dependencies import get_db

notifications = APIRouter(
  prefix="/notifications",
  tags=["Notifications"]
)

sns_client = boto3.client('sns', region_name='us-west-2'
)

@notifications.get("/{username}", response_model=list[Notification])
async def getNotifications(username: str, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.username == username).first()

  return user.notifications

@notifications.post("/publish-notification")
async def publsihNotification(notification: Notification):
  response = sns_client.publish(
        TopicArn=os.environ['SNS_ARN'],
        Message=notification.model_dump_json(),
        Subject='Job Published',
    )
  return {"sns_response": response}

@notifications.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
  await websocket.accept()
  while True:
      data = await websocket.receive_text()
      await websocket.send_text(data)



