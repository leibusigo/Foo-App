# coding=utf-8
import json
import os
from flask import Blueprint, request
from libs import stats
from libs.check import check
from services import algorithm
import requests as rq

algorithm_api = Blueprint('algorithm_api', __name__)
headers = {'content-type': 'application/json'}


# 开始跟踪接口
@algorithm_api.route("/startTracking")
def start_tracking():
    epoch = request.args['epoch']
    start_result, origin_image = algorithm.start_tracking(str(epoch))
    if start_result is 'ErrIpNotFound':
        return stats.err['ErrIpNotFound'], 404
    # 请求检测照片
    detect_url = os.environ.get("PY36_SERVER_URL", None) + '/detect'
    try:
        detect_res = rq.post(
            url=detect_url,
            data=json.dumps({"image": origin_image, "epoch": epoch}),
            headers=headers
        )
        # 返回检测结果
        return stats.JsonResp(0, detect_res.json()['data']).res()
    except:
        return stats.err['ErrPy36ServerError'], 404


# 循环跟踪接口
@algorithm_api.route("/loopTracking")
def loop_tracking():
    epoch = request.args['epoch']
    if int(epoch) < 2:
        return stats.err['ErrParametersNotAllowed'], 403
    loop_result, origin_image = algorithm.loop_tracking(epoch)
    if loop_result is 'ErrIpNotFound':
        return stats.err['ErrIpNotFound'], 404
    elif loop_result == '未检测到目标':
        return stats.JsonResp(0, '未检测到目标').res()
    # 请求检测照片
    detect_url = os.environ.get("PY36_SERVER_URL", None) + '/detect'
    try:
        detect_res = rq.post(
            url=detect_url,
            data=json.dumps({"image": origin_image, "epoch": epoch}),
            headers=headers
        )
        # 返回检测结果
        return stats.JsonResp(0, detect_res.json()['data']).res()
    except:
        return stats.err['ErrPy36ServerError'], 404


# 测距跟踪接口
@algorithm_api.route("/rangeTracking")
def range_tracking():
    data = algorithm.range_and_tracking()

    return check(data)


# 停止跟踪接口
@algorithm_api.route("/stopTracking")
def stop_tracking():
    value = request.args['value']
    data = algorithm.stop_tracking(value)

    return check(data)
