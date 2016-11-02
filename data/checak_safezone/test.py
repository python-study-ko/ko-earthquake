from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.checak_safezone.safezone_db import *
from data.check_building_info.AD_converter import find_cd


# 세션 연결
engine = create_engine('sqlite:///check_safezone.sqlite')
Session = sessionmaker(bind=engine)
session = Session()

data = session.query(POI).all()

for x in data:
    CD = find_cd(x.address)
    print(CD)
