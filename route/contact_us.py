from fastapi import APIRouter, HTTPException, BackgroundTasks
from model.contact_us import ContactUsInfo
from util.email_ import send_email_async
import os

router = APIRouter()

@router.post("/contact-us")
async def contact_us(contact_info: ContactUsInfo, background_tasks: BackgroundTasks):
    try:
        subject = f'Contact Us Message from {contact_info.name}'
        body = f"NAME: {contact_info.name}\n\nCONTACT EMAIL: {contact_info.email}\n\nSUBJECT: {contact_info.subject}\n\nMESSAGE: -\n\n{contact_info.message}"
        background_tasks.add_task(
            send_email_async,
            to_=os.getenv('SMTP_USER'),
            from_=contact_info.email,
            subject_=subject,
            body_=body
        )
        return {"status_code": 200, "message": "Your message has been sent successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")
    