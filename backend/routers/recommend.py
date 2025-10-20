# backend/routers/recommend.py
from fastapi import APIRouter, HTTPException
from typing import List
import json
from pathlib import Path


# Import from the same package
from backend.schemas import ProfileIn, MealOut
from backend.utils.calculations import estimate_calories_daily, filter_foods, score_meal_combo

router = APIRouter()

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "food_data.json"

@router.post("/", response_model=dict)
def recommend(profile: ProfileIn):
    # load food DB
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            food_db = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Food database not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid food database format")

    daily_cal = estimate_calories_daily(profile)
    candidates = filter_foods(profile, food_db)

    # generate combos (single + pairs)
    combos = []
    for i in range(len(candidates)):
        combos.append([candidates[i]])
        for j in range(i+1, len(candidates)):
            combos.append([candidates[i], candidates[j]])

    scored = []
    for combo in combos:
        score, cost = score_meal_combo(combo, profile, daily_cal)
        # keep only reasonably priced meals
        if cost <= max(1, profile.daily_budget_ksh * 0.6):
            scored.append((score, cost, combo))

    if not scored:
        raise HTTPException(status_code=404, detail="No suitable meal combos found for the given profile & budget")

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:6]

    recommendations = []
    for score, cost, combo in top:
        recommendations.append(
            {
                "meal_items": [c["name"] for c in combo],
                "kcal_total": sum(c["kcal"] for c in combo),
                "protein_g": sum(c["protein"] for c in combo),
                "price_ksh": cost,
                "score": round(score, 3)
            }
        )

    return {"daily_calorie_target": daily_cal, "recommendations": recommendations}