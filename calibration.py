import numpy as np
import matplotlib.pyplot as plt


class Mera:
    def __init__(self):
        self.value = []
        self.nominal_value = []

    def add_mera(self, value, nominal_value):
        self.value.append(value)
        self.nominal_value.append(nominal_value)

    def delete_mera(self, id):
        self.value.pop(id)
        self.nominal_value.pop(id)

    def __len__(self):
        return len(self.value)


def calibrate(pixel_value, nominal_value, gray_templates=None):
    n = np.size(pixel_value)

    mean_pixel_value = np.mean(pixel_value)
    mean_nominal_value = np.mean(nominal_value)

    SS_xy = np.sum(nominal_value * pixel_value) - n * mean_nominal_value * mean_pixel_value
    SS_xx = np.sum(pixel_value ** 2) - n * mean_pixel_value ** 2

    k = SS_xy / SS_xx
    b = mean_nominal_value - k * mean_pixel_value

    if gray_templates is not None:
        optical_density_gray = k * gray_templates + b

        return optical_density_gray

    return [k, b]


def plot_regression(x, y, k, b):
    plt.scatter(x, y, color='m', s=30)

    y_pred = k * x + b

    plt.plot(x, y_pred, color='g')


if __name__ == '__main__':
    a = Mera(0, 22, 1)
    b = Mera(0, 22, 1)
    x = np.array([10, 100, 180, 240])
    y = np.array([15, 40, 60, 90])

    k, b = calibrate(x, y)
    print(f'k = {k}\nb = {b}')
    plot_regression(x, y, k, b)
    plt.show()
