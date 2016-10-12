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
vworld_key = ini.get("vworld", "KEY")
vworld_url = "http://apis.vworld.kr/geocode"

google_key = ini.get("google","KEY")
google_url = "https://maps.googleapis.com/maps/api/geocode/json"




# 세션 연결
engine = create_engine('sqlite:///check_safezone.sqlite')
Session = sessionmaker(bind=engine)
session = Session()

data = session.query(POI).all()[:10]
all = len(data)

# 구글 테스트 코드
def google_ad(lat, lon):
    """
    경위도 좌표를 역지오코딩하여 주소를 취득
    :param lat: 위도(y)
    :param lon: 경도(x)
    :return: 주소 혹은 실패 문구
    """
    parms = {"key": google_key,"latlng":"{},{}".format(lat,lon)}
    try:
        r = requests.get(google_url, params=parms)
        status = r.json()["status"]
        results = r.json()["results"]

        if status == "OK":
            #return results[0]["address_components"] # 주소 쳬계별로 분류된 결과
            return results[0]["formatted_address"] # 전체 주소
        else:
            return "실패: {}".format(status)
    except Exception as e:
        return "실패: 에러발생 {}".format(e)


# 역 지오코딩 테스트
# 역지오코딩 결과 확인용
g_ad_li = []    # 구글 역지오코딩 결과
g_count = 0     # 총 작업 횟수
g_ok = 0        # 성공 횟수
g_fail = 0      # 실패 횟수

print("google 역지오코딩 결과")
for poi in data:
    g_count += 1
    print(g_count,"/",all," : ",poi,"변환 요청")
    ad = google_ad(poi.lat,poi.lon)
    if ad[:2] == "실패":
        g_fail += 1
    else:
        g_ok += 1
    print("변환 주소: {}".format(ad))
    g_ad_li.append(ad)

# 영문->국문 주소변환 작업
trans_ad_li = []    # 구글 국문 주소변환 결과
trans_count = 0     # 총 작업 횟수
trans_ok = 0        # 성공 횟수
trans_fail = 0      # 실패 횟수

print("google 주소 변환 결과")
for ad_en in g_ad_li:
    trans_count += 1
    print(trans_count,"/",all," : ",ad_en,"주소 변환 크롤")
    result,ad_ko = trans_ad(ad_en)

    if result in [0,2]:
        trans_fail += 1
        print(ad_ko)
        trans_ad_li.append(ad_ko)
    else:
        trans_ok += 1
        print("변환 주소: {}".format(ad_ko))
    trans_ad_li.append(ad_ko)

# 영문,국문 주소 결과 합치기
ad_merge = {}
for ad_en,ad_ko in zip(g_ad_li,trans_ad_li):
    ad_merge[ad_en] = ad_ko

print("====================================================================")
print("구글 역지오코딩 결과/ 요청 :{0}  성공 : {1}, 실패 : {2}".format(all,g_ok,g_fail))
print("구글 영문주소 변환 결과/ 요청 :{0}  성공 : {1}, 실패 : {2}".format(all,trans_ok,trans_fail))
print("====================================================================")
print("최종 변환 결과")
print(ad_merge)
"""
for poi in data:
    poi.address = address(poi.lat, poi.lon)
session.commit()

"""