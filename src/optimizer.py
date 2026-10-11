"""
Multi-objective Combinatorial Optimizer for McFit Meal Planning.
Maximizes protein and satiety while enforcing calorie and budget constraints.
"""
from typing import List, Optional, Tuple
from models import FoodItem, MealPlan, Coupon, NutritionProfile
from nutrition_db import NutritionDatabase

class MealOptimizer:
    def __init__(self, db: NutritionDatabase):
        self.db = db

    def optimize(
        self,
        max_calories: float = 600.0,
        min_protein: float = 25.0,
        max_budget: float = 50.0,
        prefer_category: Optional[str] = None,
        avoid_fried: bool = False,
        available_coupons: Optional[List[Coupon]] = None
    ) -> List[MealPlan]:
        """
        Generate candidate meal plans ranked by fitness score.
        """
        mains = self.db.get_by_category("main")
        sides = self.db.get_by_category("side")
        drinks = self.db.get_by_category("drink")

        if avoid_fried:
            mains = [m for m in mains if "炸" not in m.name and "麦辣" not in m.name]
            sides = [s for s in sides if "薯条" not in s.name]

        valid_plans: List[MealPlan] = []

        # Combination strategy 1: 1 Main + 1 Side + 1 Drink
        for m in mains:
            for s in sides:
                for d in drinks:
                    plan = MealPlan(items=[m, s, d])
                    plan.recalculate()
                    if plan.total_nutrition.calories <= max_calories and plan.original_price <= max_budget:
                        valid_plans.append(plan)

        # Combination strategy 2: 1 Main + 1 Drink (minimalist snack/light lunch)
        for m in mains:
            for d in drinks:
                plan = MealPlan(items=[m, d])
                plan.recalculate()
                if plan.total_nutrition.calories <= max_calories and plan.original_price <= max_budget:
                    valid_plans.append(plan)

        # Combination strategy 3: 1 Main + 2 Sides (e.g. burger + chicken + corn)
        for m in mains:
            for s1 in sides:
                for s2 in sides:
                    if s1.code != s2.code:
                        plan = MealPlan(items=[m, s1, s2])
                        plan.recalculate()
                        if plan.total_nutrition.calories <= max_calories and plan.original_price <= max_budget:
                            valid_plans.append(plan)

        # Apply coupons if available
        coupons = available_coupons or [
            Coupon("CPN_01", "麦麦省满35减8券", discount_amount=8.0, min_spend=35.0),
            Coupon("CPN_02", "麦麦省满25减5券", discount_amount=5.0, min_spend=25.0),
        ]

        for plan in valid_plans:
            self._apply_best_coupon(plan, coupons)

        # Rank plans by comprehensive fitness score
        # Objective: High protein, close to calorie target without exceeding, high protein/price ratio
        def fitness_score(p: MealPlan) -> float:
            nut = p.total_nutrition
            protein_score = nut.protein * 2.5
            cal_penalty = 0.0
            if nut.calories > max_calories:
                cal_penalty = (nut.calories - max_calories) * 10
            
            # Bonus for meeting min protein target
            protein_bonus = 20.0 if nut.protein >= min_protein else -10.0

            # Economic efficiency (Protein per CNY)
            eff_score = (nut.protein / max(p.final_price, 1.0)) * 15.0

            # Fat penalty (prevent overly greasy options)
            fat_penalty = nut.fat * 0.5

            return protein_score + protein_bonus + eff_score - cal_penalty - fat_penalty

        valid_plans.sort(key=fitness_score, reverse=True)
        return valid_plans[:3]

    def _apply_best_coupon(self, plan: MealPlan, coupons: List[Coupon]):
        best_coupon: Optional[Coupon] = None
        max_discount = 0.0

        for cpn in coupons:
            if plan.original_price >= cpn.min_spend:
                if cpn.discount_amount > max_discount:
                    max_discount = cpn.discount_amount
                    best_coupon = cpn

        if best_coupon:
            plan.applied_coupons = [best_coupon]
            plan.discount_amount = best_coupon.discount_amount
            plan.recalculate()
