# backend/routers/recommend.py
from fastapi import APIRouter, HTTPException
from typing import List
import json
from pathlib import Path
import logging

# Import from the same package
from backend.schemas import ProfileIn, MealOut
from backend.utils.calculations import estimate_calories_daily, filter_foods, score_meal_combo

router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "food_data.json"

@router.post("/recommend", response_model=dict)
def recommend(profile: ProfileIn):
    try:
        logger.info(f"Received profile: {profile.dict()}")
        
        # load food DB
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                food_db = json.load(f)
            logger.info(f"Loaded {len(food_db)} food items from database")
        except FileNotFoundError:
            logger.error("Food database file not found")
            raise HTTPException(status_code=500, detail="Food database not found")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in food database: {e}")
            raise HTTPException(status_code=500, detail="Invalid food database format")

        # Calculate daily calories
        daily_cal = estimate_calories_daily(profile)
        logger.info(f"Estimated daily calories: {daily_cal}")

        # Filter foods
        candidates = filter_foods(profile, food_db)
        logger.info(f"Filtered to {len(candidates)} candidate foods")

        if not candidates:
            raise HTTPException(status_code=404, detail="No foods match your dietary preferences")

        # generate combos (single + pairs)
        combos = []
        for i in range(len(candidates)):
            combos.append([candidates[i]])
            for j in range(i+1, len(candidates)):
                combos.append([candidates[i], candidates[j]])

        logger.info(f"Generated {len(combos)} meal combinations")

        scored = []
        for combo in combos:
            score, cost = score_meal_combo(combo, profile, daily_cal)
            # keep only reasonably priced meals
            if cost <= max(1, profile.daily_budget_ksh * 0.6):
                scored.append((score, cost, combo))

        logger.info(f"Scored {len(scored)} affordable meal combinations")

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

        logger.info(f"Returning {len(recommendations)} recommendations")
        return {"daily_calorie_target": daily_cal, "recommendations": recommendations}
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log any unexpected errors
        logger.error(f"Unexpected error in recommend endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")