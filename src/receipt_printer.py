"""
Receipt formatter for McFit meal plans.
Generates aesthetic and structured text receipts suitable for terminal or chat displays.
"""
from models import MealPlan

def render_receipt(plan: MealPlan, target_calories: float, target_protein: float, address: str = "默认常用外送地址") -> str:
    lines = []
    w = 56
    lines.append("=" * w)
    lines.append("        🍔 麦当劳 McFit · 营养精算与点餐小票 🍔".center(w - 6))
    lines.append("=" * w)
    lines.append(f"【就餐目标】: 控卡减脂 (目标 ≤ {target_calories:.0f} kcal, 蛋白质 ≥ {target_protein:.0f}g)")
    lines.append(f"【就餐方式】: 麦乐送外送 ({address})")
    lines.append("-" * w)
    lines.append("【精选餐品组合】:")

    for idx, item in enumerate(plan.items, 1):
        lines.append(f"  {idx}. {item.name}  (¥{item.price:.2f})")
        lines.append(f"     热量: {item.nutrition.calories} kcal | 蛋白质: {item.nutrition.protein}g | 脂肪: {item.nutrition.fat}g | 碳水: {item.nutrition.carbohydrates}g")
        if item.customization_tip:
            lines.append(f"     💡 贴士: {item.customization_tip}")

    lines.append("-" * w)
    nut = plan.total_nutrition
    cal_diff = target_calories - nut.calories
    cal_status = f"低于上限 {cal_diff:.1f} kcal ✅" if cal_diff >= 0 else f"超标 {-cal_diff:.1f} kcal ⚠️"
    
    prot_diff = nut.protein - target_protein
    prot_status = f"达标 (超出 {prot_diff:.1f}g) ✅" if prot_diff >= 0 else f"缺口 {-prot_diff:.1f}g ⚠️"

    lines.append("【宏量营养素统计】:")
    lines.append(f"  🔥 总能量 (Calories)   : {nut.calories:>6.1f} kcal  ({cal_status})")
    lines.append(f"  🥩 总蛋白质 (Protein)  : {nut.protein:>6.1f} g     ({prot_status})")
    lines.append(f"  🥑 总脂肪 (Fat)        : {nut.fat:>6.1f} g")
    lines.append(f"  🍞 总碳水 (Carbs)      : {nut.carbohydrates:>6.1f} g")
    lines.append(f"  🧂 总钠含量 (Sodium)   : {nut.sodium:>6.1f} mg")
    lines.append("-" * w)
    lines.append("【价格与优惠精算】:")
    lines.append(f"  餐品门市原价  : ¥ {plan.original_price:>6.2f}")
    if plan.applied_coupons:
        for c in plan.applied_coupons:
            lines.append(f"  优惠券自动减免: -¥ {c.discount_amount:>5.2f} ({c.title})")
    else:
        lines.append("  优惠券自动减免: -¥   0.00 (无可用满减券)")
    lines.append(f"  麦乐送外送配送费: +¥ {plan.delivery_fee:>5.2f}")
    lines.append(f"  💰 实付到手价 : ¥ {plan.final_price:>6.2f}")
    lines.append("=" * w)
    lines.append("祝您用餐愉快！保持能量与健康，越吃越轻盈！")
    lines.append("=" * w)
    return "\n".join(lines)
