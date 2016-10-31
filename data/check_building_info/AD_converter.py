import json

# 시군구,법정동 자료 불러오기
with open('sgg.json') as f:
    sgg = json.load(f)

with open('bjd.json') as f:
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
                cd_list[x] = sgg[x]
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
            return True,data
        # 아무런 결과가 없을 경우 None값 전달
        elif len(data) == 0:
            return False,data

ok,li = sgg_cd("광주광역시 남구 방림동")
print(ok,li)