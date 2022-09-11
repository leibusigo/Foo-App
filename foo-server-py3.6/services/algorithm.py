# coding=utf-8
import os
from PIL import Image
from paddleocr import PaddleOCR
import cv2
import re
import db
import numpy as np
from yolo import YOLO

yolo = YOLO()


# yolo检测
def yolo_detect(image_url, epoch):
    try:
        image = Image.open(image_url)
        # 使用目标检测算法对图片进行检测
        r_image, flag, top_arr, bottom_arr, left_arr, right_arr = yolo.detect_image(image)
        # 将得到的数组转化为图片的形式
        r_image = np.array(r_image, np.uint8)
        # 将颜色从BGR转换为RGB
        r_image = cv2.cvtColor(r_image, cv2.COLOR_BGR2RGB)
        data = dict(
            top_arr=top_arr,
            bottom_arr=bottom_arr,
            left_arr=left_arr,
            right_arr=right_arr,
            r_image=r_image
        )
        base_url = os.environ.get("IMG_SAVE_PATH", None) + '/epoch' + str(epoch)
        cv2.imwrite(base_url + '/detect.jpg', r_image)
        if flag:
            return 'success', base_url + '/detect.jpg', 'found', data
        else:
            return 'success', base_url + '/detect.jpg', 'not found', 0
    except FileNotFoundError as e:
        return 'ErrFileNotFound', '', '', 0


# ocr识别
def ocr_test(r_image, top, bottom, left, right, epoch):
    crop_img = r_image[top:bottom, left:right]
    base_url = os.environ.get("IMG_SAVE_PATH", None) + '/epoch' + str(epoch)
    cv2.imwrite(base_url + '/cut.jpg', crop_img)
    zoom = super_resolution(crop_img, top, bottom, left, right, base_url)
    # Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
    # 参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`。
    ocr = PaddleOCR(use_angle_cls=True, lang="en")  # need to run only once to download and load model into memory
    result = ocr.ocr(zoom, cls=True)
    i = 0
    text_arr = []
    while i < len(result):
        text_arr.append(result[i][1][0])
        i += 1

    return text_arr


# 文字匹配
def reg_word(text_arr, top, bottom, left, right):
    if len(text_arr) != 0:
        for text_num in range(len(text_arr)):
            regexp = re.compile(r'H')
            # 用正则方法匹配ocr检测到的字符
            if regexp.search(text_arr[text_num]):
                # 存入数据库
                db.coordinates.delete_many({})
                db.coordinates.insert({
                    "top": str(top),
                    "bottom": str(bottom),
                    "left": str(left),
                    "right": str(right)
                })

                return 'ocr识别到特定目标物品'

        return '物品上不存在特定标记'
    else:
        return '该物品无标记'


# 双三次插值主程序
def super_resolution(crop_img, top, bottom, left, right, base_url):
    zoom = function(crop_img, (bottom - top) * 5, (right - left) * 5)
    cv2.imwrite(base_url + "/resolution_result.jpg", zoom)

    return zoom


# 双三次插值内部执行函数
def S(x):
    x = np.abs(x)
    if 0 <= x < 1:
        return 1 - 2 * x * x + x * x * x
    if 1 <= x < 2:
        return 4 - 8 * x + 5 * x * x - x * x * x
    else:
        return 0


# 双三次插值
def function(img, m, n):
    height, width, channels = img.shape
    empty_image = np.zeros((m, n, channels), np.uint8)
    sh = m / height
    sw = n / width
    for i in range(m):
        for j in range(n):
            x = i / sh
            y = j / sw
            p = (i + 0.0) / sh - x
            q = (j + 0.0) / sw - y
            x = int(x) - 2
            y = int(y) - 2
            A = np.array([
                [S(1 + p), S(p), S(1 - p), S(2 - p)]
            ])
            if x >= m - 3:
                m - 1
            if y >= n - 3:
                n - 1
            if 1 <= x <= (m - 3) and 1 <= y <= (n - 3):
                B = np.array([
                    [img[x - 1, y - 1], img[x - 1, y],
                     img[x - 1, y + 1],
                     img[x - 1, y + 1]],
                    [img[x, y - 1], img[x, y],
                     img[x, y + 1], img[x, y + 2]],
                    [img[x + 1, y - 1], img[x + 1, y],
                     img[x + 1, y + 1], img[x + 1, y + 2]],
                    [img[x + 2, y - 1], img[x + 2, y],
                     img[x + 2, y + 1], img[x + 2, y + 1]],
                ])
                C = np.array([
                    [S(1 + q)],
                    [S(q)],
                    [S(1 - q)],
                    [S(2 - q)]
                ])
                blue = np.dot(np.dot(A, B[:, :, 0]), C)[0, 0]
                green = np.dot(np.dot(A, B[:, :, 1]), C)[0, 0]
                red = np.dot(np.dot(A, B[:, :, 2]), C)[0, 0]

                # adjust the value to be in [0,255]
                def adjust(value):
                    if value > 255:
                        value = 255
                    elif value < 0:
                        value = 0
                    return value

                blue = adjust(blue)
                green = adjust(green)
                red = adjust(red)
                empty_image[i, j] = np.array([blue, green, red], dtype=np.uint8)

    return empty_image
