# coding=utf-8
from naoqi import ALProxy
from libs import stats
import time

port = 9559


def nao_proxy(ip):
    try:
        motion_proxy = ALProxy("ALMotion", str(ip), port)
        posture_proxy = ALProxy("ALRobotPosture", str(ip), port)
        camera_proxy = ALProxy("ALVideoDevice", str(ip), port)
        speech_proxy = ALProxy("ALTextToSpeech", str(ip), port)
        battery_proxy = ALProxy("ALBattery", str(ip), port)
        connect_proxy = ALProxy("ALConnectionManager", str(ip), port)

        return dict(
            motion_proxy=motion_proxy,
            posture_proxy=posture_proxy,
            camera_proxy=camera_proxy,
            speech_proxy=speech_proxy,
            battery_proxy=battery_proxy,
            connect_proxy=connect_proxy,
        )
    except:

        return stats.err['ErrFailToConnect'], 403


# 作用：控制noa转头
# 参数：angle：输入使nao偏转的角度
def turn_head(motion_proxy, angle):
    motion_proxy.setStiffnesses("Head", 1.0)
    names = ["HeadYaw", "HeadPitch"]
    # 设置转头角度[横向转头角度，纵向转头角度]
    angles = [angle, 0]
    fraction_max_speed = 0.2
    motion_proxy.setAngles(names, angles, fraction_max_speed)
    # 休眠0.75s，让nao执行完转头动作
    time.sleep(0.75)
    motion_proxy.setStiffnesses("Head", 0.0)
