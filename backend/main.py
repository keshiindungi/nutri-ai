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

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(recommend_router, prefix="/recommend", tags=["Recommendation"])

# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to NutriAI API!"}