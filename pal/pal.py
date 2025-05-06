# Patient Acceptance Level (Survey Score) 患者接受度（调研评分）
import pandas as pd
import random
import numpy as np

# 读取问卷文件
questionnaire_path = "pal/患者AI医疗接受度问卷_单选版.csv"
question_df = pd.read_csv(questionnaire_path)

# 生成3200份答卷
num_responses = 3200
responses = []

for i in range(num_responses):
    response = {"ID": f"R{i+1}"}
    for idx, row in question_df.iterrows():
        qid = row["编号"]
        options = [opt.strip() for opt in row["选项（单选）"].split(" / ")]
        
        if qid == "Q7":
            answer = random.choices(["是", "否"], weights=[0.95, 0.05])[0]
        elif qid == "Q8":
            answer = random.choices(["是", "否"], weights=[0.90, 0.10])[0]
        elif qid in [f"Q{n}" for n in range(9, 26)]:
            main_weight = 0.5 + random.uniform(-0.1, 0.1)
            other_weight = (1 - main_weight) / (len(options) - 1)
            weights = [main_weight] + [other_weight] * (len(options) - 1)
            answer = random.choices(options, weights=weights)[0]
        else:
            answer = random.choice(options)
        
        response[qid] = answer
    responses.append(response)

# 转换为DataFrame并保存
df_responses = pd.DataFrame(responses)
output_path = "pal/患者AI医疗接受度问卷_结果样本3200份.csv"
df_responses.to_csv(output_path, index=False)