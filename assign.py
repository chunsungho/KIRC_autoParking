import random
from gui_CarNumber import *


parking_area=[1,2,3,4,5,6,7,8,9,10,11,12,13]  # parking_area 리스트는 주차 가능한 공간들의 모임.

dic = {14:'none'}
temp = 0


def assign_push(key,value):
    if key in dic:
        print('해당 주차공간은 이미 차있습니다.')
    else:
        print("assign_push")
        print(str(key) + '번 주차공간에 ' + str(value) + ' 차량 등록됨')
        dic[key] = value
        parking_area.remove(key)  # list 에서 남은 주차공간 삭제해줌


def assign_pop(value):
    global temp
    temp = 0
    if value not in dic.values():
        print('그런 차는 없습니다.')
    else :
        for k, v in dic.items():  # mydict에 아이템을 하나씩 접근해서, key, value를 각각 k, v에 저.장.
            if v == value:
                print(str(k) + ' 번 주차공간에 있던 ' + str(v) + ' 차량 출차')
                temp = k
                parking_area.append(k)
        del dic[temp]

def assign_autopush(value):       # 입력값은 차량번호 4자리. 16개 자리 체크 후 할당.  # 바리케이트에서 번호를 인식하여 차량을 등록하는 함수.
                                  # value는 string 으로 입력받는게 좋음. 예를들어 '3450' 이런식으로.
    if len(parking_area) == 0:
        print('주차공간이 모두 다 찼습니다.')
    else :
        key = random.choice(parking_area)
        dic[key] = value
        print(str(key) + ' 번 주차공간에 ' + str(value) + ' 차량 등록됨')
        parking_area.remove(key)  # parking_area 리스트는 주차 가능한 공간들의 모임.
                                  # 주차를 했으니, 리스트에서 그 번호를 삭제한다.

'''
assign_autopush('1444')
assign_autopush('1226')
assign_autopush('1316')
assign_autopush('1561')
assign_autopush('5168')
assign_autopush('8948')
'''




