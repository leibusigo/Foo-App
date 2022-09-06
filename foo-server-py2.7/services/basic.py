# coding=utf-8
import db
import time
from flask import request
from libs.nao_proxy import nao_proxy


# 连接nao机器人
def robot_connect(robot_ip):
    motion_proxy = nao_proxy(robot_ip)['motion_proxy']
    motion_proxy.rest()
    db.session.insert({
        'ip': robot_ip,
        'createdAt': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    })
    # 将其他ip删除
    db.session.delete_many({"ip": {"$ne": robot_ip}})

    return 'success'


# nao机器人唤醒
def robot_wake():
    ip = request.ip
    if ip is not 1:
        motion_proxy = nao_proxy(ip)['motion_proxy']
        motion_proxy.wakeUp()
        motion_proxy.moveTo(1, 0, 0)

        return 'success'
    else:
        return 'ErrIpNotFound'


# nao机器人信息
def robot_info():
    ip = request.ip
    if ip is not 1:
        battery_proxy = nao_proxy(ip)['battery_proxy']
        # 这里还没测试
        connect_proxy = nao_proxy(ip)['connect_proxy']
        battery = battery_proxy.getBatteryCharge()
        status = connect_proxy.state()

        return dict(battery=battery, status=status)
    else:
        return 'ErrIpNotFound'


# nao机器人说话
def robot_speak(value):
    ip = request.ip
    if ip is not 1:
        speech_proxy = nao_proxy(ip)['speech_proxy']
        # 将ascii编码换位utf-8
        speech_proxy.say(value.encode('utf8'))

        return 'success'
    else:
        return 'ErrIpNotFound'
