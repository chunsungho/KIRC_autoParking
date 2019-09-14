import cv2
import numpy as np
import time
import SetROI

class kirc_yolo:
    def __init__(self):
        # Loading camera
        self.cnt = 0
        self.net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
        self.classes = []
        with open("coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]

        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        self.cap = cv2.VideoCapture(0)           # 웹캠 번호가 0일수도, 1일수도 그 이상일 수도 있다.
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.starting_time = time.time()
        self.frame_id = 0

        self.ls_ROI = SetROI.RoiList

    def Loop_main(self):
        while True:
            _, frame = self.cap.read()
            self.frame_id += 1
            height, width, channels = frame.shape

            # Detecting objects
            # 320*320 #416*416 #609*609 <=== 정확도 조절
            blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
            self.net.setInput(blob)
            outs = self.net.forward(self.output_layers)
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
                        # print(class_id, center_x , center_y)
                        w = int(detection[2] * width)  # width of object
                        h = int(detection[3] * height)
                        # Rectangle coordinates
                        x = int(center_x - w / 2)  # the starting X position of detected object
                        y = int(center_y - h / 2)
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))  # percentage
                        class_ids.append(class_id)  # the name of detected object
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.3)  # NMS 알고리즘(한 물체를 두개의 물체로 인식하면 이거 조정하면 돼)

            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(self.classes[class_ids[i]])
                    confidence = confidences[i]
                    color = self.colors[class_ids[i]]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.rectangle(frame, (x, y), (x + w, y + 30), color, -1)
                    cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), self.font, 3, (255, 255, 255),
                                3)

                    # 시리얼통신
                    # ser.write(bytes('h', encoding='ascii'))  # 출력방식1

            elapsed_time = time.time() - self.starting_time
            fps = self.frame_id / elapsed_time
            cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), self.font, 3, (0, 0, 0), 3)

            for r in self.ls_ROI:
                # 여기서 모든 roi 마다 그 안에 x,y 좌표가 포함이 되어있는지 판단하기
                cv2.rectangle(frame, r[0], r[1], (0, 255, 0), 1)

            cv2.imshow("Image", frame)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break


if __name__ == '__main__':
    kirc = kirc_yolo()
    kirc.Loop_main()




