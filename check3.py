import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Создание входных переменных
service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')
food = ctrl.Antecedent(np.arange(0, 11, 1), 'food')

# Определение функций принадлежности для входных переменных
service['poor'] = fuzz.trapmf(service.universe, [0, 0, 2, 5])
service['average'] = fuzz.trapmf(service.universe, [2, 5, 8, 10])
service['good'] = fuzz.trapmf(service.universe, [8, 10, 10, 10])

food['bad'] = fuzz.trapmf(food.universe, [0, 0, 2, 5])
food['acceptable'] = fuzz.trapmf(food.universe, [2, 5, 8, 10])
food['delicious'] = fuzz.trapmf(food.universe, [8, 10, 10, 10])

# Создаем выходную переменную (она не будет иметь функций принадлежности, так как это константы для Сугено)
tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip', defuzzify_method='centroid')

# Задаем правила с константными значениями для каждого правила
rule1 = ctrl.Rule(service['poor'] & food['bad'], tip['tip'] == 5)   # Если сервис плохой и еда плохая, чаевые 5%
rule2 = ctrl.Rule(service['average'] & food['acceptable'], tip['tip'] == 10)  # Если средний, то 10%
rule3 = ctrl.Rule(service['good'] & food['delicious'], tip['tip'] == 15)  # Если хороший сервис и отличная еда, то 20%

# Создание системы управления
tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

# Установка входных значений
tipping.input['service'] = 7.5
tipping.input['food'] = 8.0

# Вычисление результата
tipping.compute()

# Вывод результата
print(f"Рассчитанные чаевые: {tipping.output['tip']} %")
