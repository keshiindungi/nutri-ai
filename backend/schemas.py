# backend/schemas.py
from pydantic import BaseModel
from typing import List, Optional, Literal
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

# Update activity levels to match frontend
class ActivityLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate" 
    HIGH = "high"

class Goal(str, Enum):
    LOSE_WEIGHT = "lose_weight"
    MAINTAIN_WEIGHT = "maintain_weight"
    GAIN_WEIGHT = "gain_weight"

class DietaryPreference(str, Enum):
    NONE = "none"
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    LOW_CARB = "low_carb"

class ProfileIn(BaseModel):
    age: int
    gender: Gender
    weight_kg: float
    height_cm: float
    activity_level: ActivityLevel
    goal: Goal
    dietary_preference: DietaryPreference
    daily_budget_ksh: float
    allergies: List[str] = []
    dislikes: List[str] = []

class MealOut(BaseModel):
    meal_items: List[str]
    kcal_total: float
    protein_g: float
    price_ksh: float
    score: float