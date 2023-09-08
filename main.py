import uvicorn
from fastapi import FastAPI
from routers import rooms, users, courses, logs, participants
import auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(rooms.router)
app.include_router(logs.router)
app.include_router(auth.router)
app.include_router(participants.router)

origins = [
    "http://localhost",
    "http://localhost:8088",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
