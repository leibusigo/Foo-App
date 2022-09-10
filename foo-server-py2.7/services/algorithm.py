# coding=utf-8
import os
import cv2
from flask import request
import db
from libs.image_process import take_picture, ImageProcess
from libs.nao_proxy import nao_proxy, turn_head


# 连接nao机器人
def start_tracking(epoch):
    ip = request.ip
    if ip is not 1:
        motion_proxy = nao_proxy(ip)['motion_proxy']
        posture_proxy = nao_proxy(ip)['posture_proxy']
        camera_proxy = nao_proxy(ip)['camera_proxy']
        # 第一轮初始化
        if epoch == '1':
            motion_proxy.wakeUp()
            posture_proxy.goToPosture("StandInit", 0.5)
            turn_head(motion_proxy, -1)
            db.track.delete_many({})
            db.track.insert({"angle": '-1'})
        camera_proxy.setActiveCamera(0)
        frame_array = take_picture(camera_proxy)
        if epoch != '1':
            db.track.delete_many({})
            db.track.insert({"angle": '-1'})
        base_url = os.environ.get("IMG_SAVE_PATH", None) + '/epoch' + str(epoch)
        ImageProcess(base_url).mkdir()
        cv2.imwrite(base_url + '/origin.jpg', frame_array)

        return 'success', base_url + '/origin.jpg'
    else:
        return 'ErrIpNotFound'
