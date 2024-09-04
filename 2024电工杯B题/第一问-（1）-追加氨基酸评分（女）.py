import pandas as pd

nutrient_content_df = pd.read_excel("女大学生营养成分表.xlsx")

nutrient_content_per_100g = {}
for index, row in nutrient_content_df.iterrows():
    food_name = row['食物名称']
    nutrient_content_per_100g[food_name] = {
        '碳水化合物': row['碳水化合物 (g/100g)'],
        '蛋白质': row['蛋白质 (g/100g)'],
        '脂肪': row['脂肪 (g/100g)'],
        '钙': row['钙 (mg/100g)'],
        '铁': row['铁 (mg/100g)'],
        '锌': row['锌 (mg/100g)'],
        '维生素A': row['维生素A (μg/100g)'],
        '维生素B1': row['维生素B1 (mg/100g)'],
        '维生素B2': row['维生素B2 (mg/100g)'],
        '维生素C': row['维生素C (mg/100g)'],
        '异亮氨酸': row['异亮氨酸 (g/100g)'],
        '亮氨酸': row['亮氨酸 (g/100g)'],
        '赖氨酸': row['赖氨酸 (g/100g)'],
        '含硫氨基酸': row['含硫氨基酸 (g/100g)'],
        '芳香族氨基酸': row['芳香族氨基酸 (g/100g)'],
        '苏氨酸': row['苏氨酸 (g/100g)'],
        '色氨酸': row['色氨酸 (g/100g)'],
        '缬氨酸': row['缬氨酸 (g/100g)']
    }

recipe = {
    '早餐': {
        '豆浆_黄豆': (10, 1),
        '鸡排面_小麦粉': (50, 1),
        '鸡排面_鸡肉': (40, 1),
        '鸡排面_豆油': (5, 1),
    },
    '午餐': {
        '鸡蛋饼_小麦粉': (25, 1),
        '鸡蛋饼_鸡蛋': (20, 1),
        '鸡蛋饼_火腿肠': (20, 1),
        '鸡蛋饼_豆油': (5, 1),
        '水饺_小麦粉': (50, 1),
        '水饺_猪肉': (20, 1),
        '水饺_白菜': (40, 1),
        '水饺_豆油': (10, 1),
        '葡萄': (100, 1),
    },
    '晚餐': {
        '大米饭_稻米': (25 * 2, 2),
        '香菇炒油菜_油菜': (100, 0.5),
        '香菇炒油菜_香菇': (20, 0.5),
        '香菇炒油菜_豆油': (5, 0.5),
        '炒肉蒜台_蒜台': (100, 0.5),
        '炒肉蒜台_猪肉': (30, 0.5),
        '炒肉蒜台_豆油': (5, 0.5),
        '茄汁沙丁鱼': (100, 0.5),
        '苹果': (100, 1),
    },
}

total_food_types = 0
for meal, foods in recipe.items():
    total_food_types += len(foods)

average_food_types_per_day = total_food_types / len(recipe)

if average_food_types_per_day > 12:
    print("平均每天摄入食物种类数量大于12种")
else:
    print("平均每天摄入食物种类数量不足12种")

total_energy = sum([sum([nutrient_content_per_100g[food][nutrient] * amount * servings / 100
                         for nutrient in ['蛋白质', '脂肪', '碳水化合物']])
                    for foods in recipe.values() for food, (amount, servings) in foods.items()])

energy_breakfast = sum([sum([nutrient_content_per_100g[food][nutrient] * amount * servings / 100
                             for nutrient in ['蛋白质', '脂肪', '碳水化合物']])
                        for food, (amount, servings) in recipe['早餐'].items()])
energy_lunch = sum([sum([nutrient_content_per_100g[food][nutrient] * amount * servings / 100
                         for nutrient in ['蛋白质', '脂肪', '碳水化合物']])
                    for food, (amount, servings) in recipe['午餐'].items()])
energy_dinner = sum([sum([nutrient_content_per_100g[food][nutrient] * amount * servings / 100
                          for nutrient in ['蛋白质', '脂肪', '碳水化合物']])
                     for food, (amount, servings) in recipe['晚餐'].items()])

percent_breakfast = (energy_breakfast / total_energy) * 100
percent_lunch = (energy_lunch / total_energy) * 100
percent_dinner = (energy_dinner / total_energy) * 100

print(f"早餐能量占比：{percent_breakfast:.2f}%")
print(f"午餐能量占比：{percent_lunch:.2f}%")
print(f"晚餐能量占比：{percent_dinner:.2f}%")

reference_percent_breakfast = (30, 30)
reference_percent_lunch = (30, 40)
reference_percent_dinner = (30, 40)

if percent_breakfast < reference_percent_breakfast[0]:
    print("早餐能量占比低于参考值")
elif percent_breakfast > reference_percent_breakfast[1]:
    print("早餐能量占比高于参考值")
else:
    print("早餐能量占比符合参考值")

if percent_lunch < reference_percent_lunch[0]:
    print("午餐能量占比低于参考值")
elif percent_lunch > reference_percent_lunch[1]:
    print("午餐能量占比高于参考值")
else:
    print("午餐能量占比符合参考值")

if percent_dinner < reference_percent_dinner[0]:
    print("晚餐能量占比低于参考值")
elif percent_dinner > reference_percent_dinner[1]:
    print("晚餐能量占比高于参考值")
else:
    print("晚餐能量占比符合参考值")

carbs_intake = sum([sum([nutrient_content_per_100g[food]['碳水化合物'] * amount * servings / 100
                         for food, (amount, servings) in foods.items()])
                    for foods in recipe.values()])
protein_intake = sum([sum([nutrient_content_per_100g[food]['蛋白质'] * amount * servings / 100
                           for food, (amount, servings) in foods.items()])
                      for foods in recipe.values()])
fat_intake = sum([sum([nutrient_content_per_100g[food]['脂肪'] * amount * servings / 100
                       for food, (amount, servings) in foods.items()])
                  for foods in recipe.values()])

daily_energy_requirement = 1900

protein_percent = (protein_intake * 4 / daily_energy_requirement) * 100
fat_percent = (fat_intake * 9 / daily_energy_requirement) * 100
carbs_percent = (carbs_intake * 4 / daily_energy_requirement) * 100

print(f"每日摄入的蛋白质量：{protein_intake:.2f}克")
print(f"每日摄入的脂肪量：{fat_intake:.2f}克")
print(f"每日摄入的碳水化合物量：{carbs_intake:.2f}克")

print(f"蛋白质占总能量的百分比：{protein_percent:.2f}%")
print(f"脂肪占总能量的百分比：{fat_percent:.2f}%")
print(f"碳水化合物占总能量的百分比：{carbs_percent:.2f}%")

reference_protein_percent = (10, 15)
reference_fat_percent = (20, 30)
reference_carbs_percent = (50, 65)

if protein_percent < reference_protein_percent[0]:
    print("蛋白质摄入量低于参考值")
elif protein_percent > reference_protein_percent[1]:
    print("蛋白质摄入量高于参考值")
else:
    print("蛋白质摄入量符合参考值")

if fat_percent < reference_fat_percent[0]:
    print("脂肪摄入量低于参考值")
elif fat_percent > reference_fat_percent[1]:
    print("脂肪摄入量高于参考值")
else:
    print("脂肪摄入量符合参考值")

if carbs_percent < reference_carbs_percent[0]:
    print("碳水化合物摄入量低于参考值")
elif carbs_percent > reference_carbs_percent[1]:
    print("碳水化合物摄入量高于参考值")
else:
    print("碳水化合物摄入量符合参考值")

reference_amino_acids = {
    '异亮氨酸': 40,
    '亮氨酸': 70,
    '赖氨酸': 55,
    '含硫氨基酸': 35,
    '芳香族氨基酸': 60,
    '苏氨酸': 40,
    '色氨酸': 10,
    '缬氨酸': 50
}

total_protein = 0
total_amino_acid_scores = {}

for foods in recipe.values():
    for food, (amount, servings) in foods.items():
        total_protein += nutrient_content_per_100g[food].get('蛋白质', 0) * (amount / 100) * servings
        for amino_acid, reference_score in reference_amino_acids.items():
            if amino_acid in nutrient_content_per_100g[food]:
                amino_acid_content = nutrient_content_per_100g[food][amino_acid]
                score = min((amino_acid_content / reference_score), 1)
                total_amino_acid_scores[amino_acid] = total_amino_acid_scores.get(amino_acid, 0) + score * (amount / 100) * servings

total_aas_score = sum(total_amino_acid_scores.values()) / len(reference_amino_acids)

print("总氨基酸评分：", total_aas_score)

