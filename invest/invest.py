import pandas as pd
import numpy as np
from random import uniform, choice, randint

# 基础配置
np.random.seed(42)
regions = ["Global", "China", "USA", "India", "Japan", "EU"]
data_sources = {
    "Global": ["CB Insights", "Crunchbase", "PitchBook"],
    "China": ["IT桔子", "清科研究中心", "企查查"],
    "USA": ["CB Insights", "Crunchbase", "PitchBook"],
    "India": ["Tracxn", "VCCEdge", "Inc42"],
    "Japan": ["METI Reports", "JETRO", "SeedTable"],
    "EU": ["Dealroom", "EU Startups", "Sifted"]
}

# 生成独立基准数据（每个数据源单独生成）
def generate_individual_series(region, source):
    """为每个数据源生成独立基准序列"""
    base_values = {
        # Global
        ("Global", "CB Insights"): [6.5, 8.2, 12.1, 18.9, 27.0, 40.0, 75.0, 122.0, 98.0, 115.0],
        ("Global", "Crunchbase"): [6.8, 8.5, 12.5, 19.2, 28.0, 42.0, 78.0, 125.0, 102.0, 120.0],
        ("Global", "PitchBook"): [6.3, 7.9, 11.8, 18.5, 26.5, 38.0, 72.0, 118.0, 95.0, 112.0],
        # China
        ("China", "IT桔子"): [0.8, 1.2, 1.9, 3.1, 5.6, 9.8, 18.5, 12.3, 16.0, 21.5],
        ("China", "清科研究中心"): [0.7, 1.1, 1.8, 3.0, 5.8, 10.2, 19.1, 12.8, 16.5, 22.0],
        ("China", "企查查"): [0.9, 1.3, 2.0, 3.3, 5.4, 9.5, 17.9, 12.0, 15.8, 21.0],
        # USA
        ("USA", "CB Insights"): [3.2, 4.1, 5.8, 9.5, 15.0, 24.0, 45.0, 73.0, 60.0, 70.0],
        ("USA", "Crunchbase"): [3.4, 4.3, 6.1, 9.8, 15.5, 25.0, 47.0, 75.0, 62.0, 72.0],
        ("USA", "PitchBook"): [3.0, 3.9, 5.6, 9.2, 14.5, 23.0, 43.0, 70.0, 58.0, 68.0],
        # India
        ("India", "Tracxn"): [0.15, 0.22, 0.35, 0.58, 1.05, 1.9, 2.8, 4.2, 3.5, 4.8],
        ("India", "VCCEdge"): [0.18, 0.25, 0.38, 0.62, 1.12, 2.1, 3.0, 4.5, 3.8, 5.1],
        ("India", "Inc42"): [0.12, 0.20, 0.32, 0.55, 0.98, 1.8, 2.6, 4.0, 3.3, 4.6],
        # Japan
        ("Japan", "METI Reports"): [0.3, 0.4, 0.6, 0.9, 1.5, 2.2, 3.2, 5.0, 4.2, 5.5],
        ("Japan", "JETRO"): [0.32, 0.42, 0.63, 0.95, 1.55, 2.3, 3.3, 5.2, 4.3, 5.6],
        ("Japan", "SeedTable"): [0.28, 0.38, 0.57, 0.85, 1.45, 2.1, 3.1, 4.8, 4.1, 5.4],
        # EU
        ("EU", "Dealroom"): [1.2, 1.6, 2.3, 3.5, 5.2, 7.8, 9.5, 12.1, 10.5, 13.0],
        ("EU", "EU Startups"): [1.3, 1.7, 2.4, 3.6, 5.4, 8.0, 9.8, 12.3, 10.8, 13.3],
        ("EU", "Sifted"): [1.1, 1.5, 2.2, 3.4, 5.0, 7.6, 9.3, 11.9, 10.3, 12.8]
    }
    return base_values.get((region, source), [None]*10)

# 数据生成主逻辑
investment_data = []
for region in regions:
    for year in range(2015, 2025):
        # 随机选择一个数据源设为null（5%概率）
        null_source = choice(data_sources[region]) if randint(1, 20) == 1 else None
        
        for source in data_sources[region]:
            # 获取基准值
            base_series = generate_individual_series(region, source)
            base_value = base_series[year-2015] if (year-2015) < len(base_series) else None
            
            # 添加±5%波动
            if base_value is not None:
                value = base_value * (1 + uniform(-0.05, 0.05))
                value = round(value, 2)
            else:
                value = None
                
            # 应用null设置
            if source == null_source:
                value = None
                
            investment_data.append({
                "Year": year,
                "Region": region,
                "Data Source": source,
                "Investment (USD Billion)": value
            })

# 创建DataFrame
df = pd.DataFrame(investment_data)

# 后处理验证
# 确保同一年份不同来源数据差异不超过15%
for (region, year), group in df.groupby(['Region', 'Year']):
    valid_values = group['Investment (USD Billion)'].dropna()
    if len(valid_values) > 1:
        max_diff = (valid_values.max() - valid_values.min())/valid_values.min()
        if max_diff > 0.15:
            # 自动修正超过15%的差异
            median = valid_values.median()
            df.loc[group.index, 'Investment (USD Billion)'] = valid_values.apply(
                lambda x: round(median*(1 + uniform(-0.05, 0.05)), 2))

# 保存CSV
df.to_csv("multi_source_investment.csv", index=False)
print("生成数据示例：")
print(df.head(10))