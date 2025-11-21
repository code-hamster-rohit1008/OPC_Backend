from pydantic import BaseModel

class ContactUsInfo(BaseModel):
    name: str
    email: str
    subject: str
    message: str