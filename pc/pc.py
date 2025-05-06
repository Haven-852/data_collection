# Patent Count / Number of Patents 专利数量

import pandas as pd
import numpy as np
from random import choice, uniform, randint
from faker import Faker

# 初始化Faker用于生成随机公司名（补充用）
fake = Faker()

# 国家/地区基准数据（基于真实占比）
country_baseline = {
    "Global": 100856,  # 基准值
    "China": 69700,    # 69.7%
    "USA": 14250,      # 14.2%
    "EU": 8493,        # 欧盟
    "Japan": 3625,     
    "India": 1514,
    "South Korea": 259,
    "UK": 879,        # 补充国家
    "Canada": 963,
    "Australia": 432,
    "France": 741
}

# 已知企业及国家映射（真实企业）
company_country_map = {
    # 国际企业
    "IBM Watson Health": "USA",
    "GE Healthcare": "USA",
    "Siemens Healthineers": "EU",
    "Philips Healthcare": "EU",
    "Google Health": "USA",
    "Microsoft Healthcare": "USA",
    # 中国企业
    "平安智慧医疗": "China",
    "腾讯觅影": "China",
    "依图科技": "China",
    "数坤科技": "China",
    "联影智能": "China",
    "深睿医疗": "China",
    # 其他国际企业
    "Digital Diagnostics": "USA",
    "Butterfly Network": "USA",
    "Owkin": "France",
    "Exscientia": "UK"
}

# 补充企业列表（用于达到1128条数据）
additional_companies = [
    "华大智造", "科亚医疗", "迈瑞医疗", "医渡云", "森亿智能",
    "PathAI", "Infervision", "Arterys", "Viz.ai", "Proscia"
]

# 生成国家年度专利数据（固定比例增长）
def generate_country_data():
    data = []
    for year in range(2015, 2025):
        for country, base in country_baseline.items():
            # 中国增速略高（30-35%），其他国家20-30%
            growth = 0.3 + 0.05*np.random.random() if country == "China" else 0.2 + 0.1*np.random.random()
            
            # 添加随机波动（保留国家间比例）
            noise = uniform(0.9, 1.1)
            patents = int(base * (1 + growth) ** (year - 2015) * noise)
            
            data.append({
                "Year": year,
                "Region": country,
                "Patent Count": max(10, patents)  # 确保最小10项
            })
    return pd.DataFrame(data)

# 生成企业专利数据（考虑国家和头部效应）
def generate_company_data(total_records=1128):
    data = []
    company_list = list(company_country_map.keys()) + additional_companies
    
    # 先填充已知企业
    for year in range(2015, 2025):
        for company in company_country_map:
            country = company_country_map[company]
            country_ratio = country_baseline[country]/country_baseline["Global"]
            
            # 头部企业专利更多（平安、西门子等）
            if company in ["平安智慧医疗", "Siemens Healthineers", "Philips Healthcare"]:
                base = randint(800, 1200)
            elif company in ["IBM Watson Health", "GE Healthcare", "腾讯觅影"]:
                base = randint(300, 600)
            else:
                base = randint(50, 200)
            
            growth = 0.25 + 0.15*np.random.random()  # 企业增速25-40%
            patents = int(base * (1 + growth) ** (year - 2015) * uniform(0.8, 1.2))
            
            data.append({
                "Year": year,
                "Company": company,
                "Country": country,
                "Patent Count": max(1, patents)
            })
    
    # 补充随机企业数据直到达到1128条
    while len(data) < total_records:
        year = randint(2015, 2024)
        country = choice(list(country_baseline.keys())[1:])  # 不选Global
        
        # 30%概率生成中国公司名
        if country == "China" and np.random.random() < 0.3:
            company = choice(["AI医疗科技", "智能诊断", "深蓝医疗"]) + fake.company_suffix()
        else:
            company = fake.company()
        
        # 根据国家基准确定专利范围
        country_patents = country_baseline[country] * (1 + 0.3) ** (year - 2015)
        base = country_patents * uniform(0.0001, 0.001)  # 企业占比
        
        patents = int(base * uniform(0.5, 2.0))  # 添加企业个体差异
        
        data.append({
            "Year": year,
            "Company": company,
            "Country": country,
            "Patent Count": max(1, patents)
        })
    
    return pd.DataFrame(data)

# 生成并保存数据
country_df = generate_country_data()
company_df = generate_company_data()

# 合并部分国家数据到企业文件（展示比例）
sample_country_data = country_df[~country_df["Region"].isin(["Global"])].sample(50)
company_df = pd.concat([company_df, sample_country_data.rename(columns={"Region": "Company"})])

company_df.to_csv("ai_medical_patents_1128_records.csv", index=False)
print(f"生成完成！总计{len(company_df)}条数据已保存到ai_medical_patents_1128_records.csv")