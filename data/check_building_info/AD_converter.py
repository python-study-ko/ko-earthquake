import json

# 시군구,법정동 자료 불러오기
with open('sgg.json') as f:
    sgg = json.load(f)

with open('bjd.json') as f:
    bjd = json.load(f)

# 주소를 입력받아 시군구코드와 법정동 코드를 구해주는 함수
def sgg_cd(ad):
    data = ad.split()

    # 일치하지 않는 결과가 나올떄 까지 차례로 순회
    sgg_ad = []
    result = False
    sgg_cd =[]
    for x in data:
        sgg_ad.append(x)
        for match in sgg:
            if x == sgg[match]:
                result = True
                break
            else:
                result = False
        if result == False:
            print(sgg_ad)
            return sgg_ad

sgg_cd("광주광역시 남구")