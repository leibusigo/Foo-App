# coding=utf-8
from flask import Blueprint, request
from libs import stats
from services import algorithm

algorithm_api = Blueprint('algorithm_api', __name__)


# 连接机器人接口
@algorithm_api.route("/detect", methods=["POST"])
def detect():
    image_url = request.json['image']
    epoch = request.json['epoch']
    # 进行目标检测
    detect_result, detect_url, detect_status, detect_data = algorithm.yolo_detect(image_url, epoch)
    # 异常
    if detect_result != 'success':
        return stats.err[detect_result], 404
    # 未找到物品
    elif detect_status == 'not found':
        return stats.JsonResp(0, '没有目标类别物品').res()
    # 找到物品
    else:
        top_arr, left_arr, bottom_arr, right_arr = detect_data['top_arr'], detect_data['left_arr'], detect_data[
            'bottom_arr'], detect_data['right_arr']
        for num in range(len(top_arr)):
            print('第' + str(num + 1) + '套坐标')
            if 200 < (left_arr[num] + right_arr[num]) / 2 < 440:
                # 接受ocr识别到的文字数组
                text_arr = algorithm.ocr_test(
                    detect_data['r_image'],
                    top_arr[num],
                    bottom_arr[num],
                    left_arr[num],
                    right_arr[num],
                    epoch
                )
                print(text_arr)
                # 正则匹配
                reg_result = algorithm.reg_word(
                    text_arr,
                    top_arr[num],
                    bottom_arr[num],
                    left_arr[num],
                    right_arr[num]
                )

                return stats.JsonResp(0, reg_result).res()
            else:
                return stats.JsonResp(0, '没有物品在设置范围内').res()
