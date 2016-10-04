from sqlalchemy import create_engine

"""
지진대피소DB연결 샘플 파일 입니다.
DB연결 작업시 아래 코드를 참고하세요

"""

# 지진대피소 원본 DB연결
engine = create_engine('sqlite:///origin_safezone.sqlite', echo=True)

# 지진대피소DB에서 대피소 ID, 이름, 수용 인원, 주소, 위,경도 를 추출 하는 쿼리
with engine.connect() as db:
    result = db.execute("select shel_id,shel_nm,shel_av,shel_ad,lat,lon from safezone")
    for row in result:
        print(row)


# 테이블 필드명을 국명으로 표시하여 처리하는 샘플코드 입니다. 추후 자료 가독성을 위해 구현 해봤습니다.
# todo: 클래스 재구현 하여 다른 프로젝트에서도 재사용 가능하게 만들기, 다른 프로젝트에서 테이블 명세를 입력해두면 쉽게 자료 추출 가능하게 함

FildName = {
    "번호" : "shel_id",
    "이름" : "shel_nm",
    "위도" : "lat",
    "경도" : "lon",
    "수용 인원" : "shel_av",
    "주소" : "shel_av",
    "생성일" : "create_dat",
    "행정구역 코드" : "b_area_cd", # 코드 출처 확인 불가(행정동, 법정동 코드 번호 모두 아님)
}

with engine.connect() as db:
    # 추출할 필드
    choice_fild = ['번호', '이름', '수용 인원']
    filds = [ FildName[x] for x in choice_fild]
    result = db.execute("select {filds} from safezone".format(filds=",".join(filds)))
    for row in result:
        print(row)




