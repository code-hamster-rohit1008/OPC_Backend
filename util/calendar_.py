from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime
import os, json
from fastapi import HTTPException

TOKEN_STRING = os.getenv("GOOGLE_CALENDAR_TOKEN", "")
SCOPES = [os.getenv("GOOGLE_API_SCOPES", "https://www.googleapis.com/auth/calendar")]
CALENDAR_ID = os.getenv("CALENDAR_ID", "primary")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")

async def get_calendar_service():
    creds = None
    if TOKEN_STRING:
        creds = Credentials.from_authorized_user_info(json.loads(TOKEN_STRING), SCOPES)
    else:
        return None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                os.environ["GOOGLE_CALENDAR_TOKEN"] = creds.to_json()
            except Exception as e:
                return None
        else:
            return None

    return build('calendar', 'v3', credentials=creds)

async def combine_date_time(date_str: str, time_str: str):
    try:
        parts = time_str.split('-')
        start_part = parts[0].strip().replace(" ", "")
        end_part = parts[1].strip().replace(" ", "")
        fmt = "%Y-%m-%d %I:%M%p"
        start_dt = datetime.strptime(f"{date_str} {start_part}", fmt)
        end_dt = datetime.strptime(f"{date_str} {end_part}", fmt)
        return (start_dt, end_dt)
    except Exception:
        return None