import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Определяем входные и выходные переменные
quality = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')
service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')
tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')

# Определяем функции принадлежности для входных и выходных переменных
quality.automf(3)  # Автоматически создаём poor, average, good
service.automf(3)
tip['low'] = fuzz.trimf(tip.universe, [0, 0, 13])
tip['medium'] = fuzz.trimf(tip.universe, [0, 13, 25])
tip['high'] = fuzz.trimf(tip.universe, [13, 25, 25])

# Изменяем метод дефаззификации на 'bisector'
tip.defuzzify_method = 'centroid'

# Правила для нечеткой системы
rule1 = ctrl.Rule(quality['poor'] | service['poor'], tip['low'])
rule2 = ctrl.Rule(service['average'], tip['medium'])
rule3 = ctrl.Rule(service['good'] | quality['good'], tip['high'])

# Создаём систему контроля
tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

# Устанавливаем значения для входных переменных
tipping.input['quality'] = 6.5
tipping.input['service'] = 9.8

# Вычисляем результат
tipping.compute()

# Печатаем результат
print(f"Результат чаевых: {tipping.output['tip']}")

# Визуализируем выходную переменную с новой агрегацией
tip.view(sim=tipping)
plt.show()
