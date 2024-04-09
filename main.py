from fastapi import FastAPI
from redis.asyncio import Redis
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware

from m14.conf.config import settings
from m14.routes import auth, contacts, users
import uvicorn
from dotenv import load_dotenv

origins = [
    "http://localhost:8000"
    ]

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')

@app.on_event("startup")
async def startup():
    r = await Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                    decode_responses=True)
    await FastAPILimiter.init(r)

@app.get("/")
def read_root():
    return {"message": "Welcome in users contacts!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.2", port=8000)