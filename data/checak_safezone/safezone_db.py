# 지진대피소 원본 DB에서 추출한 자료를 검증하기 위한 DB입니다.
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

# 지진대피소의 위치정보
class POI(Base):
    __tablename__ = 'point'
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    address = Column(String(90))
    lat = Column(Float(6))
    lot = Column(Float(6))
    def __init__(self,name,address,lat,lot):
        self.name = name
        self.address = address
        self.lat = lat
        self.lot = lot

    def __repr__(self):
        return "<{name} 대피소, {lat}, {lot} >".format(name=self.name, lat=self.lat, lot=self.lot)

"""
# 건물 세부정보(건축물 대장, 내진 설계 여부등)
class Detail(Base):
    __tablename__ = 'detail'
    id =

# 대피소 정보에 대한 상태정보
# 잘못된 정보, 내진설계 여부 등을 관리하는 테이블, 최종 판단을 위한 테이블

class state(Base):
    __tablename__ = 'state'
    id =
    baddata =
    safe =
"""

# 세션 연결

engine = create_engine('sqlite:///check_safezonee.sqlite')
Session = sessionmaker(bind=engine)
session = Session()

#test code
sample = POI('대피소 샘플파일','','36.1457','127.747')
print(sample.id)
print(sample.name)
print(sample.lot)
print(sample.lat)
print(sample.address)

# session.add(sample)
# session.commit()

# sample.id