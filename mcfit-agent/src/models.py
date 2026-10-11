"""
Data models for McFit Nutrition and Ordering Agent.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class NutritionProfile:
    calories: float       # kcal
    protein: float        # g
    fat: float            # g
    carbohydrates: float  # g
    sodium: float = 0.0   # mg

    def __add__(self, other: 'NutritionProfile') -> 'NutritionProfile':
        return NutritionProfile(
            calories=round(self.calories + other.calories, 1),
            protein=round(self.protein + other.protein, 1),
            fat=round(self.fat + other.fat, 1),
            carbohydrates=round(self.carbohydrates + other.carbohydrates, 1),
            sodium=round(self.sodium + other.sodium, 1)
        )

@dataclass
class FoodItem:
    code: str
    name: str
    category: str        # 'main', 'side', 'drink', 'dessert'
    price: float         # CNY
    nutrition: NutritionProfile
    customization_tip: str = ""
    is_available: bool = True

@dataclass
class Coupon:
    coupon_id: str
    title: str
    discount_amount: float
    min_spend: float = 0.0

@dataclass
class MealPlan:
    items: List[FoodItem] = field(default_factory=list)
    total_nutrition: NutritionProfile = field(default_factory=lambda: NutritionProfile(0, 0, 0, 0, 0))
    original_price: float = 0.0
    discount_amount: float = 0.0
    delivery_fee: float = 9.0
    final_price: float = 0.0
    applied_coupons: List[Coupon] = field(default_factory=list)

    def recalculate(self):
        total_nut = NutritionProfile(0, 0, 0, 0, 0)
        total_price = 0.0
        for item in self.items:
            total_nut = total_nut + item.nutrition
            total_price += item.price
        self.total_nutrition = total_nut
        self.original_price = round(total_price, 2)
        self.final_price = round(max(0.0, total_price - self.discount_amount + self.delivery_fee), 2)
