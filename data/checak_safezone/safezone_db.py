# 지진대피소 원본 DB에서 추출한 자료를 검증하기 위한 DB입니다.
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


# 지진대피소의 위치정보
class POI(Base):
    __tablename__ = 'point'
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    address = Column(String(90))
    lat = Column(Float(6))
    lot = Column(Float(6))
    type = Column(String(8))

    # 관계 연결
    detail_id = Column(Integer, ForeignKey('detail.id'))
    detail = relationship("Detail", backref=backref("point", uselist=False))

    state_id = Column(Integer, ForeignKey('state.id'))
    state = relationship("State", backref=backref("point", uselist=False))

    def __init__(self, name, address, lat, lot, type='미확인'):
        self.name = name
        self.address = address
        self.lat = lat
        self.lot = lot
        self.type = type

    def __repr__(self):
        return "<{name} 대피소, {type}, {lat}, {lot} >".format(type=self.type, name=self.name, lat=self.lat, lot=self.lot)


# 건물 세부정보(건축물 대장, 내진 설계 여부등)
class Detail(Base):
    """
    테이블 명세
    type: 대피소 종류 (건물, 주차장, 공터, 학교 등)
    __date: 허가일
    area: 연면적
    
    """
    __tablename__ = 'detail'
    id = Column(Integer, primary_key=True)
    test = Column(String(10))

    def __init__(self, test):
        self.test = test

    def __repr__(self):
        return 'test'


# 대피소 정보에 대한 상태정보
# 잘못된 정보, 내진설계 여부 등을 관리하는 테이블, 최종 판단을 위한 테이블

class State(Base):
    """
    테이블 명세
    info_checke: 불량 정보 확인(기본 True, 무의미한 정보로 확인되면 False)
    safe_checke: 내진설계 확인(기본 False, 내진 설계 확인시 True)
    """
    __tablename__ = 'state'
    id = Column(Integer, primary_key=True)
    info_checke = Column(Boolean)
    safe_checke = Column(Boolean)

    def __init__(self, info=True, safe=False):
        self.info_checke = info
        self.safe_checke = safe

    def __repr__(self):
        return '< {}의 상태정보 입니다>'.format(id)
