# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import engine, Base
from .routers import auth, events, users
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles



@asynccontextmanager
async def lifespan(app: FastAPI):
    # This block runs on startup
    async with engine.begin() as conn:
        # Create the database tables
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)









app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS Middleware - allows your frontend to talk to your backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your API routers
app.include_router(auth.router, tags=["Authentication"])
app.include_router(events.router, tags=["Events"])
app.include_router(users.router, prefix="/api", tags=["Users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Event Management System API"}