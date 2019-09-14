import cv2
import numpy as np
import time
import SetROI



if __name__ == '__main__':

    cnt = 0
    #### serial communication
    # 포트 설정
    PORT = '/dev/ttyUSB0'
    # 연결
    #ser = serial.serial_for_url(PORT, baudrate=115200, timeout=1)

    #### yolo
    # Load Yolo
    net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
    #net = cv2.dnn.readNet("yolov3-tiny_custom_900_conv15.weights", "yolov3-tiny_custom.cfg")
    classes = []
    with open("coco.names", "r") as f:
    #with open("obj.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # Loading camera
    cap = cv2.VideoCapture(0)           # 웹캠 번호가 0일수도, 1일수도 그 이상일 수도 있다.

    font = cv2.FONT_HERSHEY_PLAIN
    starting_time = time.time()
    frame_id = 0

    ls_ROI = SetROI.RoiList

    while True:
        _, frame = cap.read()
        frame_id += 1
        height, width, channels = frame.shape

     # Detecting objects
        # 320*320 #416*416 #609*609 <=== 정확도 조절
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)
        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    #print(class_id, center_x , center_y)
                    w = int(detection[2] * width)   # width of object
                    h = int(detection[3] * height)
                    # Rectangle coordinates
                    x = int(center_x - w / 2)       #the starting X position of detected object
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))   #percentage
                    class_ids.append(class_id)  #the name of detected object
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.3)    #NMS 알고리즘(한 물체를 두개의 물체로 인식하면 이거 조정하면 돼)

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = confidences[i]
                color = colors[class_ids[i]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.rectangle(frame, (x, y), (x + w, y + 30), color, -1)
                cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 3, (255,255,255), 3)

                #시리얼통신
                #ser.write(bytes('h', encoding='ascii'))  # 출력방식1

        elapsed_time = time.time() - starting_time
        fps = frame_id / elapsed_time
        cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), font, 3, (0, 0, 0), 3)

        for r in ls_ROI:
            # 여기서 모든 roi 마다 그 안에 x,y 좌표가 포함이 되어있는지 판단하기 
            cv2.rectangle(frame, r[0], r[1], (0, 255, 0), 1)

        cv2.imshow("Image", frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break



