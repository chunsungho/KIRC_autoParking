

class KIRC_function:
    def __init__(self):
        import serial
        from collections import deque
        self.n_parkingNumber = 7
        self.n_parkingArea = 2
        self.c_InOut = 'i'
        self.str_ledOrder_1 = ''
        self.str_ledOrder_2 = ''
        self.que_parkingAreaBuf_1 = deque([])
        self.que_parkingAreaBuf_2 = deque([])
        self.que_orderING_1 = deque([])
        self.que_orderING_2 = deque([])
        self.bool_parkingArea_1 = True
        self.bool_parkingArea_2 = True
        self.str_ROI_1 = ''     #실행 명령 큐의 앞부분과 동일한지 판단해야함
        self.str_ROI_2 = ''
        self.str_ROI_3 = ''
        self.str_ROI_4 = ''
        self.RoiList = []

        #ser = serial.serial_for_url(uartPORT, baudrate=115200, timeout=1)


    # 몇번주차공간, 몇번구역, in인지 out인지 판단함수
    def whichAreaOrder(self, packetGui):
        # in 인지 Out인지 판단
        InOut = packetGui[2]
        tmp = packetGui[0] + packetGui[1]
        n_order = int(tmp)
        if n_order > 6:
            if InOut == 'i':
                self.n_parkingNumber = n_order
                self.n_parkingArea = 2
                self.c_InOut = 'i'

            elif InOut == 'o':
                self.n_parkingNumber = n_order
                self.n_parkingArea = 2
                self.c_InOut = 'o'

        else:
            if InOut == 'i':
                self.n_parkingNumber = n_order
                self.n_parkingArea = 1
                self.c_InOut = 'i'

            elif InOut == 'o':
                self.n_parkingNumber = n_order
                self.n_parkingArea = 1
                self.c_InOut = 'o'

    def whichLEDneed(self):
        if self.c_InOut == 'i':
            if self.n_parkingNumber == 1:
                self.str_ledOrder_1 = "14R"
                self.str_ledOrder_2 = "22R"
            elif self.n_parkingNumber == 2:
                self.str_ledOrder_1 = "14R"
                self.str_ledOrder_2 = "23R"
            elif self.n_parkingNumber == 3:
                self.str_ledOrder_1 = "14R"
                self.str_ledOrder_2 = "24R"
            elif self.n_parkingNumber == 4:
                self.str_ledOrder_1 = "14R"
                self.str_ledOrder_2 = "22L"
            elif self.n_parkingNumber == 5:
                self.str_ledOrder_1 = "14R"
                self.str_ledOrder_2 = "23L"
            elif self.n_parkingNumber == 6:
                self.str_ledOrder_1 = "14R"
                self.str_ledOrder_2 = "24L"
            elif self.n_parkingNumber == 7:
                self.str_ledOrder_1 = "16R"
                self.str_ledOrder_2 = "27R"
            elif self.n_parkingNumber == 8:
                self.str_ledOrder_1 = "16R"
                self.str_ledOrder_2 = "28R"
            elif self.n_parkingNumber == 9:
                self.str_ledOrder_1 = "16R"
                self.str_ledOrder_2 = "29R"
            elif self.n_parkingNumber == 10:
                self.str_ledOrder_1 = "16R"
                self.str_ledOrder_2 = "26L"
            elif self.n_parkingNumber == 11:
                self.str_ledOrder_1 = "16R"
                self.str_ledOrder_2 = "27L"
            elif self.n_parkingNumber == 12:
                self.str_ledOrder_1 = "16R"
                self.str_ledOrder_2 = "28L"
            elif self.n_parkingNumber == 13:
                self.str_ledOrder_1 = "16R"
                self.str_ledOrder_2 = "29L"


        # 만약 주차장 led 설계 할때 Aisle_1,2의 LED와 Aisle_Ext led가 겹치면
        # 여기서 led 인덱스 조정 해주어야한다.
        elif self.c_InOut == 'o':
            if self.n_parkingNumber == 1:
                self.str_ledOrder_1 = "1R"
                self.str_ledOrder_2 = "18R"
            elif self.n_parkingNumber == 2:
                self.str_ledOrder_1 = "2R"
                self.str_ledOrder_2 = "18R"
            elif self.n_parkingNumber == 3:
                self.str_ledOrder_1 = "3R"
                self.str_ledOrder_2 = "18R"
            elif self.n_parkingNumber == 4:
                self.str_ledOrder_1 = "4L"
                self.str_ledOrder_2 = "18R"
            elif self.n_parkingNumber == 5:
                self.str_ledOrder_1 = "5L"
                self.str_ledOrder_2 = "18R"
            elif self.n_parkingNumber == 6:
                self.str_ledOrder_1 = "6L"
                self.str_ledOrder_2 = "18R"
            elif self.n_parkingNumber == 7:
                self.str_ledOrder_1 = "7R"
                self.str_ledOrder_2 = "20L"
            elif self.n_parkingNumber == 8:
                self.str_ledOrder_1 = "8R"
                self.str_ledOrder_2 = "20L"
            elif self.n_parkingNumber == 9:
                self.str_ledOrder_1 = "9R"
                self.str_ledOrder_2 = "20L"
            elif self.n_parkingNumber == 10:
                self.str_ledOrder_1 = "10L"
                self.str_ledOrder_2 = "20L"
            elif self.n_parkingNumber == 11:
                self.str_ledOrder_1 = "11L"
                self.str_ledOrder_2 = "20L"
            elif self.n_parkingNumber == 12:
                self.str_ledOrder_1 = "12L"
                self.str_ledOrder_2 = "20L"
            elif self.n_parkingNumber == 13:
                self.str_ledOrder_1 = "13L"
                self.str_ledOrder_2 = "20L"

    # GUI에서 들어온 차정보를 가지고 led명령화 시켜서 que_buffer에 쌓음
    def queueingBuffer(self,packetGui):
        self.whichAreaOrder(packetGui)
        self.whichLEDneed()

        if self.n_parkingArea == 1:
            self.que_parkingAreaBuf_1.append(self.str_ledOrder_1)
            self.que_parkingAreaBuf_1.append(self.str_ledOrder_2)
        if self.n_parkingArea == 2:
            self.que_parkingAreaBuf_2.append(self.str_ledOrder_1)
            self.que_parkingAreaBuf_2.append(self.str_ledOrder_2)

    def whichROIactive(self,packetYolo):
        self.str_ROI_1 = packetYolo[0] + packetYolo[1]
        self.str_ROI_2 = packetYolo[2] + packetYolo[3]
        self.str_ROI_3 = packetYolo[4] + packetYolo[5]
        self.str_ROI_4 = packetYolo[6] + packetYolo[7]

    def bufToOrder(self):
        if self.bool_parkingArea_1 == True:
            # 명령어는 2개씩 가져온다
            self.que_orderING_1.append(self.que_parkingAreaBuf_1.popleft())
            self.que_orderING_1.append(self.que_parkingAreaBuf_1.popleft())
            self.bool_parkingArea_1 = False

    def Roi_Update(self):
        self.RoiList = []
        self.RoiList.append(self.str_ROI_1)
        self.RoiList.append(self.str_ROI_2)
        self.RoiList.append(self.str_ROI_3)
        self.RoiList.append(self.str_ROI_4)

    # 활성화된 roi가 내가 원하는 led 의 위치와 동일한지 확인
    # 동일하면 코어텍스로 명령어를 보내
    # 해당 Area에 대한 명령어가 종료되면 다음 명령어를 받을 준비.
    def isTargetRoi_commandLIFI(self):
        for R in self.RoiList:
            if R == self.que_orderING_1[0]:  # 16R 이런식으로 되어있어서 수정해야함
                ser.write(bytes(self.que_orderING_1[0], encoding='ascii'))  # 출력방식1
                self.que_orderING_1.popleft()  # 이 명령어를 실행했으면 이제 다시는 실행안할거니까 삭제

                if self.que_orderING_1.__len__() == 0:
                    self.bool_parkingArea_1 = True
                    print("1구역 명령완료")

