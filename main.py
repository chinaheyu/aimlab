import time
import cv2
import numpy as np
from mss import mss
from keys import Keys
import math


hsv_low = (68, 109, 147)
hsv_high = (102, 255, 255)


def find_target(raw_image):
    hsv_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2HSV)
    hsv_image = cv2.inRange(hsv_image, hsv_low, hsv_high)
    contours, hierarchy = cv2.findContours(hsv_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        contours = filter(lambda x: cv2.contourArea(x) > 100, contours)
        bbox = list(map(cv2.boundingRect, contours))
        return bbox
    return []


if __name__ == '__main__':
    # 延时，三秒内切到游戏界面
    time.sleep(3)

    # 屏幕捕获及鼠标按键控制
    sct = mss()
    keys = Keys()

    # 图像缩放，提升性能
    w = 960
    h = 540
    hw = w / 2
    hh = h / 2

    # PD控制器上次的误差
    last_x_error = 0
    last_y_error = 0

    while True:
        # 捕获屏幕
        image = np.array(sct.grab(sct.monitors[0]))
        # 缩放，线性插值（可以改用金字塔下采样提升性能）
        image = cv2.resize(image, (w, h), interpolation=cv2.INTER_LINEAR)
        # 定位目标
        bbox = find_target(image)
        # 如果检测到目标，进行瞄准
        if len(bbox) > 0:
            # 计算距离，筛选最近的目标
            distance = [math.sqrt((d[0] + d[2] / 2 - hw) ** 2 + (d[1] + d[3] / 2 - hh) ** 2) for d in bbox]
            best_index = distance.index(min(distance))
            box = bbox[best_index]
            # 判断是否位于目标圆心内（其实理论上应该除2√2，这里除4提升精度）
            if distance[best_index] < math.sqrt(box[2] * box[2] + box[3] * box[3]) / 4:
                # 开火
                keys.directMouse(buttons=keys.mouse_lb_press)
                time.sleep(0.001)
                keys.directMouse(buttons=keys.mouse_lb_release)
                last_x_error = 0
                last_y_error = 0
                continue
            # 移动鼠标
            x_error = hw - box[0] - box[2] / 2
            y_error = hh - box[1] - box[3] / 2
            dx = 1.5 * x_error + 0.005 * (x_error - last_x_error)
            dy = 1.5 * y_error + 0.005 * (y_error - last_y_error)
            last_x_error = x_error
            last_y_error = y_error
            keys.directMouse(int(-dx), int(-dy))
