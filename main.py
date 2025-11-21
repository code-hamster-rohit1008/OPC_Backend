from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from route import auth, contact_us, register_event, schedule_meet
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(router=contact_us.router, tags=["Contact Us"])
app.include_router(router=register_event.router, tags=["Register Event"])
app.include_router(router=schedule_meet.router, prefix="/meet", tags=["Schedule Meet"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)