from sqlalchemy import create_engine

"""
지진대피소DB연결 샘플 파일 입니다.
DB연결 작업시 아래 코드를 참고하세요

"""

# 지진대피소 원본 DB연결
engine = create_engine('sqlite:///origin_safezone.sqlite', echo=True)

with engine.connect() as db:
    result = db.execute("select shel_id,shel_nm,shel_av,shel_ad,lat,lon from safezone")
    for row in result:
        print(row)