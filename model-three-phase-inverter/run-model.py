import matlab.engine
import pandas as pd
import matplotlib.pyplot as plt

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

    start_simulation("config1", r"C:\Users\Konstantin\Desktop\test.csv", Time_simulation=0.01)
    draw_plot(r"C:\Users\Konstantin\Desktop\test.csv")