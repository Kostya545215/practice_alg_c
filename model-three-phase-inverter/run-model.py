import matlab.engine
import pandas as pd
import matplotlib.pyplot as plt
import configparser
import sys

HELP_TEXT = """
[general]
description = Программа для запуска моделирования трехфазного инвертора и выведения графиков тока и напряжения на нагрузке. 
important_note = Важно иметь ввиду, что модель работает в 1000 раз медленнее, поэтому при задании, например, 0.1 секунды симуляции, она будет выполняться 100 секунд.

[parameters]
config = Название конфигурации (например 'config1')
csv_file = Путь к CSV файлу (ввод/вывод)
Time_simulation = Время симуляции (по умолчанию 0.01)
R_load = Сопротивление нагрузки в омах (по умолчанию 50)
C_load = Ёмкость нагрузки в фарадах (по умолчанию 0.01)
L_load = Индуктивность нагрузки в генри (по умолчанию 0.0001)
voltage = Напряжение источника в вольтах (по умолчанию 50)

"""

def show_help():
    """Показывает справку"""
    config = configparser.ConfigParser()
    config.read_string(HELP_TEXT)
    
    print("\n" + config['general']['description'])
    print("\nВажно!: " + config['general']['important_note'])
    print("\nПараметры:")
    for param, desc in config['parameters'].items():
        print(f"  {param}: {desc}")
    print()


def start_simulation(config, csv_file, **kwargs):
    eng = matlab.engine.start_matlab()   

    args = [config, csv_file]

    for key, value in kwargs.items():
        args.extend([key, value])

    eng.three_phase_inverter(*args, nargout=0)

    eng.quit()

def draw_plot(csv_file):

    data = pd.read_csv(csv_file)

    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize = (12, 10))

    ax1.plot(data['Time']/100, data['current1'], linewidth=2)
    ax1.plot(data['Time']/100, data['current2'], linewidth=2)
    ax1.plot(data['Time']/100, data['current3'], linewidth=2)
    ax1.set_title('График токов на нагрузке', fontsize=14)
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    ax2.plot(data['Time']/100, data['voltage1'], linewidth=1)
    ax2.plot(data['Time']/100, data['voltage2'], linewidth=1)
    ax2.plot(data['Time']/100, data['voltage3'], linewidth=1)
    ax2.set_title('График напряжения на нагрузке', fontsize=14)
    ax2.grid(True, linestyle='--', alpha=0.7)

    plt.xlabel('Время', fontsize=12)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":

    if '--help' in sys.argv or '-h' in sys.argv:
        show_help()
    else:
        start_simulation("config1", r"C:\Users\Konstantin\Desktop\test.csv", Time_simulation=0.01)
        draw_plot(r"C:\Users\Konstantin\Desktop\test.csv")