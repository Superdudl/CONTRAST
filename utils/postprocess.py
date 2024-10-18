import numpy as np
import cv2


def histogram(img):
    # Вычисление гистограммы
    bins = 64
    a = cv2.calcHist([img], [0], None, [bins], ranges=(0, 256)).ravel()

    hist_w = 384
    hist_h = 192
    a = np.uint(0.85 * hist_h * (a / np.max(a)))

    histogram = np.zeros((hist_h, hist_w, 3), dtype=np.uint8)

    for i, x in enumerate(range(0, histogram.shape[1], int(hist_w / bins))):
        cv2.line(histogram, (x + int(hist_w / bins / 2) - 1, hist_h),
                 (x + int(hist_w / bins / 2) - 1, int(0.95 * hist_h - a[i])), [255, 255, 255], int(hist_w / bins - 2))

    return histogram
