# 4. 시구군 주소 약어 처리
"""
다음에서 받은 주소의 시구군 명칭이 약어('전남','충북')등으로 표시되어 제대로 검색되지 않는 문제가 있음
그래서 주소의 약어를 변경해주는 작업을 수행함

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

transData = {
    '전남':'전라남도',
    '전북':'전라북도',
    "충남":"충청남도",
    "충북":"충청북도",
    "경남":'경상북도',
    "경북":'경상북도',
    "울산":'울산광역시',
    "광주":'광주광역시',
    "대구":'대구광역시',
    '부산':'부산광역시',
    '대전':'대전광역시',
    '인천':'인천광역시',
    '서울':'서울특별시',
    '세종':'세종특별시',
    '강원':'강원도',
    '경기':'경기도',
}

data = session.query(POI).filter(POI.address != "").all()
# 주소 변경
for x in data:
    print('원본', x.address)
    ori_ad = x.address.split()[0]
    if ori_ad in transData:
        x.address = x.address.replace(ori_ad,transData[ori_ad])
    else:
        continue

session.commit()