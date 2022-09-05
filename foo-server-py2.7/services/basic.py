# coding=utf-8
import db
import time
from flask import request
from libs.nao_proxy import nao_proxy


# 连接nao机器人
def robot_connect(robot_ip):
    old_ip = request.ip
    # 新老ip相同表示已经连接
    if str(old_ip) is not None and str(old_ip) == str(robot_ip):
        motion_proxy = nao_proxy(robot_ip)['motion_proxy']
        motion_proxy.rest()

        return 'ErrAlreadyConnect'
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
    if ip is not None:
        motion_proxy = nao_proxy(ip)['motion_proxy']
        motion_proxy.wakeUp()
        motion_proxy.moveTo(1, 0, 0)

        return 'success'
    else:
        return 'ErrIpNotFound'


# nao机器人信息
def robot_info():
    ip = request.ip
    if ip is not None:
        battery_proxy = nao_proxy(ip)['battery_proxy']
        battery = battery_proxy.getBatteryCharge()

        return dict(battery=battery)
    else:
        return 'ErrIpNotFound'
