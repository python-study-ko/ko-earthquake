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
import progressbar
from pprint import pprint

ini = configparser.ConfigParser()
ini.read("API_KEY.ini")

# API 정리
api_key = ini.get("sk", "KEY")
api_url = "https://apis.skplanetx.com/tmap/geo/reversegeocoding"

# sk플래닛 역지오코딩
def sk_ad(lat, lon):
    """
    경위도 좌표를 역지오코딩하여 주소를 취득
    :param lat: 위도(y)
    :param lon: 경도(x)
    :return: 주소 혹은 None
    """
    parms = {"version": 1, "lat": lat, "lon": lon, "coordType": "WGS84GEO", 'addressType':'A10'}
    headers = {'appKey': api_key}
    try:
        r = requests.get(api_url, params=parms, headers=headers)
        if r.status_code == 200:
            ad = r.json()['addressInfo']['fullAddress'].split(',') # 할일: 응답받은 자료에서 행정동,법정동,도로명주소 분리
            if len(ad) >= 4:
                ad = [ad[0], ad[1], ','.join(ad[2:])]
            return ad # (행정동,법정동,도로명) 주소로 넘겨줌
        else:
            return None
    except Exception as e:
        return "실패: 에러발생 {}".format(e)

# 변환 작업
# 세션 연결
engine = create_engine('sqlite:///check_safezone.sqlite')
Session = sessionmaker(bind=engine)
session = Session()

data = session.query(POI).all()
all = len(data)

#  지오코딩 테스트
count = 0
check = {}
fail_list = []
fail = 0

with progressbar.ProgressBar(max_value=all) as bar:
    for poi in data:
        count += 1
        ad = sk_ad(poi.lat, poi.lon)
        if ad:
            if len(ad) == 3:
                poi.hjdAd, poi.bjdAd, poi.roadAd = ad
            elif len(ad) == 2:
                poi.hjdAd, poi.bjdAd = ad
            else: # sk에서 받은 주소가 3개 이상이 아닐경우
                check[poi.id] = ad

        else:
            fail += 1
            fail_list.append((poi.x,poi.lat,poi.lon))

        bar.update(count)

session.commit()

print("==========================================================================")
print("역 지오코딩 결과/ 요청 :{0}  성공 : {1}, 실패 : {2}".format(all, all-fail, fail))
print("==========================================================================")
print("실패한 자료")
pprint(fail_list)
print("재확인 필요한 자료")
pprint(check)

"""
결과
100% (6119 of 6119) |#####################| Elapsed Time: 0:11:41 Time: 0:11:41
==========================================================================
역 지오코딩 결과/ 요청 :6119  성공 : 6119, 실패 : 0
==========================================================================
실패한 자료
[]
재확인 필요한 자료
{5516: "실패: 에러발생 Expecting ',' delimiter: line 1 column 95 (char 94)"}
"""

"""
5516 자료 보정

해당 자료를 요청하면 아래와 같은 결과가 나오는데 대림,벽산아파트가 큰따움표에 둘러쌓여 있음 이때문에 .split()를 하면 오류를 발생시키는것 같음
{"addressInfo": {    "fullAddress": "서울특별시 노원구 중계본동,서울특별시 노원구 중계동 363-8,서울특별시 노원구 한글비석로8길 20 "대림,벽산아파트"",    "addressType": "A10",    "city_do": "서울특별시",    "gu_gun": "노원구",    "eup_myun": "",    "adminDong": "중계본동",    "adminDongCode": "1135061900",    "legalDong": "중계동",    "legalDongCode": "1135010600",    "ri": "",    "bunji": "363-8",    "roadName": "한글비석로8길",    "buildingIndex": "20",    "buildingName": ""대림,벽산아파트"",    "mappingDistance": "148.192442",    "roadCode": "113504130431"  }}
그래서 위 자료는 임의로 db에 추가를 하였습니다.
"""