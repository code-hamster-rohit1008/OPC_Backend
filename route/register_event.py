from fastapi import APIRouter, BackgroundTasks
from model.event import EventInfo
from util.email_ import send_email_async
from util.emails_template_ import register_event_email
from db.rules import add, get
import os

router = APIRouter()

@router.post("/register-event")
async def register_event(event_data: EventInfo, background_tasks: BackgroundTasks):
    try:
        exsisting_event = get({"name": event_data.name}, "REGISTERED_EVENTS", "EVENTS")
        if exsisting_event:
            return {"status_code": 400, "message": "Event with this name already exists"}
        else:
            event_data = dict(event_data)
            _ = add(event_data, "REGISTERED_EVENTS", "EVENTS")
            email_content = await register_event_email(event_data['name'])
            background_tasks.add_task(
                send_email_async,
                to_=event_data['poc_email'],
                from_=os.getenv('SMTP_USER'),
                subject_=email_content['subject_'],
                body_=email_content['body_']
            )
            return {"status_code": 200, "message": "Event registered successfully"}
    except Exception as e:
        raise {"status_code": 500, "message": "An error occurred, please try again later."}