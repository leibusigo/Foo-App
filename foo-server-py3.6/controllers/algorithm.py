# coding=utf-8
import math
from PIL import Image
from flask import Blueprint
from flask import request
from libs import stats
from services import algorithm
from yolo import YOLO

yolo = YOLO()
algorithm_api = Blueprint('algorithm_api', __name__)


# 连接机器人接口
@algorithm_api.route("/detect")
def detect():
    image_url = request.args['image']
    image = Image.open(image_url)
    # 使用目标检测算法对图片进行检测
    r_image, flag, top, bottom, left, right = yolo.detect_image(image)
    # 返回的四个坐标值现在为数组
    print(top, bottom, left, right)

    return stats.JsonResp(0, '通信成功').res()




