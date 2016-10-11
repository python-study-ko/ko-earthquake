# 지진대피소 검증 DB 설계 및 테스트를 위한 코드 입니다.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.checak_safezone.safezone_db import *
from data.bridge import Bridge


# 세션 연결
engine = create_engine('sqlite:///test_safezone.sqlite')
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

#test code

# 자료 추가 테스트(완료)
"""
s_point = POI('대피소 샘플파일','','36.1457','127.747')
print(s_point)
print(s_point.detail)

s_point.detail = Detail('확인')


session.add(s_point)
session.commit()

for row in session.query(POI).all():
    print(row.name, row.detail.test, row.type, row.detail)
# sample.id
"""

# 관계 자료 변경 테스트(완료)
"""
# 자료 하나만 들고올떈 .one()활용
test1 = session.query(POI).filter_by(id=1).one()
test1.detail.test = "다시변경 확인"

session.commit()
"""
