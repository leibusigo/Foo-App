# coding=utf-8
import math
from flask import Blueprint, request
from libs import stats
from libs.check import check
from services import basic

basic_api = Blueprint('basic_api', __name__)


# 连接机器人接口
@basic_api.route("/connect")
def connect():
    robot_ip = request.args['ip']
    data = basic.robot_connect(robot_ip)
    return check(data)


# 唤醒机器人接口
@basic_api.route("/wake")
def wake():
    data = basic.robot_wake()
    return check(data)


# 停止机器人接口
@basic_api.route("/stop")
def stop():
    data = basic.robot_stop()
    return check(data)


# 获取nao机器人信息
@basic_api.route("/info")
def info():
    data = basic.robot_info()
    if data is 'ErrFailToConnect':
        return stats.err[data], 404
    else:
        return stats.JsonResp(0, data).res()


# 机器人说话
@basic_api.route("/speak", methods=['POST'])
def speak():
    value = request.json['value']
    data = basic.robot_speak(value)
    return check(data)


# 机器人行走
@basic_api.route("/walk", methods=['POST'])
def walk():
    distance = request.json['distance']
    angle = request.json['angle']
    if float(distance) < 0 or float(angle) < -math.pi or float(angle) > math.pi:
        return stats.err['ErrParametersNotAllowed']
    data = basic.robot_walk(distance, angle)
    return check(data)


# 机器人摄像头
@basic_api.route("/camera")
def camera():
    camera_id = int(request.args['id'])
    data = basic.robot_camera(camera_id)
    return check(data)
