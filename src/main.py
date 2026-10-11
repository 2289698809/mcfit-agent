#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
McFit: McDonald's Calorie Actuary & Smart Meal Planner CLI.
Official Contest Project for 2026 McDonald's Developer Innovation Challenge.
"""
import sys
import argparse
from models import NutritionProfile
from nutrition_db import NutritionDatabase
from optimizer import MealOptimizer
from receipt_printer import render_receipt
from mcp_client import McDonaldMCPClient

def main():
    parser = argparse.ArgumentParser(
        description="McFit - 麦当劳卡路里精算师与减脂点餐管家",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python main.py --calories 550 --protein 30 --budget 45
  python main.py --calories 600 --protein 25 --avoid-fried --address "公司前台"
        """
    )
    parser.add_argument("--calories", type=float, default=550.0, help="最高热量上限 (kcal，默认: 550)")
    parser.add_argument("--protein", type=float, default=25.0, help="最低蛋白质目标 (g，默认: 25)")
    parser.add_argument("--budget", type=float, default=50.0, help="预算上限 (元，默认: 50)")
    parser.add_argument("--avoid-fried", action="store_true", help="严格避开油炸食品 (如薯条、炸鸡排)")
    parser.add_argument("--address", type=str, default="科技园软件大厦", help="收货地址名称")
    parser.add_argument("--token", type=str, default=None, help="麦当劳 MCP Token (可选)")

    args = parser.parse_args()

    print("\n🚀 正在启动 McFit 营养精算规划引擎...")
    mcp_client = McDonaldMCPClient(token=args.token)
    
    if mcp_client.is_configured:
        print("🔗 麦当劳官方 MCP Server 连接已就绪: https://mcp.mcd.cn")
    else:
        print("ℹ️ 未检测到外部 MCD_MCP_TOKEN，使用官方核准的基准营养数据库与离线推演引擎。")

    db = NutritionDatabase()
    optimizer = MealOptimizer(db)

    print(f"📊 规划目标: 热量 ≤ {args.calories} kcal | 蛋白质 ≥ {args.protein}g | 预算 ≤ ¥{args.budget}")
    plans = optimizer.optimize(
        max_calories=args.calories,
        min_protein=args.protein,
        max_budget=args.budget,
        avoid_fried=args.avoid_fried
    )

    if not plans:
        print("❌ 未能在当前约束条件下找到符合的餐品组合，请尝试适当放宽热量或预算限制。")
        sys.exit(1)

    print(f"✨ 成功计算出最优方案，正在生成麦门精算小票...\n")
    best_plan = plans[0]
    receipt_text = render_receipt(
        plan=best_plan,
        target_calories=args.calories,
        target_protein=args.protein,
        address=args.address
    )
    print(receipt_text)

if __name__ == "__main__":
    main()
