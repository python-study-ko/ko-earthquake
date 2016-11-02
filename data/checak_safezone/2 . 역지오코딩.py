# 대피소 위경도 좌표를 주소로 역 지오코딩
"""
역지오코딩 API 설명: http://dev.vworld.kr/dev/dv_icbbeta_s002.do?pageIndex=1&brdIde=BTA_0000000000000029&searchCondition=0&searchKeyword=
API URL : http://apis.vworld.kr/geocode?service=reverse&apiKey=인증키&[검색 파라미터]

전체 작업 계획
    1. 지진대피소db 마이그레이션
    2. 위도, 경도를 역 지오코딩 하여 주소를 취득
    3. 주소를 바탕으로 새움터에서 건축물 정보 취득
    4. 내진 설계여부 판단
    5. 정확한 자료인지 수검수
    6. 최종적으로 추출된 자료를 자체 지진대피소 DB에 추가
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.checak_safezone.safezone_db import *
from data.checak_safezone.google_ad_trans import trans_ad
import requests
import configparser
from pprint import pprint

ini = configparser.ConfigParser()
ini.read("API_KEY.ini")

# API 정리
daum_key = ini.get("daum", "KEY")
daum_url = "https://apis.daum.net/local/geo/coord2detailaddr"

# 세션 연결
engine = create_engine('sqlite:///check_safezone.sqlite')
Session = sessionmaker(bind=engine)
session = Session()

data = session.query(POI).all()
all = len(data)

print("============================")
print(" 작업할 자료는 총 {}개입니다".format(all))
print("============================")
# 다음 테스트 코드
def daum_ad(lat, lon):
    """
    경위도 좌표를 역지오코딩하여 주소를 취득
    :param lat: 위도(y)
    :param lon: 경도(x)
    :return: 주소 혹은 실패 문구
    """
    parms = {"apikey": daum_key, "x": lon, "y": lat, "inputCoordSystem": "WGS84", "output": "json"}
    try:
        r = requests.get(daum_url, params=parms)
        ad = r.json()["old"]["name"]
        if ad == "":
            return "실패: 주소가 조회되지 않습니다."
        return ad
    except Exception as e:
        return "실패: 에러발생 {}".format(e)


# 다음 지오코딩 테스트
d_ad_li = []  # 다음 지오코딩 결과
d_count = 0  # 총 작업 횟수
d_ok = 0  # 성공 횟수
d_fail = 0  # 실패 횟수

print("다음 역지오코딩후 db에 반영")
for poi in data:
    d_count += 1
    print(d_count, "/", all, " : ", poi, "변환 요청")
    ad = daum_ad(poi.lat, poi.lon)
    if ad[:2] == "실패":
        d_fail += 1
        print("실패")
    else:
        # 조회 성공시 db에 주소 입력
        d_ok += 1
        poi.address = ad
        print("성공")

session.commit()
print("==========================================================================")
print("다음 지오코딩 결과/ 요청 :{0}  성공 : {1}, 실패 : {2}".format(all, d_ok, d_fail))
print("==========================================================================")


""""
작업 결과
==========================================================================
다음 지오코딩 결과/ 요청 :6119  성공 : 6114, 실패 : 5
==========================================================================

실패한 5건은 아래와 같습니다.
[ id: 1684 | lat: 35.2016 | lon:126.1367 ]
[ id: 2189 | lat: 34.9415 | lon:128.088 ]
[ id: 2484 | lat: 34.6792 | lon:127.3584 ]
[ id: 4921 | lat: 37.5221 | lon:126.6685 ]
[ id: 5557 | lat: 37.6568 | lon:127.1154 ]

수작업으로 확인한 결과
id 1684 | 낙월초등학교
id 2189 | 삼천포종합운동장
id 2484 | 과역초등학교
id 4921 | 인천가현초등학교
id 5557 | 인근공터로 유츄되나 확인 불가

위와 같이 파악됬습니다. 그래서 다음 작업에서 해당 자료에 대한 보정 작업을 진행할 예정입니다.

"""

