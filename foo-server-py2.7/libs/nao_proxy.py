# coding=utf-8
from naoqi import ALProxy
from libs import stats

port = 9559


def nao_proxy(ip):
    try:
        motion_proxy = ALProxy("ALMotion", str(ip), port)
        posture_proxy = ALProxy("ALRobotPosture", str(ip), port)
        camera_proxy = ALProxy("ALVideoDevice", str(ip), port)
        speech_proxy = ALProxy("ALTextToSpeech", str(ip), port)
        battery_proxy = ALProxy("ALBattery",str(ip),port)
        connect_proxy = ALProxy("ALConnectionManager", str(ip), port)

        return dict(
            motion_proxy=motion_proxy,
            posture_proxy=posture_proxy,
            camera_proxy=camera_proxy,
            speech_proxy=speech_proxy,
            battery_proxy=battery_proxy,
            connect_proxy=connect_proxy
        )
    except Exception  as e:
        # 连接失败异常
        print ("nao机器人错误log：", e)

        return stats.err['ErrFailToConnect'], 403
