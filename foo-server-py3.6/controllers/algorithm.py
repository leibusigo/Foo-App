# coding=utf-8
from flask import Blueprint, request
from libs import stats
from services import algorithm

algorithm_api = Blueprint('algorithm_api', __name__)


# 连接机器人接口
@algorithm_api.route("/detect", methods=["POST"])
def detect():
    image_url = request.json['image']
    epoch = request.json['epoch']
    # 进行目标检测
    detect_result, detect_url, detect_status, detect_data = algorithm.yolo_detect(image_url, epoch)
    # 异常
    if detect_result != 'success':
        return stats.err[detect_result], 404
    # 未找到物品
    elif detect_status == 'not found':
        return stats.JsonResp(0, '没有目标物品').res()
    # 找到物品
    else:
        print(detect_data)
