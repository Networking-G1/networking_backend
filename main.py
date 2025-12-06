# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables
from routers import users, auth_routes
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Networking Backend")

# CORS configuration
origins = os.getenv("CORS_ORIGINS", "")
origins_list = [o.strip() for o in origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins_list or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
create_db_and_tables()

# Include routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def root():
    return {"message": "Backend funcionando correctamente 🚀"}
