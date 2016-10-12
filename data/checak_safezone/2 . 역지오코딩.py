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

data = session.query(POI).all()[:100]
all = len(data)


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

print("다음 지오코딩 결과")
for poi in data:
    d_count += 1
    print(d_count, "/", all, " : ", poi, "변환 요청")
    ad = daum_ad(poi.lat, poi.lon)
    if ad[:2] == "실패":
        d_fail += 1
    else:
        # 조회 성공시 db에 주소 입력
        d_ok += 1

    print("변환 주소: {}".format(ad))
    d_ad_li.append(ad)


print("==========================================================================")
print("다음 지오코딩 결과/ 요청 :{0}  성공 : {1}, 실패 : {2}".format(all, d_ok, d_fail))
print("==========================================================================")

"""
for poi in data:
    poi.address = address(poi.lat, poi.lon)
session.commit()

"""
