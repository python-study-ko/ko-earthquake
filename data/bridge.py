from sqlalchemy import create_engine
import json

"""
DB 연결 관리 모듈 입니다.

DB관련 작업시 가독성을 향상시켜보자 만들었습니다.
일반적으로 DB 테이블의 필드명이 영문 약자인경우가 많아 다중 DB를 작업하다 보면 혼동이 오거나 매번 명세서를 확인해야 합니다.
그래서 연결할 DB정보와 필드명을 json에 작성해두고 이를 바탕으로 DB작업시 한글명을 활용하여 작업을 진행한느 것을 목표로 합니다.

json 파일 에는 DB종류, DB경로(혹은 주소), 테이블별 대응 필드 국명을 작성 해두시고 객체에서 불어와 사용하시면 됩니다.
모든 테이블의 필드를 명세할 필요는 없습니다. 필요하신 테이블과 필드에 대해서만 작성하시면 됩니다.
아직 sqlite만 지원합니다만, sqlalchemy를 기반으로 만든 것이이기 추후 다른 DB도 연결 할 수 있습니다.
"""

"""
DB명세 JSON 파일 구조

{
    # DB 종류
    "type":"sqlite",

    # DB 파일경로(sqlite일경우), 추후 다른 DB 지원시 url경로를 작성하시면 됩니다.
    "path":"origin_safezone.sqlite",

    # 불러올 테이블 및 필드 명세
    "tables":{
        "safezone": {
            "번호" : "shel_id",
            "이름" : "shel_nm",
            "위도" : "lat",
            "경도" : "lon",
            "수용 인원" : "shel_av",
            "주소" : "shel_av",
            "자료생성일" : "create_dat",
            "행정구역 코드" : "b_area_cd", # 코드 출처 확인 불가(행정동, 법정동 코드 번호 모두 아님)
        },
    },
}
"""


class Bridge:

    def __init__(self, ini_path):
        self.ini_path = str(ini_path)
        self.path = None
        self.tables = None
        self.engin = None

        def path_prefix(db_type, db_path):
            """
            DB 종류에 따라 DB 경로에 prefix를 붙여줍니다.
            :return: sqlalchemy에서 사용될 DB주소를 만들어 넘겨줍니다.
            """
            # 지원 하는 DB 및 DB별 경로 prefix
            prefix = {
                "sqlite": "sqlite:///",
            }

            try:
                return "{type}{path}".format(type=prefix[db_type], path=db_path)
            except KeyError:
                print("{0} 종류의 DB는 지원하지 않습니다. 현재 지원하는 DB는 {1} 입니다.".format(db_type, list(prefix.keys())))

        # DB 연결을 위한 기본 변수 설정
        with open(self.ini_path ,'r') as file:
            ini = json.loads(file.read())

            # 테이블별 필드 명세정보
            info = ini['tables']

            # DB 연결을 위한 경로
            self.path = path_prefix(ini["type"], ini["path"])
            # info에 명시한 테이블 목록
            self.tables = list(info.keys())
            self.engin = create_engine(self.path, echo=True)

