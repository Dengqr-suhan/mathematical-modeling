import pandas as pd

# 假设你的Excel文件名为 'nutrition_data.xlsx'
file_path = '种类成分表.xlsx'

# 读取Excel文件
df = pd.read_excel(file_path)

# 提取需要的列，假设第一列是食物名称，其他列包含了各种营养成分
# 这里假设蛋白质、脂肪和碳水化合物列名分别为 '蛋白质', '脂肪', '碳水化合物'
required_columns = ['主要成分', '蛋白质', '脂肪', '碳水化合物']

# 只保留需要的列
df = df[required_columns]

# 将数据转换为所需的字典格式
nutrition_dict = {}
for index, row in df.iterrows():
    food_name = row['主要成分']
    nutrition_dict[food_name] = {
        '蛋白质': row['蛋白质'],
        '脂肪': row['脂肪'],
        '碳水化合物': row['碳水化合物']
    }

# 输出结果
print(nutrition_dict)
