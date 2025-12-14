from util.calendar_ import get_calendar_service, combine_date_time
from util.email_ import send_email_async
from model.meet import Meet
from db.rules import get, get_all, add
from fastapi import APIRouter, BackgroundTasks
from datetime import datetime
import os

router = APIRouter()

@router.get("/timings")
async def get_meeting_timings(date: str):
    try:
        scheduled_meetings = get_all(
            query={'date': date},
            collection="SCHEDULED_MEETS",
            database="MEET"
        )
        all_slots = get({}, collection="TIMINGS", database="MEET")
        booked_slots = [meeting['time_slot'] for meeting in scheduled_meetings]
        available_slots = [slot for slot in all_slots['time_slots'] if slot not in booked_slots]
        return {'status_code': 200, 'available_time_slots': available_slots}
    except Exception as e:
        return {'status_code': 500, 'message': 'An error occurred, please try again later.'}

@router.post("/schedule")
async def schedule_meet(request: Meet, background_tasks: BackgroundTasks):
    try:
        service = await get_calendar_service()
        if service:
            start_dt, end_dt = await combine_date_time(request.date, request.time_slot)
            if not start_dt or not end_dt:
                return {'status_code': 400, 'message': 'Invalid date or time format.'}
            attendee_list = [{'email': p.strip()} for p in request.emails.split(',') if p.strip()]

            meeting_description = (
                f"Meeting with Own Professional Collaboration (OPC)\n"
                f"--------------------------------------------------\n"
                f"Participants: {request.emails}\n\n"
                f"Agenda & Guidelines:\n"
                f"• Start Time: We will begin sharply at the scheduled time.\n"
                f"• Duration: Approximately 30 minutes. We are happy to extend this if the discussion requires it.\n\n"
                f"**Important Policy**:\n"
                f"Please join on time. If you do not enter the meeting within 10 minutes of the start time, "
                f"the session will be automatically cancelled.\n"
                f"If you need to reschedule, please inform us via email at least 2 hours in advance or rebook via our website.\n\n"
                f"We look forward to speaking with you.\n"
                f"- The OPC Team"
            )

            event_body = {
                'summary': 'Scheduled Meeting with OPC',
                'description': meeting_description,
                'start': {
                    'dateTime': start_dt.isoformat(),
                    'timeZone': os.getenv("TIMEZONE", "Asia/Kolkata"),
                },
                'end': {
                    'dateTime': end_dt.isoformat(),
                    'timeZone': os.getenv("TIMEZONE", "Asia/Kolkata"),
                },
                'attendees': attendee_list,
                
                'conferenceData': {
                    'createRequest': {
                        'requestId': f"meet-{int(datetime.now().timestamp())}",
                        'conferenceSolutionKey': {'type': 'hangoutsMeet'}
                    }
                }
            }

            event = service.events().insert(
                calendarId=os.getenv("CALENDAR_ID", "primary"),
                body=event_body,
                conferenceDataVersion=1,
                sendUpdates='all'
            ).execute()

            body = {
                'name': request.name,
                'emails': request.emails,
                'user_type': request.user_type,
                'date': request.date,
                'time_slot': request.time_slot,
                'google_meet_link': event.get('hangoutLink', ''),
                'created_at': datetime.now().isoformat()
            }

            _ = add(data=body, collection="SCHEDULED_MEETS", database="MEET")

            background_tasks.add_task(send_email_async, to_=os.getenv("SMTP_USER"), from_=os.getenv("SMTP_USER"), subject_=f"New Meeting Scheduled by {request.name}", body_=str(body))
            return {'status_code': 200, 'message': 'Meeting scheduled successfully.'}
        else:
            return {'status_code': 500, 'message': 'Failed to schedule meeting, please try again later.'}
    except Exception as e:
        return {'status_code': 500, 'message': f'An error occurred, please try again later.'}