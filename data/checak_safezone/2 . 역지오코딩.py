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
import requests
import configparser

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

data = session.query(POI).all()[:20]
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



# 테스트 결과 확인용 변수
g_ad_li = []
g_count = 0
g_ok = 0
g_fail = 0

print("google 결과")
for poi in data:
    g_count += 1
    print(g_count,"/",all)
    print(poi,"변환 요청")
    ad = google_ad(poi.lat,poi.lon)
    if ad[:2] == "실패":
        g_fail += 1
    else:
        g_ok += 1
    print("변환 주소: {}".format(ad))
    g_ad_li.append(ad)






print("구글 역지오코딩 결과/ 요청 :{0}  성공 : {1}, 실패 : {2}".format(all,g_ok,g_fail))

"""
for poi in data:
    poi.address = address(poi.lat, poi.lon)
session.commit()

"""