import pandas as pd

# 重新读取数据
input_path = "market/multi_source_market_size.csv"
df = pd.read_csv(input_path)

# 按照 Data Source 和 Region 进行分组，计算每年增长率
growth_data = []

for (region, source), group in df.groupby(["Region", "Data Source"]):
    group_sorted = group.sort_values("Year")
    prev_year = None
    prev_value = None
    for _, row in group_sorted.iterrows():
        year = row["Year"]
        value = row["Market Size"]
        if prev_year is not None:
            growth_rate = (value - prev_value) / prev_value if prev_value != 0 else None
            growth_data.append({
                "Region": region,
                "Data Source": source,
                "From Year": prev_year,
                "To Year": year,
                "Growth Rate (%)": round(growth_rate * 100, 2) if growth_rate is not None else None
            })
        prev_year = year
        prev_value = value

# 转换为DataFrame并保存
df_growth = pd.DataFrame(growth_data)
output_path = "market/market_growth_rate_by_source.csv"
df_growth.to_csv(output_path, index=False)