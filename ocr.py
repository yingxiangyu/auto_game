from dataclasses import dataclass

import easyocr

from utils import Point

reader = easyocr.Reader(['ch_sim', 'en'])  # this needs to run only once to load the model into memory


@dataclass
class OcrRet:
    text: str
    point: Point


def image_ocr(image):
    result = reader.readtext(image)
    rets = []
    for i in result:
        box = i[0]
        text = i[1]
        top_x = box[0][0]
        top_y = box[0][1]
        width = box[1][0] - box[0][0]
        high = box[2][1] - box[0][1]
        point_x = top_x + width // 2
        point_y = top_y + high // 2
        rets.append(OcrRet(text, Point(int(point_x), int(point_y))))
    return rets


if __name__ == '__main__':
    import pyautogui
    import numpy as np

    im = pyautogui.screenshot()
    print(image_ocr(np.array(im)))
