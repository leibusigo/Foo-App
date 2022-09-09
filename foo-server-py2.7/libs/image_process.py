# coding=utf-8
import os
import vision_definitions
import numpy as np


def take_picture(camera_proxy):
    video_client = camera_proxy.subscribe("python_GVM", vision_definitions.kVGA,
                                          vision_definitions.kBGRColorSpace,
                                          20)
    frame = camera_proxy.getImageRemote(video_client)
    camera_proxy.unsubscribe(video_client)
    frame_width = frame[0]
    frame_height = frame[1]
    frame_channels = frame[2]
    frame_array = np.frombuffer(frame[6], dtype=np.uint8).reshape([frame_height, frame_width, frame_channels])

    return frame_array


class ImageProcess:
    def __init__(self, path):
        self.path = path

    def mkdir(self):
        exist = os.path.exists(self.path)

        if not exist:
            os.makedirs(self.path)
        else:
            print('folder exists')
