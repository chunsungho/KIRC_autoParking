import cv2
import sys
import math
import cv2 as cv
import numpy as np

PI = 3.141592
cap = cv2.VideoCapture("lane.mp4")

while (True):
    ret, src = cap.read()

    src = cv2.resize(src, (640, 360))

    dst = cv.Canny(src, 50, 200, None, 3)

    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)

    # lines 에 어떤식으로 무슨 데이터가 저장되는거지
    lines = cv.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)

    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            #if abs(theta) < PI / 2:
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
            cv.line(cdst, pt1, pt2, (0, 0, 255), 3, cv.LINE_AA)

                #cv.imshow("test", cdst)
                #cv.waitKey(0)

    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]

            # 허프변환으로 추출된 선의 기울기 조사
            radian = math.atan2(l[3] - l[1], l[2] - l[0])
            theta2 = -radian * 180 / PI

            # 기울기가 수직에 가까운 선들만 채택
            if abs(theta2) > 45 :
                cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv.LINE_AA)
                #cv.imshow("test",cdstP)
                #cv.waitKey(0)

    cv.imshow("Source", src)
    cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
    cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
