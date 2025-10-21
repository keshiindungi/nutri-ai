# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.recommend import router as recommend_router  # Import the router directly

# Create the FastAPI app
app = FastAPI(
    title="NutriAI - AI-Powered Nutrition Recommendation System",
    description="Provides affordable meal and diet suggestions using AI and nutrition data.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers - FIX: Remove the prefix to simplify
app.include_router(recommend_router, tags=["Recommendation"])
# Root endpoint

@app.get("/")
def home():
    return {"message": "Welcome to NutriAI API!"}