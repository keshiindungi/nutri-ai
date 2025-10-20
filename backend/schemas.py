# backend/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"
    LIGHT = "light"
    MODERATE = "moderate"
    ACTIVE = "active"
    VERY_ACTIVE = "very_active"

class Goal(str, Enum):
    LOSE_WEIGHT = "lose_weight"
    MAINTAIN_WEIGHT = "maintain_weight"
    GAIN_WEIGHT = "gain_weight"

class DietaryPreference(str, Enum):
    ANY = "any"
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    KETO = "keto"
    LOW_CARB = "low_carb"

class ProfileIn(BaseModel):
    age: int
    gender: str
    weight_kg: float
    height_cm: float
    activity_level: Literal["low", "moderate", "high"]
    goal: Literal["maintain", "lose", "gain"]
    daily_budget_ksh: float
    dietary_preference: str = "none"
    allergies: List[str] = []
    dislikes: List[str] = []

class MealOut(BaseModel):
    meal_items: List[str]
    kcal_total: float
    protein_g: float
    price_ksh: float
    score: float