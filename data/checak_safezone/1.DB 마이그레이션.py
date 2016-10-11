# 정부 지진대피소 db(origin_safezone.sqlite)를 검증 db(check_safezone.sqlite)로 마이그레이션
"""
마이그레이션 대상 : 정부 지진 대피소 db(origin_safezone.sqlite)의 이름, 위도, 경도
    주소정보가 부정확하다 판단하여 대피소명, 위도, 경도만 마이그레이션 했습니다.

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
from safezone_db import *
from data.bridge import Bridge


# 세션 연결
engine = create_engine('sqlite:///check_safezone.sqlite')
Session = sessionmaker(bind=engine)
session = Session()

# 스키마 생성
Base.metadata.create_all(engine)

# 지진대피소 db연결
origin_db = Bridge("ini_sample.json")
shelv = origin_db.info['safezone']

# 추출할 자료
choice_field = ["이름","위도","경도"]

# 추출된 자료
poi_list = []

with origin_db.engin.connect() as db:
    result = db.execute("select {filds} from safezone".format(filds=",".join([shelv[x] for x in choice_field])))
    for 이름, 위도, 경도 in result:
        shelv_poi = POI(위도,경도)
        shelv_poi.info = Info(이름)
        poi_list.append(shelv_poi)

# 검증용 db에 추가
session.add_all(poi_list)
session.commit()
