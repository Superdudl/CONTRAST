import time
import numpy as np
import cv2
import logging
import matplotlib.pyplot as plt

logging.basicConfig(filemode='w', filename='timer.log', level=logging.INFO)


def profiler(func):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        retval = func(*args, **kwargs)
        t1 = time.time()
        logging.info(f'Function {func.__name__}: {t1 - t0:.4f}')
        return retval

    return wrapper


@profiler
def postprocess(img):
    # Определение маски для цифр и бумаги
    numbers_mask = (img >= 50) & (img <= 120)
    paper_mask = (img >= 200) & (img <= 240)

    # Вычисление гистограммы
    t0 = time.time()
    bins = 128
    a = cv2.calcHist([img], [0], None, [bins], ranges=(0, 256)).ravel()

    hist_w = 384
    hist_h = 192
    a = np.uint(0.85 * hist_h * (a / np.max(a)))

    histogram = np.zeros((hist_h, hist_w, 3), dtype=np.uint8)

    for i, x in enumerate(range(0, histogram.shape[1], int(hist_w / bins))):
        cv2.line(histogram, (x + int(hist_w / bins / 2), hist_h),
                 (x + int(hist_w / bins / 2), int(0.95 * hist_h - a[i])), [255, 255, 255], int(hist_w / bins - 2))

    t1 = time.time()
    print(f'Time: {t1 - t0:.6}')

    avg_numbers = np.mean(img[numbers_mask]) if np.any(numbers_mask) else None
    avg_paper = np.mean(img[paper_mask]) if np.any(paper_mask) else None
    contrast = avg_paper / avg_numbers if avg_numbers is not None and avg_paper is not None else None

    return {
        "histogram": histogram,
        'avg_numbers': avg_numbers,
        'avg_paper': avg_paper,
        'contrast': contrast,
        'paper_mask': paper_mask.astype(np.uint8) * 255,
        'numbers_mask': numbers_mask.astype(np.uint8) * 255
    }


if __name__ == '__main__':
    img = cv2.imread('banknota.jpg', cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (2048, 1596))

    res = postprocess(img)

    print(f'avg_numbers = {res["avg_numbers"]}\n'
          f'avg_paper = {res["avg_paper"]}\n'
          f'contrast = {res["contrast"]}')

    # Show histogram
    cv2.namedWindow('HISTOGRAM', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('HISTOGRAM', res['histogram'])

    img_numbers = img & res['numbers_mask']
    img_paper = img & res['paper_mask']

    image = np.concatenate([img_numbers, img_paper], axis=1)
    plt.imshow(image, cmap='gray')
    plt.show()
