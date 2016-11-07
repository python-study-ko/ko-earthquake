import requests
import configparser

ini = configparser.ConfigParser()
ini.read("../check_building_info/API_KEY.ini")

# API 정리
# api_key = ini.get("seumtu", "KEY")
api_key = "hb8NTDfY%2FQ2fEe4MiYwodBcwcsOn6u8TYMdYV%2BfiH9KMkahhnyiRLz%2BjnDONdensgT44OwUr6iq0IX4VgBcngg%3D%3D"
api_url = "http://apis.data.go.kr/1611000/BldRgstService/getBrRecapTitleInfo"

def saeumtu(adCd):
    """
    주소 코드가 담긴 사전을 바탕으로 세움터에 해당 주소의 건축물대장을 조회 합니다.
    :param adCd: 주소 딕셔너리 {'sgg_cd':CD_sgg[0],'bjd_cd':CD_bjd[0],'bun':last[1],'ji':last[2],"land":last[0]}
    :return:
    """
    parms = {"sigunguCd": adCd['sgg_cd'], "bjdongCd": adCd['bjd_cd'],  "bun": adCd['bun'], 'ji': adCd['ji'], 'serviceKey': api_key}
    if adCd['land']: # 대지구분 추가
        parms['platGbCd'] = adCd['land']

    try:
        r = requests.get(api_url, params=parms)
        print(r.url)
        if r.status_code == 200:
            return r.content
        else:
            return None
    except Exception as e:
        return "실패: 에러발생 {}".format(e)