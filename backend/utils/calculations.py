# backend/utils/calculations.py
from typing import List, Dict, Any, Tuple
from backend.schemas import ProfileIn
import logging

logger = logging.getLogger(__name__)

def estimate_calories_daily(profile: ProfileIn) -> float:
    """
    Estimate daily calorie needs using Mifflin-St Jeor Equation
    """
    try:
        logger.info(f"Calculating calories for: {profile.dict()}")
        
        if profile.gender.value == "male":
            bmr = 10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age + 5
        else:
            bmr = 10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age - 161
        
        logger.info(f"BMR calculated: {bmr}")
        
        # Activity multipliers - match frontend values
        activity_multipliers = {
            "low": 1.375,
            "moderate": 1.55, 
            "high": 1.725
        }
        
        activity_level = profile.activity_level.value
        if activity_level not in activity_multipliers:
            raise ValueError(f"Unknown activity level: {activity_level}")
            
        maintenance_calories = bmr * activity_multipliers[activity_level]
        logger.info(f"Maintenance calories: {maintenance_calories}")
        
        # Adjust for goal
        goal = profile.goal.value
        if goal == "lose_weight":
            result = maintenance_calories * 0.8  # 20% deficit
        elif goal == "gain_weight":
            result = maintenance_calories * 1.2  # 20% surplus
        else:  # maintain
            result = maintenance_calories
            
        logger.info(f"Final daily calories: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error in estimate_calories_daily: {str(e)}")
        raise

def filter_foods(profile: ProfileIn, food_db: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter foods based on dietary preferences, allergies, and dislikes
    """
    try:
        logger.info(f"Filtering foods for dietary preference: {profile.dietary_preference.value}")
        filtered = []
        
        for food in food_db:
            # Skip if food contains allergens
            if any(allergy.lower() in food.get('tags', []) for allergy in profile.allergies):
                continue
                
            # Skip if food contains disliked items
            if any(dislike.lower() in food.get('name', '').lower() for dislike in profile.dislikes):
                continue
                
            # Filter by dietary preference
            dietary_pref = profile.dietary_preference.value
            if dietary_pref != "none":
                food_tags = [tag.lower() for tag in food.get('tags', [])]
                
                if dietary_pref == "vegetarian" and "meat" in food_tags:
                    continue
                elif dietary_pref == "vegan" and any(tag in food_tags for tag in ["meat", "dairy", "eggs"]):
                    continue
                elif dietary_pref == "low_carb" and food.get('carbs', 0) > 20:
                    continue
            
            filtered.append(food)
        
        logger.info(f"Filtered from {len(food_db)} to {len(filtered)} foods")
        return filtered
        
    except Exception as e:
        logger.error(f"Error in filter_foods: {str(e)}")
        raise

def score_meal_combo(combo: List[Dict[str, Any]], profile: ProfileIn, daily_cal: float) -> Tuple[float, float]:
    """
    Score a meal combination based on nutrition and cost
    """
    try:
        total_calories = sum(food.get('kcal', 0) for food in combo)
        total_protein = sum(food.get('protein', 0) for food in combo)
        total_cost = sum(food.get('price_ksh', 0) for food in combo)
        
        # Ideal meal calories (assuming 3 meals per day)
        ideal_meal_calories = daily_cal / 3
        
        # Score components (0-1 each)
        calorie_score = 1 - min(abs(total_calories - ideal_meal_calories) / ideal_meal_calories, 1)
        
        # Protein target (1.6-2.2g per kg for active individuals)
        protein_target = profile.weight_kg * 1.8 / 3  # per meal
        protein_score = min(total_protein / protein_target, 1) if protein_target > 0 else 0
        
        # Cost efficiency (lower cost is better, but not zero)
        cost_score = 1 - min(total_cost / profile.daily_budget_ksh, 1)
        
        # Variety score (more items is better, but not too many)
        variety_score = min(len(combo) / 3, 1)
        
        # Weighted final score
        final_score = (
            calorie_score * 0.4 +
            protein_score * 0.3 +
            cost_score * 0.2 +
            variety_score * 0.1
        )
        
        return final_score, total_cost
        
    except Exception as e:
        logger.error(f"Error in score_meal_combo: {str(e)}")
        raise