"""
McDonald's Food Nutritional Database and Official Reference Cache.
Based on McDonald's China official published nutritional figures and MCP list-nutrition-foods schema.
"""
from typing import List, Dict, Optional
from models import FoodItem, NutritionProfile

# Official baseline nutrition data for typical McDonald's China menu
OFFICIAL_NUTRITION_ITEMS: List[FoodItem] = [
    # ---- 主食 (Main Course) ----
    FoodItem(
        code="MCD_BEEF_01",
        name="板烧鸡腿堡",
        category="main",
        price=23.5,
        nutrition=NutritionProfile(calories=398.0, protein=23.8, fat=15.4, carbohydrates=41.2, sodium=980.0),
        customization_tip="建议备注【不加沙拉酱】，可削减约 45 kcal 热量与 4.5g 脂肪"
    ),
    FoodItem(
        code="MCD_BEEF_02",
        name="吉士汉堡包",
        category="main",
        price=13.0,
        nutrition=NutritionProfile(calories=302.0, protein=15.6, fat=12.2, carbohydrates=32.4, sodium=680.0),
        customization_tip="高蛋白单片纯牛肉饼，性价比控卡首选"
    ),
    FoodItem(
        code="MCD_BEEF_03",
        name="双层吉士汉堡",
        category="main",
        price=22.0,
        nutrition=NutritionProfile(calories=448.0, protein=26.4, fat=23.2, carbohydrates=33.1, sodium=910.0),
        customization_tip="双份 100% 纯牛肉，力量训练后超强蛋白质补充（超 26g 蛋白）"
    ),
    FoodItem(
        code="MCD_BEEF_04",
        name="巨无霸",
        category="main",
        price=26.0,
        nutrition=NutritionProfile(calories=524.0, protein=25.8, fat=27.4, carbohydrates=43.5, sodium=1020.0),
        customization_tip="双层牛肉配生菜，碳水蛋白充足，适合作为高消耗日的主食"
    ),
    FoodItem(
        code="MCD_CHICKEN_01",
        name="麦香鸡",
        category="main",
        price=14.0,
        nutrition=NutritionProfile(calories=379.0, protein=14.2, fat=16.8, carbohydrates=42.6, sodium=750.0),
        customization_tip="建议去沙拉酱"
    ),
    FoodItem(
        code="MCD_CHICKEN_02",
        name="麦辣鸡腿汉堡",
        category="main",
        price=22.5,
        nutrition=NutritionProfile(calories=518.0, protein=21.5, fat=26.8, carbohydrates=47.6, sodium=1150.0),
        customization_tip="炸鸡外皮热量略高，减脂期建议去皮或优选板烧鸡腿堡"
    ),

    # ---- 小食与小菜 (Sides & Snacks) ----
    FoodItem(
        code="MCD_SIDE_01",
        name="麦乐鸡 (5块装)",
        category="side",
        price=14.0,
        nutrition=NutritionProfile(calories=226.0, protein=13.2, fat=12.5, carbohydrates=15.1, sodium=460.0),
        customization_tip="白肉鸡胸肉制成，搭配甜酸酱优质蛋白加餐"
    ),
    FoodItem(
        code="MCD_SIDE_02",
        name="玉米杯 (小杯)",
        category="side",
        price=9.0,
        nutrition=NutritionProfile(calories=74.0, protein=2.6, fat=1.1, carbohydrates=13.5, sodium=15.0),
        customization_tip="【绝佳减脂替餐】天然复合慢碳水 + 高膳食纤维，完美替代油炸薯条"
    ),
    FoodItem(
        code="MCD_SIDE_03",
        name="苹果片",
        category="side",
        price=8.0,
        nutrition=NutritionProfile(calories=38.0, protein=0.2, fat=0.1, carbohydrates=9.2, sodium=2.0),
        customization_tip="新鲜爽脆，维生素丰富，极低热量"
    ),
    FoodItem(
        code="MCD_SIDE_04",
        name="脆脆薯条 (小包)",
        category="side",
        price=10.0,
        nutrition=NutritionProfile(calories=222.0, protein=3.1, fat=10.6, carbohydrates=28.5, sodium=170.0),
        customization_tip="油炸高碳水，控卡阶段建议替换为玉米杯"
    ),
    FoodItem(
        code="MCD_SIDE_05",
        name="烟熏风味鸡胸肉排 (单片)",
        category="side",
        price=12.5,
        nutrition=NutritionProfile(calories=135.0, protein=18.5, fat=3.2, carbohydrates=2.1, sodium=420.0),
        customization_tip="纯蛋白质炸弹！超低脂肪超高蛋白"
    ),

    # ---- 饮品 (Drinks) ----
    FoodItem(
        code="MCD_DRINK_01",
        name="可口可乐 零度 (中杯)",
        category="drink",
        price=9.5,
        nutrition=NutritionProfile(calories=0.0, protein=0.0, fat=0.0, carbohydrates=0.0, sodium=25.0),
        customization_tip="0 糖 0 热量 0 脂肪，快乐解渴控卡神器"
    ),
    FoodItem(
        code="MCD_DRINK_02",
        name="鲜煮咖啡 (中杯/黑咖啡)",
        category="drink",
        price=10.0,
        nutrition=NutritionProfile(calories=4.0, protein=0.3, fat=0.0, carbohydrates=0.7, sodium=8.0),
        customization_tip="天然抗氧化，促进新陈代谢，去水肿优选"
    ),
    FoodItem(
        code="MCD_DRINK_03",
        name="纯牛奶 (盒装 250ml)",
        category="drink",
        price=11.0,
        nutrition=NutritionProfile(calories=162.0, protein=8.5, fat=9.0, carbohydrates=12.0, sodium=115.0),
        customization_tip="优质乳清蛋白 + 丰富天然乳钙"
    ),
    FoodItem(
        code="MCD_DRINK_04",
        name="纯水 (冰露)",
        category="drink",
        price=7.0,
        nutrition=NutritionProfile(calories=0.0, protein=0.0, fat=0.0, carbohydrates=0.0, sodium=0.0),
        customization_tip="纯净补水"
    )
]

class NutritionDatabase:
    def __init__(self, items: Optional[List[FoodItem]] = None):
        self.items: List[FoodItem] = items or OFFICIAL_NUTRITION_ITEMS
        self._code_map: Dict[str, FoodItem] = {item.code: item for item in self.items}

    def get_all(self) -> List[FoodItem]:
        return self.items

    def get_by_category(self, category: str) -> List[FoodItem]:
        return [item for item in self.items if item.category == category]

    def get_by_code(self, code: str) -> Optional[FoodItem]:
        return self._code_map.get(code)

    def search_by_name(self, keyword: str) -> List[FoodItem]:
        return [item for item in self.items if keyword in item.name]
