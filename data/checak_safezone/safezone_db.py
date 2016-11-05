# 지진대피소 원본 DB에서 추출한 자료를 검증하기 위한 DB입니다.
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


# 지진대피소의 위치정보
class POI(Base):
    """
    address: 주소
    hjdAd: 행정동 주소
    bjdAd: 법정동 주소
    roadAd: 도로명 주소
    lat: 위도
    lon: 경도
    """
    __tablename__ = 'point'
    id = Column(Integer, primary_key=True)
    hjdAd = Column(String(90))
    bjdAd = Column(String(90))
    roadAd = Column(String(90))
    lat = Column(Float(6))
    lon = Column(Float(6))

    # 관계 연결
    detail_id = Column(Integer, ForeignKey('detail.id'))
    detail = relationship("Detail", backref=backref("point", uselist=False))

    info_id = Column(Integer, ForeignKey('info.id'))
    info = relationship("Info", backref=backref("point", uselist=False))

    state_id = Column(Integer, ForeignKey('state.id'))
    state = relationship("State", backref=backref("point", uselist=False))

    def __init__(self, lat, lon, hjdAd="", bjdAd="", roadAd=""):
        self.hjdAd = hjdAd
        self.bjdAd = bjdAd
        self.roadAd = roadAd
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return "< {lat}, {lon} >".format(lat=self.lat, lon=self.lon)


# 대피소 정보
class Info(Base):
    """
    name: 대피소명
    sh_type: 대피소 종류 (건물, 주차장, 공터, 학교 등)
    sh_av: 수용인원
    """
    __tablename__ = 'info'
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    sh_type = Column(String(8))
    sh_av = Column(Integer)

    def __init__(self, name, sh_type='미확인', sh_av=0):
        self.name = name
        self.sh_type = sh_type
        self.sh_av = sh_av

    def __repr__(self):
        return "<{name} 대피소, {type}>".format(type=self.type, name=self.name)


# 건물 세부정보(건축물 대장, 내진 설계 여부등)
class Detail(Base):
    """
    건물 세부정보 테이블 명세

    auth_date: 허가일
    floor : 건물 층수
    util : 건물 용도
    area: 연면적
    
    """
    __tablename__ = 'detail'
    id = Column(Integer, primary_key=True)
    auth_date = Column(Date)
    floor = Column(Integer)
    util = Column(String(6))
    area = Column(Float)

    def __init__(self, auth_date, area, floor, util):
        self.auth_date = auth_date
        self.area = area
        self.floor = floor
        self.util = util

    def __repr__(self):
        return '< shelv detail >'


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
        return '< {} >'.format(id)
