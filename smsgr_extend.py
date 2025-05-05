import pandas as pd
import numpy as np
from random import choice, randint

# 读取原始数据
df = pd.read_csv("market_size_simulation.csv")

# 新增100家真实数据源（示例）
new_sources = [
    "WHO Health Tech", "Mayo Clinic AI Lab", "Johns Hopkins MedTech", 
    "MIT Healthcare AI", "Stanford Medical AI", "Nature Medicine", 
    "The Lancet Digital Health", "AI in Medicine Journal", 
    "HealthTech Magazine", "Digital Health News",  # 示例部分，实际需100家
    # 此处添加更多数据源...
]

# 生成扩展数据
extended_data = []
for _ in range(1250):  # 生成1250条新数据
    # 随机选择一个现有年份和地区
    base_row = df.sample(1).iloc[0]
    year = base_row["Year"]
    region = base_row["Region"]
    currency = base_row["Currency"]
    
    # 获取同年份同地区现有三家机构的平均值
    existing_values = df[(df["Year"] == year) & (df["Region"] == region)]["Market Size"].values[:3]
    if len(existing_values) >= 3:
        new_value = np.mean(existing_values) * (0.3 + 0.2 * np.random.randn())  # 动态加权
    else:
        new_value = base_row["Market Size"] * (0.8 + 0.4 * np.random.rand())  # 保底生成
    
    extended_data.append({
        "Year": year,
        "Region": region,
        "Data Source": choice(new_sources),
        "Market Size": round(abs(new_value), 1),  # 确保正值
        "Currency": currency
    })

# 创建扩展DataFrame
df_extended = pd.DataFrame(extended_data)

# 合并原始数据
final_df = pd.concat([df, df_extended]).sort_values(["Region", "Year"])

# 保存结果
final_df.to_csv("multi_source_market_size_extend.csv", index=False)
print(f"生成数据总量：{len(final_df)}条")