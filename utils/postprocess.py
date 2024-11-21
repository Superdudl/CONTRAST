import numpy as np
import cv2
import platform


def histogram(img):
    # Вычисление гистограммы
    bins = 64
    a = cv2.calcHist([img], [0], None, [bins], ranges=(0, 256)).ravel()
    # a = np.where(a > 0, np.log(a), a)
    hist_w = 384
    hist_h = 192
    a = np.uint(0.85 * hist_h * (a / np.max(a)))

    histogram = np.zeros((hist_h, hist_w, 3), dtype=np.uint8)

    for i, x in enumerate(range(0, histogram.shape[1], int(hist_w / bins))):
        cv2.line(histogram, (x + int(hist_w / bins / 2) - 1, hist_h),
                 (x + int(hist_w / bins / 2) - 1, int(hist_h - a[i])), [255, 255, 255], int(hist_w / bins - 2))

    return histogram


def calc_contrast(img):
    # Определение маски для цифр и бумаги
    # numbers_mask = (img >= 50) & (img <= 120)
    # paper_mask = (img >= 200) & (img <= 240)
    img_shape = img.shape
    numbers_mask = cv2.threshold(img, 127, 1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    paper_mask = 1 - numbers_mask
    res = np.concatenate((img*paper_mask, img*numbers_mask), axis=1)
    if platform.system != 'Windows':
        cv2.imwrite('/home/contrast/shared/masks.png', res)

    avg_numbers = None
    avg_paper = None

    if np.any(numbers_mask) and np.any(paper_mask):
        avg_numbers = np.mean(img[img * numbers_mask > 0])
        avg_paper = np.mean(img[img * paper_mask > 0])
    contrast = avg_paper / avg_numbers if avg_numbers is not None and avg_paper is not None else None

    return {
        'avg_numbers': avg_numbers,
        'avg_paper': avg_paper,
        'contrast': contrast,
        'paper_mask': paper_mask.astype(np.uint8) * 255,
        'numbers_mask': numbers_mask.astype(np.uint8) * 255
    }

def calc_gain(frame):
    h, w = frame.shape[0], frame.shape[1]
    central_value = frame[int(h / 2), int(w / 2)]
    gain = central_value/frame
    return gain
