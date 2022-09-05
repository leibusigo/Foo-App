# coding=utf-8
from flask import Blueprint
from flask import request
from libs import stats
from services import basic

basic_api = Blueprint('basic_api', __name__)


# 连接机器人接口
@basic_api.route("/connect")
def connect():
    robot_ip = request.args['ip']
    data = basic.robot_connect(robot_ip)
    if data is 'success':
        return stats.JsonResp(0, data).res()
    else:
        return stats.err[data], 403


# 唤醒机器人接口
@basic_api.route("/wake")
def wake():
    data = basic.robot_wake()
    if data is 'success':
        return stats.JsonResp(0, data).res()
    else:
        return stats.err[data], 404


# 获取nao机器人信息
@basic_api.route("/info")
def info():
    data = basic.robot_info()
    if data is 'ErrFailToConnect':
        return stats.err[data], 404
    else:
        return stats.JsonResp(0, data).res()
