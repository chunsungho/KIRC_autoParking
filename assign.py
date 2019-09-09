import random
from File_IO import File_in_gui

list_parkingArea1 = [1,2,3,4,5,6]
list_parkingArea2 = [7,8,9,10,11,12,13]

# parkingArea 리스트는 주차 가능한 공간들의 모임.

dic = {}

areaAssignFlag = 2


# 차 빠지면 리스트에서 해당번호 복구
# 사전[areNUmer] = 0
# g -> m 주차공간 정보 전송
def assign_pop(value):


    if value not in dic.values():
        print('그런 차는 없습니다.')
    else:
        for k, v in dic.items():  # mydict에 아이템을 하나씩 접근해서, key, value를 각각 k, v에 저.장.
            if v == value:
                #k 가 10의 자리인지 1의자리인지 따져야함
                if k >= 10:
                    File_in_gui("/home/chun/Desktop/KIRC_GYM/GtoM", k + 'o')
                elif k < 10:
                    File_in_gui("/home/chun/Desktop/KIRC_GYM/GtoM", '0' + str(k) + 'o')

                if k > 6:
                    list_parkingArea2.append(k)
                else:
                    list_parkingArea1.append(k)
                del dic[k]
                break

        for k, v in dic.items():
            print(str(k) + ' 번에' + str(v) + '가 있습니다.')



def assign_autopush(value):       # 입력값은 차량번호 4자리. 16개 자리 체크 후 할당.  # 바리케이트에서 번호를 인식하여 차량을 등록하는 함수.j
                                  # value는 string 으로 입력받는게 좋음. 예를들어 '3450' 이런식으로.
    global areaAssignFlag

    if areaAssignFlag == 2 :

        areaNumber= random.choice(list_parkingArea2)
        list_parkingArea2.remove(areaNumber)
        dic[areaNumber] = value

        # g -> m 으로 areaNumber 전송
        #숫자를 무조건 2자리로 맞추기 위한작업
        if areaNumber >= 10:
            str_areaNumber = str(areaNumber)
        elif areaNumber < 10:
            str_areaNumber = '0' + str(areaNumber)
        File_in_gui("/home/chun/Desktop/KIRC_GYM/GtoM", str_areaNumber + 'i')

        areaAssignFlag = 1

        print(str(areaNumber) + ' 번 주차공간에 ' + str(value) + ' 차량 등록됨')

        for k, v in dic.items():
            print(str(k) + ' 번에' + str(v) + '가 있습니다.')




    elif areaAssignFlag == 1:

        areaNumber = random.choice(list_parkingArea1)
        list_parkingArea1.remove(areaNumber)
        dic[areaNumber] = value

        # g -> m 으로 areaNumber 전송
        # 숫자를 무조건 2자리로 맞추기 위한작업
        str_areaNumber = '0' + str(areaNumber)
        File_in_gui("/home/chun/Desktop/KIRC_GYM/GtoM", str_areaNumber + 'i')

        # 디버깅용
        print(str(areaNumber) + ' 번 주차공간에 ' + str(value) + ' 차량 등록됨')
        for k, v in dic.items():
            print(str(k) + ' 번에' + str(v) + '가 있습니다.')

        areaAssignFlag = 2

