import pandas as pd

# 读取Excel文件
file_path = '种类成分表.xlsx'  # 替换为你的Excel文件路径
df = pd.read_excel(file_path)

# 指定需要除以100的列
columns_to_divide = [
    '异亮氨酸 (g/100g)', '亮氨酸 (g/100g)', '赖氨酸 (g/100g)', 
    '含硫氨基酸 (g/100g)', '芳香族氨基酸 (g/100g)', '苏氨酸 (g/100g)', 
    '色氨酸 (g/100g)', '缬氨酸 (g/100g)'
]

# 对指定列的所有数值除以100
df[columns_to_divide] = df[columns_to_divide] / 100

# 保存修改后的DataFrame到新的Excel文件
output_file_path = '种类成分表1.xlsx'  # 替换为你希望保存的Excel文件路径
df.to_excel(output_file_path, index=False)

print("操作完成，文件已保存到：", output_file_path)
