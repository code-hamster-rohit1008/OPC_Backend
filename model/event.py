from datetime import date
import datetime
from pydantic import BaseModel

class EventInfo(BaseModel):
    name: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    organizer: str
    location: str
    poc_name: str
    poc_phone: int