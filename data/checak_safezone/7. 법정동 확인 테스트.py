from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.checak_safezone.safezone_db import *
from data.check_building_info.AD_converter import find_cd
from pprint import pprint
import progressbar
"""
sk API를 이용하여 받은 주소를 바탕으로 법정동 코드를 분리하는 테스트 코드입니다.
테스트 결과는 아래와 같습니다.
=============================================================
 99% (6118 of 6119) |##################### | Elapsed Time: 0:06:18 ETA: 0:00:00총 6119개의 주소에서 6117개가 성공적으로 변환됬으며 2개는 실패함
법정코드 변환 실패한 주소입니다.
===============================
['경기도 평택시 청북면 후사리 265-1', '경기도 가평군 조종면 하판리 458']
확인 결과 sk플래닛에서 변환 오류가 발생한것으로 보여 확인후 아래와 같이 직접 수정했습니다.
5897(경기도 가평군 조종면 하판리 458) -> 경기도 가평군 조종면 운악리 458
3789(경기도 평택시 청북면 후사리 265-1) -> 경기도 평택시 청북읍 후사리 265-1

위에 두가지를 보정한 결과 모든 주소가 행정표준코드에서 제공하는 법정동 코드와 매칭이 되는것을 확인했습니다.

"""
# 세션 연결
engine = create_engine('sqlite:///check_safezone.sqlite')
Session = sessionmaker(bind=engine)
session = Session()

data = session.query(POI).filter(POI.bjdAd != "").all()

count1 = 0
count2 = 0
fail = []

with progressbar.ProgressBar(max_value=len(data)) as bar:
    for x in data:
        count1 += 1
        # print(x.address)
        CD = find_cd(x.bjdAd)
        if CD:
            count2 += 1
            # print('test 결과',CD)
        else:
            fail.append(x.bjdAd)
        bar.update(count1)

print("총 {0}개의 주소에서 {1}개가 성공적으로 변환됬으며 {2}개는 실패함".format(count1,count2,count1-count2))
print("법정코드 변환 실패한 주소입니다.")
print("===============================")
pprint(fail)