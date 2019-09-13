import cv2

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
        #index += 1
        #RoiList.append(tmpList)
        RoiList.insert(index, tmpList)
        #print(RoiList)
        cropping = False

        # ROI 사각형을 이미지에 그립니다.
        cv2.rectangle(image, (x1,y1), (x2,y2), (0, 255, 0), 1)
        cv2.imshow("image", image)

if __name__ == '__main__':
    capture()
    index = 0
    #initiaize RoiList
    for i in range(30):
        RoiList.append([(0,0),(0,0),i])

    # 이미지를 load 합니다.
    image = cv2.imread("ParkingLot.jpg")
    # 원본 이미지를 clone 하여 복사해 둡니다.
    clone = image.copy()
    # 새 윈도우 창을 만들고 그 윈도우 창에 click_and_crop 함수를 세팅해 줍니다.
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop)


    while True:
        # 이미지를 출력하고 key 입력을 기다립니다.
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF
        # 만약 r이 입력되면, crop 할 영열을 리셋합니다.
        if key == ord("r"):
            image = clone.copy()
            for i in range(30):
               cv2.rectangle(image, RoiList[i][0], RoiList[i][1], (0, 255, 0), 1)


        #Console Out x,y
        elif key == ord("c"):
            for R in RoiList:
                print(R)
            
        elif key == ord("m"):
            number = int(input("Input number : "))
            index = number
            del RoiList[number]

        # 만약 q가 입력되면 작업을 끝냅니다.
        elif key == ord("q"):
            break

    # 모든 window를 종료합니다.
    cv2.destroyAllWindows()
