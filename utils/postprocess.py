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


def calc_contrast(img):
    # Определение маски для цифр и бумаги
    numbers_mask = (img >= 50) & (img <= 120)
    paper_mask = (img >= 200) & (img <= 240)

    avg_numbers = np.mean(img[numbers_mask]) if np.any(numbers_mask) else None
    avg_paper = np.mean(img[paper_mask]) if np.any(paper_mask) else None
    contrast = avg_paper / avg_numbers if avg_numbers is not None and avg_paper is not None else None

    return {
        'avg_numbers': avg_numbers,
        'avg_paper': avg_paper,
        'contrast': contrast,
        'paper_mask': paper_mask.astype(np.uint8) * 255,
        'numbers_mask': numbers_mask.astype(np.uint8) * 255
    }
