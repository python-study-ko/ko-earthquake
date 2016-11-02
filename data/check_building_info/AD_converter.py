import json
import os
"""
주소를 입력하면 시구군,법정동 코드를 찾아주는 소스코드 입니다.
행정표준코드관리 시스템에서 다운로드 받은 법정동코드 전체 자료(BJD_CD.txt)에서
현재 존재하는 시구군 코드와 법정동 코드를 분류하여 각각 bjd.json, sgg.json 파일에 저장했으며
해당 자료를 기반으로 주소에서 시구군,법정동 코드를 찾아 줍니다.


테스트 코드
>>> print(find_cd("광주광역시 남구 방림동 방림휴먼시아"))
    (('29155', ['광주광역시', '남구']), ('11400', ['방림동']))

>>> print(find_cd("광주광역시 동구 운림동 455"))
    (('29110', ['광주광역시', '동구']), ('12100', ['운림동']))
"""

# 시군구,법정동 자료 불러오기
path = os.path.abspath('.')

with open(os.path.join(path,'sgg.json')) as f:
    sgg = json.load(f)

with open(os.path.join(path,'bjd.json')) as f:
    bjd = json.load(f)

def uplist(data,ad,num):
    """
    시군구 코드에서 특정 행정구역이 포함된 모든 코드를 추출합니다
    :param data: 비교할 자료 원본
    :param ad: 검색할 행정구역
    :param num: 행정구역 크기(시,도 -> 0, 구,군 -> 1)
    :return: 행정구역이 포함된 모든 코드
    """
    cd_list = {}
    for x in data:
        try:
            if data[x][num] == ad:
                cd_list[x] = data[x]
        except:
            pass
    return cd_list

# 주소를 입력받아 시군구코드와 법정동 코드를 구해주는 함수
def sgg_cd(ad):
    ad_list = ad.split()

    # 주소 결과값이 1개가 나올때까지 행정구역 단위로 순회
    for x in ad_list:
        num = ad_list.index(x)
        if num == 0:
            # 최상위 행정구역일 경우 시구군 전체 자료에서 검색
            data = sgg
        data = uplist(data,x,num)

        # 유일한 시군구 코드가 나올 경우 검색 종료
        if len(data) == 1:
            for x in data:
                return (x,data[x])
        # 결과값이 없을 경우 None값 전달
        elif len(data) == 0:
            return None

def remove_sgg(sgg_ad,ad):
    # 전체 주소에서 시구군 부분만 제거해 준다
    for x in sgg_ad:
        ad.remove(x)
    return ad

def bjd_cd(CD_ssg,ad):
    ad_list = ad.split()
    data = {}   # 해당 지역의 모든 법정동 코드

    # 검색하려는 주소가 속한 시구군의 법정동 코드만 추출
    for x in bjd.keys():
        # 법정동 코드의 앞 5자리(시구군코드 부분)으로 해당 지역의 모든 법정동 코드 추출
        if x[:5] == CD_ssg[0]:
            # data 자료는 {'법정동코드번호':['시구군을 제외한 법정동 주소 리스트']}로 구성한다
            data[x] = remove_sgg(CD_ssg[1],bjd[x])

    # 추출된 자료에서 해당 지역의 법정동 코드 추출
    ad_list = remove_sgg(CD_ssg[1],ad_list)

    for x in ad_list:
        num = ad_list.index(x)
        data = uplist(data,x,num)

        # 유일한 법정동 코드가 나올 경우 검색 종료
        if len(data) == 1:
            for x in data:
                return (x[5:],data[x])
        # 결과값이 없을 경우 None값 전달
        elif len(data) == 0:
            return None




def find_cd(ad):
    CD_sgg = sgg_cd(ad)
    if CD_sgg:
        CD_bjd = bjd_cd(CD_sgg,ad)
        if CD_bjd:
            return CD_sgg,CD_bjd
        else:
            return None
    else:
        return None

# test code
print(find_cd("광주광역시 동구 운림동 455"))