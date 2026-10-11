# 🍔 McFit · 麦当劳卡路里精算师与减脂点餐管家

<p align="center">
  <img src="https://img.shields.io/badge/McDonald's-China_MCP_Official-FFC72C?style=for-the-badge&logo=mcdonalds&logoColor=DA291C" alt="McDonald's MCP" />
  <img src="https://img.shields.io/badge/Challenge-2026_Developer_Innovation-red?style=for-the-badge" alt="Contest" />
  <img src="https://img.shields.io/badge/Partner-WorkBuddy-blue?style=for-the-badge" alt="WorkBuddy" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</p>

> **让快餐秒变科学减脂餐！**  
> 基于**麦当劳官方 Model Context Protocol (MCP)** 深度打造，集「食品级营养成分精算」、「高蛋白低脂餐品推荐」、「麦麦省智能一键领券」与「麦乐送对话式下单」于一体的专属健康饮食智能体。

---

## 🌟 项目亮点与痛点解决

现代都市白领与健身爱好者经常面临**“外卖高热量、做饭没时间、想吃快餐又有罪恶感”**的困扰。虽然麦当劳拥有众多高品质、高蛋白的优质食材（如 100% 纯牛肉、精选白羽鸡胸肉、纯牛奶、玉米杯），但由于缺乏智能搭配工具，大众往往无从下手。

**McFit** 利用麦当劳官方开放的 **20+ 核心 MCP 工具**，彻底打通了**营养数据、门店库存、优惠券体系与订单履约系统**：

- 🥩 **高蛋白控卡算法**：用户只需给出目标（如“预算 550 kcal，蛋白质 ≥ 30g”），算法自动匹配热量达标、饱腹感最强的黄金组合；
- 🥗 **独家特制减脂小贴士**：自动标注“板烧去沙拉酱/去皮”、“薯条换玉米杯”，轻松削减隐形热量；
- 🎟️ **麦麦省一键智能领券**：自动调用 `auto-bind-coupons`，将全部可用满减券一网打尽，并算出实付最低到手价；
- 🧾 **极客风精算小票**：清晰直观输出三大宏量营养素（碳水、蛋白质、脂肪）分析小票与下单短链，实现 5 秒点餐决策。

---

## 🏗️ 架构与调用流程

本项目遵循 **“需求解析 ➔ 营养规划 ➔ 门店校验 ➔ 卡券叠加 ➔ 闭环下单”** 的严密业务管道：

```mermaid
flowchart LR
    A[用户输入营养与就餐需求] --> B(list-nutrition-foods\n获取官方真实营养库)
    B --> C(McFit 规划算法\n求解三大宏量营养素最优解)
    C --> D(delivery-query-stores\n校验附近营业门店与菜单)
    D --> E(auto-bind-coupons\n自动一键领取满减券)
    E --> F(calculate-price\n核算最优折扣与实付到手价)
    F --> G[输出精算小票 & 确认下单]
```

详细的接口映射表与 Mermaid 时序图参见 👉 [MCP_INTEGRATION.md](./MCP_INTEGRATION.md)。

---

## 🧾 真实运行效果演示 (示例精算小票)

当向 McFit 发送指令：  
> *“教练，我今晚练了背，晚饭热量预算 550 大卡内，蛋白质要大于 30g，不要太贵，帮我配一份麦当劳送到公司前台。”*

**McFit 输出的精算小票如下：**

```text
========================================================
        🍔 麦当劳 McFit · 营养精算与点餐小票 🍔
========================================================
【就餐目标】: 控卡减脂 (目标 ≤ 550 kcal, 蛋白质 ≥ 30g)
【就餐方式】: 麦乐送外送 (科技园软件大厦前台)
--------------------------------------------------------
【精选餐品组合】:
  1. 板烧鸡腿堡  (¥23.50)
     热量: 398.0 kcal | 蛋白质: 23.8g | 脂肪: 15.4g | 碳水: 41.2g
     💡 贴士: 建议备注【不加沙拉酱】，可削减约 45 kcal 热量与 4.5g 脂肪
  2. 麦乐鸡 (5块装)  (¥14.00)
     热量: 226.0 kcal | 蛋白质: 13.2g | 脂肪: 12.5g | 碳水: 15.1g
     💡 贴士: 白肉鸡胸肉制成，搭配甜酸酱优质蛋白加餐
  3. 可口可乐 零度 (中杯)  (¥9.50)
     热量: 0.0 kcal | 蛋白质: 0.0g | 脂肪: 0.0g | 碳水: 0.0g
     💡 贴士: 0 糖 0 热量 0 脂肪，快乐解渴控卡神器
--------------------------------------------------------
【宏量营养素统计】:
  🔥 总能量 (Calories)   :  524.0 kcal  (低于上限 26.0 kcal ✅)
  🥩 总蛋白质 (Protein)  :   37.0 g     (达标: 超出 7.0g ✅)
  🥑 总脂肪 (Fat)        :   27.9 g
  🍞 总碳水 (Carbs)      :   56.3 g
  🧂 总钠含量 (Sodium)   : 1440.0 mg
--------------------------------------------------------
【价格与优惠精算】:
  餐品门市原价  : ¥  47.00
  优惠券自动减免: -¥   8.00 (麦麦省满35减8券)
  麦乐送外送配送费: +¥   9.00
  💰 实付到手价 : ¥  48.00
========================================================
祝您用餐愉快！保持能量与健康，越吃越轻盈！
👉 回复【确认下单】为您立即创建订单并生成收银台支付链接！
```

---

## 🚀 快速上手 (Quick Start)

### 方式一：在 WorkBuddy / Cursor / Trae 中作为 Skill 启用（推荐）

1. **申请麦当劳 MCP Token**：  
   登录 [麦当劳开放平台](https://open.mcd.cn/mcp) 控制台，激活并复制你的 `MCP Token`。

2. **配置连接器**：  
   在 WorkBuddy 的【专家·技能·连接器】➔【连接器】➔【自定义连接器】中粘贴以下配置：
   ```json
   {
     "mcpServers": {
       "mcd-mcp": {
         "type": "streamablehttp",
         "url": "https://mcp.mcd.cn",
         "headers": {
           "Authorization": "Bearer YOUR_MCP_TOKEN"
         }
       }
     }
   }
   ```

3. **载入 Skill 提示词**：  
   将本项目根目录下的 [`skill_prompt.md`](./skill_prompt.md) 内容导入至 WorkBuddy 自定义 Skill 或系统提示词中，开启对话即可！

---

### 方式二：本地 Python 规划引擎运行

克隆代码并在本地运行：

```bash
# 1. 运行核心规划算法 (默认目标: 550大卡, 25g蛋白)
python src/main.py

# 2. 自定义参数运行
python src/main.py --calories 600 --protein 35 --budget 50 --address "家里的地址"
```

---

## 📁 目录规范结构

```text
mcfit-agent/
├── CONTEST_DECLARATION.md    # 官方参赛声明 (必须且内容未修改)
├── MCP_INTEGRATION.md        # 麦当劳 MCP 协议接入深度说明与时序图
├── workbuddy.md              # WorkBuddy 协同开发实录 (专项奖励凭证)
├── skill_prompt.md           # McFit 智能体角色与系统提示词规范
├── README.md                 # 项目介绍与使用指南
├── LICENSE                   # MIT 开源协议
└── src/
    ├── models.py             # 营养档案、餐品、卡券与订单数据模型
    ├── nutrition_db.py       # 麦当劳官方食品营养参考库与缓存
    ├── optimizer.py          # 多目标宏量营养素组合优化算法
    ├── receipt_printer.py    # 结构化麦门营养精算小票渲染器
    ├── mcp_client.py         # 麦当劳官方 Streamable HTTP MCP 客户端
    └── main.py               # 命令行交互与推演主程序
```

---

## 📜 参赛声明与开源协议

- 本项目严格遵守 [CONTEST_DECLARATION.md](./CONTEST_DECLARATION.md) 所载之原创性与合规性声明。
- 本项目采用 [MIT License](./LICENSE) 协议开源，欢迎各位“麦门信徒”与开发者点亮 🌟 **Star** 支持！
