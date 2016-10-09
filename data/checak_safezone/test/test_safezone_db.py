# 지진대피소 검증 DB 설계 및 테스트를 위한 코드 입니다.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from data.checak_safezone.safezone_db import POI, Detail

Base = declarative_base()

# 세션 연결
engine = create_engine('sqlite:///test/check_safezonee.sqlite')
Session = sessionmaker(bind=engine)
session = Session()

# 스키마 생성
Base.metadata.create_all(engine)

#test code
s_point = POI('대피소 샘플파일','','36.1457','127.747')
print(s_point)
print(s_point.detail)

s_point.detail = Detail('확인')


session.add(s_point)
session.commit()

for row in session.query(POI).all():
    print(row.name, row.detail.test, row.type, row.detail)
# sample.id