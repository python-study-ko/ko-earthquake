# 행정표준코드에서 다운로드 받은 우리나라 전체 법정동코드.txt 파일에서 필요한 코드만 추출하는 코드입니다.
from pprint import pprint

# 테스트할때 최대 반복회수 지정(0일시 전체 자료를 순회)
count_limit = 200

# 시군구 코드
sgg_CD = {}

# 법정동 코드
bjd_CD = {}


def check(list):
    """
    코드 폐지여부를 확인후 코드와 주소를 분리한다.
    :param list: 법정동코드.txt에서 불러들인 코드,주소 정보
    :return: 존재하는 코드일경우 (코드,주소)
    """
    if list[-1] == '존재':
        return (list[0], list[1:-1])
    else:
        return False


# 법정동 코드 자료에서 현재 폐지되지 않는(존재하는) 법정동,시군구 코드 추출
with open("법정동코드.txt", encoding='euc-kr') as data:
    count = 0
    for line in data:
        if count_limit == 0:
            pass
        else:
            if count == count_limit:
                break
        count += 1
        info = line.split()

        # 시군구 코드
        if len(info) in [3, 4]:
            result = check(info)
            if result:
                CD, AD = result
                # 세종특별자치시 필터
                sgg_CD[CD[:5]] = AD

        # 법정동 코드
        elif len(info) in [5,6,7,8]:
            result = check(info)
            if result:
                CD,AD = result
                # 광역시외 시군구 필터
                if AD[-1][-1] in ['시','군','구']:
                    sgg_CD[CD[:5]] = AD
                else:
                    bjd_CD[CD] = AD

print(count)
sgg_count = len(sgg_CD)
bjd_count = len(bjd_CD)
all_count = sgg_count+bjd_count

print("존재 코드: {0}, 폐지 코드: {1}".format(all_count,count-all_count))
print("시군구 코드 개수 : {0}, 법정동 코드 갯수: {1}".format(sgg_count,bjd_count))
pprint(sgg_CD)
