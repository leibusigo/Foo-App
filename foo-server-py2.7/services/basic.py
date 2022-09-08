# coding=utf-8
import db
import time
from flask import request
from libs.nao_proxy import nao_proxy
import vision_definitions
import numpy as np
import cv2

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

        return 'success'
    else:
        return 'ErrIpNotFound'


# nao机器人停止
def robot_stop():
    ip = request.ip
    if ip is not 1:
        motion_proxy = nao_proxy(ip)['motion_proxy']
        motion_proxy.rest()

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


# nao机器人行走
def robot_walk(distance, angle):
    ip = request.ip
    if ip is not 1:
        motion_proxy = nao_proxy(ip)['motion_proxy']
        motion_proxy.moveTo(0, 0, float(angle))
        motion_proxy.moveTo(float(distance), 0, 0)

        return 'success'
    else:
        return 'ErrIpNotFound'


# nao机器人摄像头
def robot_camera(camera_id):
    ip = request.ip
    if ip is not 1:
        camera_proxy = nao_proxy(ip)['camera_proxy']
        camera_proxy.setActiveCamera(camera_id)
        video_client = camera_proxy.subscribe("python_GVM", vision_definitions.kVGA,
                                              vision_definitions.kBGRColorSpace,
                                              20)
        frame = camera_proxy.getImageRemote(video_client)
        camera_proxy.unsubscribe(video_client)
        frame_width = frame[0]
        frame_height = frame[1]
        frame_channels = frame[2]
        frame_array = np.frombuffer(frame[6], dtype=np.uint8).reshape([frame_height, frame_width, frame_channels])
        # 保存图片到此绝对路径
        print frame_array
        # 相对路径是相对于根目录
        cv2.imwrite('../foo-front/src/assets/img/shot_cut.jpg', frame_array)

        return 'success'
    else:
        return 'ErrIpNotFound'
