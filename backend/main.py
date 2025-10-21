from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.recommend import router as recommend_router
import os
import uvicorn

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
        "https://nutri-ai-1-5djx.onrender.com",  
        "https://nutri-ai-v3kd.onrender.com",       # optional if backend also calls itself
    ],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommend_router, tags=["Recommendation"])

@app.get("/")
def home():
    return {"message": "Welcome to NutriAI API!"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port)
