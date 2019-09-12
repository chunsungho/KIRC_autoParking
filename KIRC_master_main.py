from File_IO import File_out_gui,File_out_yolo,\
    File_in_gui,File_in_yolo
import KIRC_master_function
import time
import serial

if __name__ == '__main__':

    kf = KIRC_master_function.KIRC_function()

    uartPORT = '/dev/ttyUSB0'
    ser = serial.serial_for_url(uartPORT, baudrate=115200, timeout=1)

    dirGui = '/home/chun/PycharmProjects/KIRC_Master/File_io/GtoM'
    dirYolo = '/home/chun/PycharmProjects/KIRC_Master/File_io/YtoM'

    packetGui = ''
    packetYolo = ''

    while True:
        #경로에서 읽어와
        #근데 이전에 읽었던 명령인지 판단하는게 필요함
        packetGui = File_out_gui(dirGui)
        packetYolo = File_out_yolo(dirGui)

        '''이거 실제 구동할때 추가해야함'''
        #File_in_gui(dirGui,'')
        #File_in_yolo(dirGui,'')

        # GUI에서 들어온 차정보를 가지고 led명령화 시켜서 que_buffer에 쌓음
        if packetGui != '':
            kf.queueingBuffer(packetGui)

        #yolo에서 들어온 패킷을 roi1,2,3,4에 저장하는 함수.
        kf.whichROIactive(packetYolo)
        # 지금 명령어를 실행중인지 아니면 넣어줄수 있는 상태인지 판단하는 함수
        kf.bufToOrder()
        kf.Roi_Update()
        
        #활성화된 roi가 내가 원하는 led 의 위치와 동일한지 확인
        #동일하면 코어텍스로 명령어를 보내
        #해당 Area에 대한 명령어가 종료되면 다음 명령어를 받을 준비.
        
        for R in kf.RoiList:
            str_tmp = kf.que_orderING_1[0][0] + kf.que_orderING_1[0][1]  
            if R == str_tmp:    #16R 이런식으로 되어있어서 수정해야함
                ser.write(bytes(kf.que_orderING_1[0], encoding='ascii'))  # 출력방식1
                kf.que_orderING_1.popleft()     #이 명령어를 실행했으면 이제 다시는 실행안할거니까 삭제

                if kf.que_orderING_1.__len__() == 0:
                    kf.bool_parkingArea_1 = True
                    print("1구역 명령완료")








