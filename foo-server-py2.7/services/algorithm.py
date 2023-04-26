# coding=utf-8
import os
import cv2
import math
from flask import request
import db
from libs.image_process import take_picture, ImageProcess
from libs.nao_proxy import nao_proxy, turn_head


# 开始跟踪
def start_tracking(is_first):
    ip = request.ip
    if ip is not 1:
        motion_proxy = nao_proxy(ip)['motion_proxy']
        posture_proxy = nao_proxy(ip)['posture_proxy']
        camera_proxy = nao_proxy(ip)['camera_proxy']
        if is_first == 'false':
            track = db.track.find_one({}, {"_id": 0})
            angle = track['angle']
            turn_head(motion_proxy, float(angle))
        # 第一轮初始化
        else:
            motion_proxy.wakeUp()
            posture_proxy.goToPosture("StandInit", 0.5)
            turn_head(motion_proxy, -1)
            db.track.delete_many({})
            db.track.insert({"angle": '-1'})
        camera_proxy.setActiveCamera(0)
        frame_array = take_picture(camera_proxy)
        base_url = os.environ.get("IMG_SAVE_PATH", None) + '/epoch1'
        ImageProcess(base_url).mkdir()
        cv2.imwrite(base_url + '/origin.jpg', frame_array)

        return 'success', base_url + '/origin.jpg'
    else:
        return 'ErrIpNotFound', ''


# 循环跟踪
def loop_tracking(epoch):
    ip = request.ip
    motion_proxy = nao_proxy(ip)['motion_proxy']
    camera_proxy = nao_proxy(ip)['camera_proxy']
    track = db.track.find_one({}, {"_id": 0})
    angle = track['angle']
    current_angle = float(angle) + 0.25
    print current_angle
    # 角度大于1，未找到目标
    if current_angle > 1:
        return '未检测到目标', ''
    # 否则更新数据库
    else:
        db.track.delete_many({})
        db.track.insert({"angle": str(current_angle)})
    if ip is not 1:
        turn_head(motion_proxy, current_angle)
        camera_proxy.setActiveCamera(0)
        frame_array = take_picture(camera_proxy)
        base_url = os.environ.get("IMG_SAVE_PATH", None) + '/epoch' + str(epoch)
        ImageProcess(base_url).mkdir()
        cv2.imwrite(base_url + '/origin.jpg', frame_array)

        return 'success', base_url + '/origin.jpg'
    else:
        return 'ErrIpNotFound', ''


# 测距跟踪
def range_and_tracking():
    ip = request.ip
    track = db.track.find_one({}, {"_id": 0})
    angle = track['angle']
    if ip is not 1:
        motion_proxy = nao_proxy(ip)['motion_proxy']
        speech_proxy = nao_proxy(ip)['speech_proxy']
        posture_proxy = nao_proxy(ip)['posture_proxy']
        forward_distance, side_distance = ranging()
        motion_proxy.moveTo(0, 0, float(angle))
        turn_head(motion_proxy, 0)
        speech_proxy.say("开始跟踪")
        # motion_proxy.moveTo((forward_distance - 1.09) / 1.25, 0, 0)
        motion_proxy.moveTo(0.8, 0, 0)
        turn_head(motion_proxy, 0)
        posture_proxy.goToPosture("StandInit", 0.5)

        return 'success'
    else:
        return 'ErrIpNotFound'


# 停止跟踪
def stop_tracking(value):
    ip = request.ip
    if ip is not 1:
        speech_proxy = nao_proxy(ip)['speech_proxy']
        motion_proxy = nao_proxy(ip)['motion_proxy']
        speech_proxy.say(value.encode('utf8'))
        motion_proxy.rest()

        return 'success'
    else:
        return 'ErrIpNotFound'


# 作用：测距
# 返回值：
#   forward_distance：nao离目标物品前向距离
#   side_distance：nao离目标物品侧向距离
def ranging():
    coordinate = db.coordinates.find_one({}, {"_id": 0})
    bottom = float(coordinate['bottom'])
    left = float(coordinate['left'])
    right = float(coordinate['right'])

    # 检测到物品下中心点的x坐标
    center_x = (left + right) / 2
    # 检测到物品下中心点的y坐标
    center_y = bottom
    dist_x = -(center_x - 640 / 2)
    dist_y = center_y - 480 / 2
    picture_angle = dist_y * (47.64 / 480)

    # 摄像头距离地面高度
    h = 0.51

    # 摄像头自身离水平线的倾角
    camera_angle = 1.2
    total_angle = picture_angle + camera_angle
    d1 = h / math.tan(total_angle * math.pi / 180)
    alpha = dist_x * (60.92 / 640)
    d2 = d1 / math.cos(alpha * math.pi / 180)
    forward_distance = round(d2 * math.cos(alpha * math.pi / 180), 2)
    side_distance = round(-d2 * math.sin(alpha * math.pi / 180), 2)
    print(forward_distance, side_distance)

    return forward_distance, side_distance
