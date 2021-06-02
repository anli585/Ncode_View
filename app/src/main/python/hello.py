import base64

import cv2
import numpy as np
from n_util.ImageUtil import ImageClass

def add(a,b):
    return str(abs(a - b))


def count_image(imageBase64):
    decoded_string = base64.b64decode(imageBase64)
    np_data = np.fromstring(decoded_string, np.uint8)
    image = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
    if image:
        return len(image)

def countABC(a, b, c):
    try:
        return ImageClass().test_util(a, b, c)
    except Exception as ex:
        return str(ex)