# coding=utf-8
import os
from flask import Blueprint, request
from libs import stats
from libs.check import check
from services import algorithm
import requests as rq

algorithm_api = Blueprint('algorithm_api', __name__)
headers = {'content-type': 'application/json'}


# 连接机器人接口
@algorithm_api.route("/tracking")
def tracking():
    epoch = request.args['epoch']
    start_end, origin_image = algorithm.start(str(epoch))
    check(start_end)
    # 请求检测照片
    detect_url = os.environ.get("PY36_SERVER_URL", None) + '/detect?image=' + origin_image
    try:
        detect_res = rq.get(detect_url, headers=headers)
    except:
        return stats.err['ErrPy36ServerError'], 404

