from sqlalchemy import create_engine

"""
지진대피소 자료를 연결 하기 위한 스크립트 파일 입니다.

"""

# DB연결
db = create_engine('sqlite:///safezone.db', echo=True)
print(db)

with db.connect() as connection:
    result = connection.execute("select * from ")
    for row in result:
        print(row)