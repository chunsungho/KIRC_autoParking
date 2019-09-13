import cv2
import argparse
# import numpy as np
index = 1
RoiList = []
x1 = 0
y1 = 0
x2 = 0
y2 = 0
cropping = False

CAM_ID = 0
def capture(camid = CAM_ID):
    cam = cv2.VideoCapture(camid)
    if cam.isOpened() == False:
        print('cant open the cam (%d)' % camid)
        return None
    ret, frame = cam.read()
    if frame is None:
        print('frame is not exist')
        return None
    cv2.imwrite('ParkingLot.jpg',frame, params=[cv2.IMWRITE_PNG_COMPRESSION,0])
    cam.release()

def click_and_crop(event, x, y, flags, param):
    # refPt와 cropping 변수를 global로 만듭니다.
    global RoiList, cropping
    global x1, x2, y1, y2
    global index

    # 왼쪽 마우스가 클릭되면 (x, y) 좌표 기록을 시작하고
    # cropping = True로 만들어 줍니다.
    if event == cv2.EVENT_LBUTTONDOWN:
        x1 = x
        y1 = y
        cropping = True

    # 왼쪽 마우스 버튼이 놓여지면 (x, y) 좌표 기록을 하고 cropping 작업을 끝냅니다.
    # 이 때 crop한 영역을 보여줍니다.
    elif event == cv2.EVENT_LBUTTONUP:
        x2 = x
        y2 = y
        tmpList = [(x1,y1),(x2,y2),index]
        index += 1
        RoiList.append(tmpList)
        #print(RoiList)
        cropping = False

        # ROI 사각형을 이미지에 그립니다.
        cv2.rectangle(image, (x1,y1), (x2,y2), (0, 255, 0), 1)
        cv2.imshow("image", image)

if __name__ == '__main__':
    capture()
    index = 0
    # 이미지를 load 합니다.
    image = cv2.imread("ParkingLot.jpg")
    # 원본 이미지를 clone 하여 복사해 둡니다.
    clone = image.copy()
    # 새 윈도우 창을 만들고 그 윈도우 창에 click_and_crop 함수를 세팅해 줍니다.
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop)


    '''
    키보드에서 다음을 입력받아 수행합니다.
    - q : 작업을 끝냅니다.
    - r : 이미지를 초기화 합니다.
    - c : ROI 사각형을 그리고 좌표를 출력합니다.
    - z : revise
    '''
    while True:
        # 이미지를 출력하고 key 입력을 기다립니다.
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF
        # 만약 r이 입력되면, crop 할 영열을 리셋합니다.
        if key == ord("r"):
            image = clone.copy()

        # 만약 c가 입력되고 ROI 박스가 정확하게 입력되었다면
        # 박스의 좌표를 출력하고 crop한 영역을 출력합니다.

        #Console Out x,y
        elif key == ord("c"):
            for R in RoiList:
                print(R)

        elif key == ord('r'):


       #elif key == ord("z"):

        # 만약 q가 입력되면 작업을 끝냅니다.
        elif key == ord("q"):
            break

    # 모든 window를 종료합니다.
    cv2.destroyAllWindows()

'''
def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(points)

CAM_ID = 0
def capture(camid = CAM_ID):
    cam = cv2.VideoCapture(camid)
    if cam.isOpened() == False:
        print('cant open the cam (%d)' % camid)
        return None
    ret, frame = cam.read()
    if frame is None:
        print('frame is not exist')
        return None
    cv2.imwrite('ParkingLot.jpg',frame, params=[cv2.IMWRITE_PNG_COMPRESSION,0])
    cam.release()





if __name__ == '__main__':
    capture()
    points = list()
    img = cv2.imread("ParkingLot.jpg")
    cv2.namedWindow('img')
    cv2.setMouseCallback('img', on_mouse)
    cv2.imshow('ParkingLot.jpg', img)

    while True:
        if len(points) == 2:
            x = points[0][0]
            y = points[0][1]
            ROI = img[y:points[1][1], x:points[1][0]]
            cv2.rectangle(img, points[0], points[1], (0, 255, 0), 3)

            #break
        cv2.imshow("ROI", ROI)
        cv2.waitKey(30)


    cv2.waitKey(0)
    cv2.destroyAllWindows()

'''
