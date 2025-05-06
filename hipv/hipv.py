# Healthcare Institution Procurement Volume 医疗机构采购量

import pandas as pd
import numpy as np
from random import choice, randint, uniform

# Original data template
original_data = [
    {"Year": 2023, "Device Name": "AI辅助诊断系统（肺部CT）", "Supplier": "深睿医疗", "Procurement Volume": 15},
    {"Year": 2022, "Device Name": "AI病理分析仪", "Supplier": "推想科技", "Procurement Volume": 8},
    {"Year": 2021, "Device Name": "AI心电图分析系统", "Supplier": "数坤科技", "Procurement Volume": 12},
    {"Year": 2020, "Device Name": "AI影像辅助诊断平台", "Supplier": "腾讯觅影", "Procurement Volume": 20},
    {"Year": 2019, "Device Name": "AI全科辅助诊疗系统", "Supplier": "依图科技", "Procurement Volume": 5},
    {"Year": 2018, "Device Name": "AI超声辅助诊断设备", "Supplier": "联影智能", "Procurement Volume": 7},
    {"Year": 2017, "Device Name": "AI手术导航系统", "Supplier": "迈瑞医疗", "Procurement Volume": 3},
    {"Year": 2016, "Device Name": "AI药物研发平台", "Supplier": "医渡云", "Procurement Volume": 2},
    {"Year": 2015, "Device Name": "AI智能问诊系统", "Supplier": "阿里健康", "Procurement Volume": 4}
]

# List of potential suppliers
suppliers = [
    "Digital Diagnostics", "Element5", "Eleos Health", "Fathom", "Infinitus", "Cleerly", "SmarterDx",
    "Lyra Health", "Hinge Health", "Everly Health", "Forward", "Arcadia", "Optum Analytics", "IBM Watson Health", 
    "SAS", "GE Healthcare", "Siemens Healthineers", "Philips Healthcare", "Arterys",
    "Butterfly Network", "Atomwise", "Praxis EMR", "Augmedix", "PathAI", "Google Health", "Microsoft Healthcare", 
    "Amazon Health", "Quibim", "Owkin", "Insitro", "Exscientia",
    "BenevolentAI", "Healx", "Causaly", "ZOE", "Color Health", "Regard", "Intelligencia AI",
    "Quris-AI", "HMNC Brain Health", "SimpleTherapy", "Vizzia Technologies", "BenchSci",
    "Heidi Health", "Elegen Corp.", "Angle Health", "CodaMetrix", "Livara Health",
    "Viz.ai", "Chordline Health", "中国信通院", "艾瑞咨询", "国家统计局", "前瞻产业研究院", "观研报告网", "Daxue Consulting",
    "CKGSB Knowledge", "ScienceDirect", "华大智造", "依图科技", "深睿医疗", "推想科技", "数坤科技", "腾讯觅影", 
    "阿里健康", "平安智慧医疗", "科亚医疗", "迈瑞医疗", "联影智能", "医渡云", "汇医慧影", "蓝帆医疗AI", "森亿智能", 
    "鹰瞳科技", "森浦医疗AI平台", "新华三AI医疗平台"
]

# Function to generate random multiplier based on year
def get_multiplier(year):
    # Base multiplier range increases over time
    if year == 2015:
        return uniform(0.92, 1.20)  # -8% to +20%
    elif year == 2016:
        return uniform(0.93, 1.25)
    elif year == 2017:
        return uniform(0.94, 1.30)
    elif year == 2018:
        return uniform(0.95, 1.35)
    elif year == 2019:
        return uniform(0.96, 1.40)
    elif year == 2020:
        return uniform(0.97, 1.50)
    elif year == 2021:
        return uniform(0.98, 1.60)
    elif year == 2022:
        return uniform(0.99, 1.70)
    elif year == 2023:
        return uniform(0.99, 1.75)
    elif year == 2024:
        return uniform(0.99, 1.75)  # -1% to +75%
    else:
        return uniform(0.95, 1.50)  # Default range

# Generate 800 records
generated_data = []
for _ in range(800):
    # Randomly select a year between 2015-2024
    year = randint(2015, 2024)
    
    # Randomly select a device template
    template = choice(original_data)
    
    # Randomly select a supplier (80% chance from new list, 20% from original)
    if np.random.random() < 0.8:
        supplier = choice(suppliers)
    else:
        supplier = template["Supplier"]
    
    # Calculate procurement volume with year-based multiplier
    base_volume = template["Procurement Volume"]
    multiplier = get_multiplier(year)
    volume = max(1, round(base_volume * multiplier))  # Ensure at least 1
    
    generated_data.append({
        "Year": year,
        "Device Name": template["Device Name"],
        "Supplier": supplier,
        "Procurement Volume": volume
    })

# Create DataFrame and save to CSV
df = pd.DataFrame(generated_data)
df = df.sort_values("Year")  # Optional: sort by year
df.to_csv("ai_medical_device_procurement.csv", index=False)

print("Generated 800 records of AI medical device procurement data.")
print("Saved to 'ai_medical_device_procurement.csv'")