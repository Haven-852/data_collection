# Policy Support Level (Quantitative Score) 政策支持力度（量化评分）
import pandas as pd
import numpy as np
import random

# 支持 AI 医疗政策的国家列表（40 个）
countries = [
    "United States", "Canada", "Mexico",
    "Germany", "France", "United Kingdom", "Netherlands", "Sweden", "Denmark", "Finland",
    "Belgium", "Italy", "Spain", "Austria", "Estonia", "Portugal",
    "China", "Japan", "South Korea", "India", "Singapore", "Israel", "United Arab Emirates",
    "Saudi Arabia", "Thailand",
    "Australia", "New Zealand", "Brazil", "Chile", "Argentina",
    "South Africa", "Egypt", "Kenya"
]

# 年份范围
years = list(range(2015, 2025))

# 生成政策数量（每年0-5条，核心国家略多）
policy_data = []

for country in countries:
    for year in years:
        # 中美英法德中日韩等国家发布频率较高
        if country in ["United States", "China", "United Kingdom", "Germany", "France", "Japan", "South Korea", "India"]:
            count = random.randint(10, 35)
        else:
            count = np.random.poisson(1.2)  # 平均1条左右
        policy_data.append({
            "Country": country,
            "Year": year,
            "Policy Count": int(count)
        })

# 转换为 DataFrame 并展示
df_policy = pd.DataFrame(policy_data)
print(df_policy.head())
df_policy.to_csv("ai_health_policy_count_by_country.csv", index=False)
print("已保存到文件：ai_health_policy_count_by_country.csv")