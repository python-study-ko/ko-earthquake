# 3. 역지오코딩 실패 자료 보정
"""
역지오코딩 API 설명: http://dev.vworld.kr/dev/dv_icbbeta_s002.do?pageIndex=1&brdIde=BTA_0000000000000029&searchCondition=0&searchKeyword=
API URL : http://apis.vworld.kr/geocode?service=reverse&apiKey=인증키&[검색 파라미터]

2단계에서 역지오코딩한 결과 5건은 실패했습니다.
좌표값을 다음,네이버지도에서 육안으로 확인결과 약간의 좌표 오차로 인해 실패한 것으로 파악되며
정황상 해당좌표가 어떤 건물,장소를 지칭하는지 파악이 될경우 해당 건물의 주소, 좌표로 자료를 변경하였으며
확정 하기 힘든 자료(1건)는 제외시켰습니다

전체 작업 계획
    1. 지진대피소db 마이그레이션
    2. 위도, 경도를 역 지오코딩 하여 주소를 취득(현재 작업부분)
    3. 주소를 바탕으로 새움터에서 건축물 정보 취득
    4. 내진 설계여부 판단
    5. 정확한 자료인지 수검수
    6. 최종적으로 추출된 자료를 자체 지진대피소 DB에 추가
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.checak_safezone.safezone_db import *

# 세션 연결
engine = create_engine('sqlite:///check_safezone.sqlite')
Session = sessionmaker(bind=engine)
session = Session()

data = session.query(POI).filter_by(address="").all()
# 미반영 작업 확인
for x in data:
    print("[ id: {} | lat: {} | lon:{} ]".format(x.id,x.lat,x.lon))

"""
작업 당시 결과
[ id: 1684 | lat: 35.2016 | lon:126.1367 ]
[ id: 2189 | lat: 34.9415 | lon:128.088 ]
[ id: 2484 | lat: 34.6792 | lon:127.3584 ]
[ id: 4921 | lat: 37.5221 | lon:126.6685 ]
[ id: 5557 | lat: 37.6568 | lon:127.1154 ]

전단계에서 각 좌표에 대하여 육안으로 확인 결과 아래와 같이 판단하였습니다.
id 1684 | 염산 초등학교 낙월분교장
id 2189 | 삼천포종합운동장
id 2484 | 과역초등학교
id 4921 | 인천가현초등학교
id 5557 | 인근공터로 유츄되나 확인 불가

그래서 아래 코드를 통하여 주소,좌표값을 변경하고 id:5557의 경우 제외 처리 하였습니다.
"""


# 5557 정보 오류 처리
id_5577 = session.query(POI).filter_by(id=5557).one()
id_5577.state = State(False)

session.commit()

"""
나머지 4건은 아래 조사결과를 db에 직접 반영하였습니다.
다음에서 건물주소를 취득한후 다음 주소->좌표 API로 변환하였습니다.

id 1684
    이름: 염산 초등학교 낙월분교장
    주소: 낙월면 상낙월리 산361
    lat: 35.2020226636
    lon: 126.1367032584

id 2484
    이름: 삼천포종합운동장
    주소: 경남 사천시 벌리동 2
    lat: 34.9423723199
    lon: 128.0881928229

id 4921
    이름: 과역초등학교
    주소: 전남 고흥군 과역면 과역리 458
    lat: 34.6796451849
    lon: 127.3574053029

id 2189
    이름: 인천가현초등학교
    주소: 인천 서구 신현동 2-103
    lat: 37.5220658093
    lon: 126.6684372099
"""