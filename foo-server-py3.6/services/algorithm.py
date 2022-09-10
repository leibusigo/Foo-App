# coding=utf-8
import os
from PIL import Image
from flask import request
import cv2
import numpy as np
from yolo import YOLO

yolo = YOLO()


#
def yolo_detect(image_url, epoch):
    try:
        image = Image.open(image_url)
        # 使用目标检测算法对图片进行检测
        r_image, flag, top_arr, bottom_arr, left_arr, right_arr = yolo.detect_image(image)
        data = dict(top_arr=top_arr, bottom_arr=bottom_arr, left_arr=left_arr, right_arr=right_arr)
        # 将得到的数组转化为图片的形式
        r_image = np.array(r_image, np.uint8)
        # 将颜色从BGR转换为RGB
        r_image = cv2.cvtColor(r_image, cv2.COLOR_BGR2RGB)
        base_url = os.environ.get("IMG_SAVE_PATH", None) + '/epoch' + str(epoch)
        cv2.imwrite(base_url + '/detect.jpg', r_image)
        if flag:
            return 'success', base_url + '/detect.jpg', 'found', data
        else:
            return 'success', base_url + '/detect.jpg', 'not found', 0
    except FileNotFoundError as e:
        return 'ErrFileNotFound', '', '', 0
