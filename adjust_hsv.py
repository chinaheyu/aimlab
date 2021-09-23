import cv2


image = cv2.imread('test.png')
image = cv2.resize(image, (960, 540))

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
hsv_low = [0, 0, 0]
hsv_high = [255, 255, 255]


def on_h_min_change(value):
    hsv_low[0] = value


def on_s_min_change(value):
    hsv_low[1] = value


def on_v_min_change(value):
    hsv_low[2] = value


def on_h_max_change(value):
    hsv_high[0] = value


def on_s_max_change(value):
    hsv_high[1] = value


def on_v_max_change(value):
    hsv_high[2] = value


cv2.createTrackbar('HMin', 'image', 0, 255, on_h_min_change)
cv2.createTrackbar('SMin', 'image', 0, 255, on_s_min_change)
cv2.createTrackbar('VMin', 'image', 0, 255, on_v_min_change)
cv2.createTrackbar('HMax', 'image', 255, 255, on_h_max_change)
cv2.createTrackbar('SMax', 'image', 255, 255, on_s_max_change)
cv2.createTrackbar('VMax', 'image', 255, 255, on_v_max_change)


if __name__ == '__main__':
    while True:
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv_image = cv2.inRange(hsv_image, tuple(hsv_low), tuple(hsv_high))
        cv2.imshow('result', hsv_image)
        if cv2.waitKey(100) == ord('q'):
            break
