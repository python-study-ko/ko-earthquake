# 대피소 위경도 좌표를 주소로 역 지오코딩
"""
다음 역지오코딩한 주소들이 법정동 기반이 아닌경우가 많아
행정동,법정동,도로명으로 구분해서 알려주는 sk플래릿 openAPI기반으로 다시 역지오코딩을 수행 했습니다.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.checak_safezone.safezone_db import *
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
        shelv_poi.state = State()
        poi_list.append(shelv_poi)

# 검증용 db에 추가
session.add_all(poi_list)
session.commit()

# 이전 작업에서 발견된 오류 자료 보정
# 5557 정보 오류 처리(무의미 자료로 판단)
id_5577 = session.query(POI).filter_by(id=5557).one()
id_5577.state = State(False)

# 좌표 불량 자료 4건
change_info = {
    1684 : {'lat':35.2020226636, 'lon':126.1367032584},
    2189 : {'lat':37.5220658093, 'lon':126.6684372099},
    2484: {'lat': 34.9423723199, 'lon': 128.0881928229},
    4921: {'lat': 34.6796451849, 'lon': 127.3574053029},
}

for x in change_info:
    error_info = session.query(POI).filter_by(id=x).one()
    error_info.lat = change_info[x]["lat"]
    error_info.lon = change_info[x]["lon"]

session.commit()

