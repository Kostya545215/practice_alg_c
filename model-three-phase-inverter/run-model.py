import matlab.engine
import pandas as pd
import matplotlib.pyplot as plt

eng = matlab.engine.start_matlab()  
eng.three_phase_inverter(
    "config2",
    r"C:\Users\Konstantin\Desktop\test.csv",
    "Time_simulation",
    100, 
    nargout=0
)

eng.quit()

# Чтение данных из CSV файла
data = pd.read_csv(r"C:\Users\Konstantin\Desktop\test.csv")

# Создание фигуры
plt.figure(figsize=(12, 6))

# Построение графиков для каждого сигнала
plt.plot(data['Time'], data['sin1'], linewidth=2)
plt.plot(data['Time'], data['sin2'], linewidth=2)
plt.plot(data['Time'], data['sin3'], linewidth=2)

# Настройка графика
plt.title('График токов на нагрузке', fontsize=14)
plt.xlabel('Время', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=10)

# Автоматическое масштабирование осей
plt.autoscale(enable=True, axis='both', tight=True)

# Показать график
plt.tight_layout()
plt.show()

