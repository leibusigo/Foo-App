# coding=utf-8
from flask import Blueprint
from flask import request
from libs import stats
from services import basic

basic_api = Blueprint('basic_api', __name__)


@basic_api.route("/connect")
def connect():
    robot_ip = request.args['ip']
    data = basic.robot_connect(robot_ip)
    if data is 'success':
        return stats.JsonResp(0, data).res()
    else:
        return stats.err[data], 404


@basic_api.route("/wake")
def wake():
    # 异常处理
    try:
        # raise RuntimeError("自定义异常")
        return stats.JsonResp(0, 'path').res()
    except RuntimeError as e:
        print(stats.err['ErrTest'])
        return stats.err['ErrTest'], 404
