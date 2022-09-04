# coding=utf-8
import db
import time
from naoqi import ALProxy

port = 9559


# 连接nao机器人
def robot_connect(robot_ip):
    try:
        old_ip = db.session.find_one({"ip": str(robot_ip)})
        # 新老ip相同表示已经连接
        if old_ip is not None and str(old_ip['ip']) == str(robot_ip):
            return 'ErrAlreadyConnect'
        motion_proxy = ALProxy("ALMotion", str(robot_ip), port)
        motion_proxy.rest()
        db.session.insert({
            'ip': robot_ip,
            'createdAt': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        })
        # 将其他ip删除
        db.session.delete_many({"ip": {"$ne": robot_ip}})
        return 'success'
    except RuntimeError as e:
        # 连接失败异常
        return 'ErrFailToConnect'
