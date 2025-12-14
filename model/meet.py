from pydantic import BaseModel

class Meet(BaseModel):
    name: str
    emails: str
    user_type: str
    date: str
    time_slot: str

class TimeSlot(BaseModel):
    date: str
    time_slot: str