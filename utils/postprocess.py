import numpy as np
import cv2
import platform


def histogram(img, log=False):
    # Вычисление гистограммы
    bins = 64
    a = cv2.calcHist([img], [0], None, [bins], ranges=(0, 256)).ravel()
    if log:
        a = np.where(a > 0, np.log10(a), a)
    hist_w = 384
    hist_h = 192
    a = np.uint(0.85 * hist_h * (a / np.max(a)))

    histogram = np.zeros((hist_h, hist_w, 3), dtype=np.uint8)

    for i, x in enumerate(range(0, histogram.shape[1], int(hist_w / bins))):
        cv2.line(histogram, (x + int(hist_w / bins / 2) - 1, hist_h),
                 (x + int(hist_w / bins / 2) - 1, int(hist_h - a[i])), [255, 255, 255], int(hist_w / bins - 2))

    return histogram


def calc_contrast(img):
    numbers_mask = cv2.threshold(img, 127, 1, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    paper_mask = 1 - numbers_mask
    res = np.concatenate((img * paper_mask, img * numbers_mask), axis=1)
    if platform.system != 'Windows':
        cv2.imwrite('/home/contrast/shared/masks.png', res)

    avg_numbers = None
    avg_paper = None
    if np.any(numbers_mask) and np.any(paper_mask):
        unique_numbers, counts1 = np.unique(img[img * numbers_mask > 0].ravel(), return_counts=True)
        unique_paper, counts2 = np.unique(img[img * paper_mask > 0].ravel(), return_counts=True)
        if counts1.size != 0 and counts2.size != 0:
            avg_numbers = unique_numbers[np.argmax(counts1)]
            avg_paper = unique_paper[np.argmax(counts2)]
            # avg_numbers = np.mean(img[img * numbers_mask > 0])
            # avg_paper = np.mean(img[img * paper_mask > 0])
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
    gain = central_value / frame
    return np.float32(gain)
