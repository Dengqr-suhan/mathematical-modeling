import math


weights = {
    '蛋白质': 0.2,
    '脂肪': 0.2,
    '碳水化合物': 0.3,
    '餐次比': 0.3
}



def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def standardize_score(gap, scale_factor=5):
    x = (scale_factor / 2 - abs(gap)) / scale_factor
    return round(sigmoid(x) * 100, 2)

def score_nutrient(gap, weight, scale_factor=5):
    return standardize_score(gap, scale_factor) * weight

def score_meal_ratio(actual_ratios, ideal_ratios, weight, scale_factor=5):
    scores = [standardize_score(abs(actual - ideal), scale_factor) for actual, ideal in
              zip(actual_ratios, ideal_ratios)]
    return round(sum(scores) * (weight / len(ideal_ratios)), 2)

male_data = {
    '蛋白质': {'摄入量': 140.21, '占比差距': 2.56},
    '脂肪': {'摄入量': 87.14, '占比差距': -3.95},
    '碳水化合物': {'摄入量': 594.93, '占比差距': 1.39},
    '餐次比': (26.10, 51.68, 22.22)
}

female_data = {
    '蛋白质': {'摄入量': 90.97, '占比差距': 12.52},
    '脂肪': {'摄入量': 36.30, '占比差距': -2.54},
    '碳水化合物': {'摄入量': 191.01, '占比差距': -9.97},
    '餐次比': (21.64, 35.16, 43.19)
}

ideal_meal_ratios = [30, 40, 30]

male_scores = {
    nutrient: score_nutrient(data['占比差距'], weights[nutrient])
    for nutrient, data in male_data.items() if nutrient != '餐次比'
}
male_scores['餐次比'] = score_meal_ratio(male_data['餐次比'], ideal_meal_ratios, weights['餐次比'])
male_total_score = sum(male_scores.values())

female_scores = {
    nutrient: score_nutrient(data['占比差距'], weights[nutrient])
    for nutrient, data in female_data.items() if nutrient != '餐次比'
}
female_scores['餐次比'] = score_meal_ratio(female_data['餐次比'], ideal_meal_ratios, weights['餐次比'])
female_total_score = sum(female_scores.values())

print(f"男生膳食质量指数总评分: {male_total_score}")
print(f"女生膳食质量指数总评分: {female_total_score}")
