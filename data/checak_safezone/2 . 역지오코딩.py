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

vworld_key = ini.get("vworld", "KEY")
vworld_url = "http://apis.vworld.kr/geocode"


def address(lat, lon):
    """
    경위도 좌표를 역지오코딩하여 주소를 취득
    :param lat: 위도(y)
    :param lon: 경도(x)
    :return: 주소 혹은 실패 문구
    """
    parms = {"service": "reverse", "apiKey": vworld_key, "select": "road", "crs": "epsg:4326", "x": lon, "y": lat}
    try:
        r = requests.get(vworld_url, params=parms)
        result = r.json()["response"]
        if result["result"] == "":
            return "주소가 조회되지 않습니다"
        else:
            return "{}".format(result["result"]["addr"])
    except:
        return "요청 실패"


# 세션 연결
engine = create_engine('sqlite:///check_safezone.sqlite')
Session = sessionmaker(bind=engine)
session = Session()

data = session.query(POI).all()[:300]

ad_li = []
all = len(data)
count = 0
ok = 0
fail = 0

for poi in data:
    count += 1
    print(count,"/",all)
    print(poi,"변환 요청")
    ad = address(poi.lat,poi.lon)
    if ad in ["요청 실패","주소가 조회되지 않습니다"]:
        fail += 1
    else:
        ok += 1
    print("변환 주소: {}".format(ad))
    ad_li.append(ad)

print("{0}개 작업 결과  성공 : {1}, 실패 : {2}".format(all,ok,fail))

"""
for poi in data:
    poi.address = address(poi.lat, poi.lon)
session.commit()
"""
