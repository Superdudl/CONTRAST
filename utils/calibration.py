import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class MlpCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MlpCanvas, self).__init__(fig)


class Mera:
    def __init__(self):
        self.value = []
        self.nominal_value = []
        self.id = None
        self.ADC = []

    def clear(self):
        self.value = []
        self.nominal_value = []
        self.id = None
        self.ADC = []

    def add_mera(self, ADC, nominal_value):
        self.ADC.append(ADC)
        self.nominal_value.append(nominal_value)
        if self.id is None:
            self.id = 1
        else:
            self.id += 1

    def delete_mera(self, id):
        if self.id is None:
            pass
        else:
            self.ADC.pop(id)
            self.nominal_value.pop(id)
            if len(self.ADC) == 0:
                self.id = None
            elif self.id > len(self.ADC):
                self.id = len(self.ADC)
            else:
                if self.id != 1:
                    self.id -= 1

    def __len__(self):
        return len(self.ADC)


def calibrate(pixel_value, nominal_value, gray_templates=False):
    n = np.size(pixel_value)
    pixel_value = np.array(pixel_value, dtype = float)
    nominal_value = np.array(nominal_value, dtype = float)

    mean_pixel_value = np.mean(pixel_value)
    mean_nominal_value = np.mean(nominal_value)

    SS_xy = np.sum(nominal_value * pixel_value) - n * mean_nominal_value * mean_pixel_value
    SS_xx = np.sum(pixel_value ** 2) - n * mean_pixel_value ** 2

    k = SS_xy / SS_xx
    b = mean_nominal_value - k * mean_pixel_value

    if gray_templates:
        LUT = k*np.linspace(0,255,256)+b
        LUT = np.uint8(np.clip(LUT,0,1)*255)
        return LUT

    return [k, b]


def plot_regression(x, y, k, b):
    plt.scatter(x, y, color='m', s=30)
    y_pred = k * np.linspace(0,255, 256) + b
    plt.plot(np.linspace(0,255, 256), y_pred, color='g')


if __name__ == '__main__':
    a = Mera()
    b = Mera()
    x = np.array([124, 102, 75, 23])
    y = np.array([0.8, 0.73, 0.6, 0.3])

    k, b = calibrate(x, y)
    print(f'k = {k}\nb = {b}')
    plot_regression(x, y, k, b)
    plt.show()
