from PIL import Image
import cv2
from yolo import YOLO
import numpy as np
import time
from paddleocr import PaddleOCR
import re


# 写txt
def write_txt(file_src, write):
    fw = open(file_src, 'w')
    fw.write(write)
    fw.close()


# 读txt
def read_txt(file_src):
    fr = open(file_src, 'r')
    read = fr.read()
    fr.close()

    return read


# 作用：清空指定txt文件
def clean_txt(file_src):
    fw = open(file_src, 'w')
    fw.truncate(0)
    fw.close()


# 校验成功函数
def until_sucess(file_scr, write):
    while True:
        sentence = read_txt(file_scr)
        if sentence == write:
            break


# 用paddle ocr进行图片文字检测
def ocr_test(r_image, top, bottom, left, right):
    cropImg = r_image[top:bottom, left:right]
    cv2.imwrite('../img/cut_result.jpg', cropImg)
    zoom = super_resolution(cropImg, top, bottom, left, right)
    # Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
    # 参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`。
    ocr = PaddleOCR(use_angle_cls=True, lang="en")  # need to run only once to download and load model into memory
    result = ocr.ocr(zoom, cls=True)
    i = 0
    textArr = []
    while i < len(result):
        textArr.append(result[i][1][0])
        # print(result[i][1][0])
        i += 1
    # print(textArr)
    return textArr


# 双三次插值主程序
def super_resolution(cropImg, top, bottom, left, right):
    zoom = function(cropImg, (bottom - top) * 5, (right - left) * 5)
    cv2.imwrite("../img/result_1.jpg", zoom)
    time.sleep(2)

    return zoom


# 双三次插值内部执行函数
def S(x):
    x = np.abs(x)
    if 0 <= x < 1:
        return 1 - 2 * x * x + x * x * x
    if 1 <= x < 2:
        return 4 - 8 * x + 5 * x * x - x * x * x
    else:
        return 0


# 双三次插值
def function(img, m, n):
    height, width, channels = img.shape
    emptyImage = np.zeros((m, n, channels), np.uint8)
    sh = m / height
    sw = n / width
    for i in range(m):
        for j in range(n):
            x = i / sh
            y = j / sw
            p = (i + 0.0) / sh - x
            q = (j + 0.0) / sw - y
            x = int(x) - 2
            y = int(y) - 2
            A = np.array([
                [S(1 + p), S(p), S(1 - p), S(2 - p)]
            ])
            if x >= m - 3:
                m - 1
            if y >= n - 3:
                n - 1
            if x >= 1 and x <= (m - 3) and y >= 1 and y <= (n - 3):
                B = np.array([
                    [img[x - 1, y - 1], img[x - 1, y],
                     img[x - 1, y + 1],
                     img[x - 1, y + 1]],
                    [img[x, y - 1], img[x, y],
                     img[x, y + 1], img[x, y + 2]],
                    [img[x + 1, y - 1], img[x + 1, y],
                     img[x + 1, y + 1], img[x + 1, y + 2]],
                    [img[x + 2, y - 1], img[x + 2, y],
                     img[x + 2, y + 1], img[x + 2, y + 1]],
                ])
                C = np.array([
                    [S(1 + q)],
                    [S(q)],
                    [S(1 - q)],
                    [S(2 - q)]
                ])
                blue = np.dot(np.dot(A, B[:, :, 0]), C)[0, 0]
                green = np.dot(np.dot(A, B[:, :, 1]), C)[0, 0]
                red = np.dot(np.dot(A, B[:, :, 2]), C)[0, 0]

                # adjust the value to be in [0,255]
                def adjust(value):
                    if value > 255:
                        value = 255
                    elif value < 0:
                        value = 0
                    return value

                blue = adjust(blue)
                green = adjust(green)
                red = adjust(red)
                emptyImage[i, j] = np.array([blue, green, red], dtype=np.uint8)

    return emptyImage


if __name__ == "__main__":

    yolo = YOLO()
    # 初始化flag，判断是否检测到目标
    flag = True
    # 当轮次为偶数时，执行py3.6程序
    turn = 2
    # 轮次标识符
    run = 1

    while True:
        sentence1 = read_txt('../txt/stop.txt')
        if sentence1 == 'stop':
            clean_txt('../txt/turn_py3.6.txt')
            write_txt('../txt/turn_py3.6.txt', str(turn + 1))
            break
        else:
            # 等待py2.7完成指令
            turn_read = read_txt('../txt/turn_py2.7.txt')
            if turn_read == "":
                continue
            else:
                # 将读取的轮次转化为int型
                turn_read = int(turn_read)
                # print(turn_read, turn)
            if turn == turn_read and turn % 2 == 0:
                print("第" + str(run) + "轮")
                # 轮次+1
                run += 1
                # time.sleep(2)
                turn = turn + 2

                image = Image.open('../img/image.jpg')
                # 使用目标检测算法对图片进行检测
                r_image, flag, top, bottom, left, right = yolo.detect_image(image, flag)
                # 返回的四个坐标值现在为数组
                print(top, bottom, left, right)
                # 将得到的数组转化为图片的形式
                r_image = np.array(r_image, np.uint8)
                # 将颜色从BGR转换为RGB
                r_image = cv2.cvtColor(r_image, cv2.COLOR_BGR2RGB)
                cv2.imwrite('../img/detect_image.jpg', r_image)
                print(flag)
                if flag:
                    # 是否找到H字符的标识符
                    findH = False
                    for num in range(len(top)):
                        print("第" + str(num + 1) + "套坐标")
                        if 200 < (left[num] + right[num]) / 2 < 440:
                            # 接受ocr识别到的文字数组
                            textArr = ocr_test(r_image, top[num], bottom[num], left[num], right[num])
                            print(textArr)
                            # print(len(textArr))
                            if len(textArr) != 0:
                                # text = textArr[0]
                                # print(text)
                                for text_num in range(len(textArr)):
                                    regexp = re.compile(r'H')
                                    # 用正则方法匹配ocr检测到的字符
                                    if regexp.search(textArr[text_num]):
                                        print("yes")
                                        cv2.imwrite('../img/image_result.jpg', r_image)
                                        write_txt('../txt/coordinate.txt',
                                                  str(top[num]) + "," + str(bottom[num]) + "," + str(
                                                      left[num]) + "," + str(right[num]))
                                        until_sucess('../txt/coordinate.txt', str(top[num]) + "," + str(bottom[num]) + "," + str(
                                                      left[num]) + "," + str(right[num]))
                                        findH = True
                                        # 结束这一轮循环
                                        if num == (len(top) - 1):
                                            write_txt('../txt/turn_py3.6.txt', str(turn - 1))
                                            print("第" + str(run - 1) + "轮结束")
                                        break
                                    else:
                                        if text_num == (len(textArr) - 1):
                                            print("该物品上不是指定标记")
                                            print("not this bottle!")
                                            # 结束这一轮循环
                                            if num == (len(top) - 1) and findH is False:
                                                write_txt('../txt/flag.txt', "none")
                                                until_sucess('../txt/flag.txt', "none")
                                                write_txt('../txt/turn_py3.6.txt', str(turn - 1))
                                                print("第" + str(run - 1) + "轮结束")
                                continue
                            else:
                                print("该物品上无标记")
                                print("not this bottle!")
                                # 结束这一轮循环
                                if num == (len(top) - 1):
                                    if findH is False:
                                        write_txt('../txt/flag.txt', "none")
                                        until_sucess('../txt/flag.txt', "none")
                                    write_txt('../txt/turn_py3.6.txt', str(turn - 1))
                                    print("第" + str(run - 1) + "轮结束")
                        else:
                            print("该物品不在指定范围内")
                            print("not this bottle!")
                            # 结束这一轮循环
                            if num == (len(top) - 1):
                                if findH is False:
                                    write_txt('../txt/flag.txt', "none")
                                    until_sucess('../txt/flag.txt', "none")
                                write_txt('../txt/turn_py3.6.txt', str(turn - 1))
                                print("第" + str(run - 1) + "轮结束")
                    continue
                else:
                    print("没有物品在指定范围内")
                    write_txt('../txt/flag.txt', "none")
                    until_sucess('../txt/flag.txt', "none")
                    write_txt('../txt/turn_py3.6.txt', str(turn - 1))
                    print("第" + str(run - 1) + "轮结束")
                    flag = True
                    continue
